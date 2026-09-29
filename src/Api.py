import asyncio
import os
from contextlib import asynccontextmanager
from datetime import date as date_

import requests
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from src.Common.CacheRepository import CacheRepository
from src.Common.DatabaseManager import DatabaseManager
from src.Common.SofascoreExtractors import extract_countries, extract_events, extract_sports
from src.Sofascore.SofascoreContainer import build_container

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, 'static')

INDEXES = {
    'countries': 'alpha2',
    'sports': 'slug',
    'teams': 'id_team',
    'tournaments': 'id_tournament',
    'team_players': 'id_team',
    'events': 'id_event',
}

container = build_container()


@asynccontextmanager
async def lifespan(app: FastAPI):
    mongo = DatabaseManager()
    for collection, key in INDEXES.items():
        await mongo.ensure_unique_index(collection, key)

    app.state.mongo = mongo
    app.state.cache = CacheRepository(mongo)
    yield
    await mongo.close()
    container.network.close()


app = FastAPI(
    title='APISofascore',
    description='Dados de futebol (e outros esportes) extraídos em tempo real da Sofascore, com cache em MongoDB.',
    version='0.2.0',
    lifespan=lifespan,
)


class TeamSummary(BaseModel):
    id: int | None = None
    name: str | None = None
    short_name: str | None = None
    slug: str | None = None


class EventSummary(BaseModel):
    id: int | None = None
    tournament: str | None = None
    category: str | None = None
    country_alpha2: str | None = None
    home_team: TeamSummary
    away_team: TeamSummary
    home_score: int | None = None
    away_score: int | None = None
    status_type: str | None = None
    status_description: str | None = None
    start_timestamp: int | None = None


@app.exception_handler(requests.RequestException)
async def handle_sofascore_error(request: Request, exc: requests.RequestException):
    return JSONResponse(status_code=502, content={'detail': f'Erro ao consultar a Sofascore: {exc}'})


def _strip_ids(documents: list[dict]) -> list[dict]:
    for document in documents:
        document.pop('_id', None)
    return documents


@app.get('/', include_in_schema=False)
async def dashboard():
    return FileResponse(os.path.join(STATIC_DIR, 'index.html'))


@app.get('/health', tags=['meta'])
async def health():
    return {'status': 'ok'}


@app.get('/live', response_model=list[EventSummary], tags=['live'])
async def live_events(sport: str = 'football'):
    events = await asyncio.to_thread(container.crawler.sport_events_live, container.network, sport)
    return extract_events(events)


@app.get('/events/today', response_model=list[EventSummary], tags=['live'])
async def events_today(sport: str = 'football', on: str = None):
    day = on or date_.today().isoformat()
    events = await asyncio.to_thread(container.crawler.sport_scheduled_events, container.network, sport, day)
    if events is None:
        raise HTTPException(
            status_code=502,
            detail=f'Agenda do dia indisponível: a Sofascore respondeu 404 em '
                   f'/sport/{sport}/scheduled-events/{day}. O endpoint de dia inteiro foi removido '
                   f'da origem — hoje a agenda só existe por torneio (scheduled-tournaments + '
                   f'unique-tournament/{{id}}/scheduled-events). Use /live para jogos em andamento.',
        )
    return extract_events(events)


@app.get('/countries', tags=['catalog'])
async def list_countries(request: Request):
    mongo: DatabaseManager = request.app.state.mongo

    cached = await mongo.find_all('countries')
    if cached:
        return {'cached': True, 'data': _strip_ids(cached)}

    categories = await asyncio.to_thread(container.crawler.sport_categories_all, container.network, 'football')
    documents = extract_countries(categories)
    await mongo.upsert_many('countries', documents, key='alpha2')
    return {'cached': False, 'data': documents}


@app.get('/sports', tags=['catalog'])
async def list_sports(request: Request):
    mongo: DatabaseManager = request.app.state.mongo

    cached = await mongo.find_all('sports')
    if cached:
        return {'cached': True, 'data': _strip_ids(cached)}

    data = await asyncio.to_thread(container.crawler.sport_event_count, container.network)
    documents = [{'slug': slug} for slug in extract_sports(data)]
    await mongo.upsert_many('sports', documents, key='slug')
    return {'cached': False, 'data': documents}


@app.get('/teams/{team_id}', tags=['teams'])
async def get_team(team_id: int, request: Request, refresh: bool = False):
    cache: CacheRepository = request.app.state.cache

    async def fetch():
        raw = await asyncio.to_thread(container.crawler.team, container.network, team_id)
        return (raw or {}).get('team')

    document, from_cache = await cache.get_or_fetch('teams', 'id_team', team_id, fetch, refresh=refresh)
    if document is None:
        raise HTTPException(status_code=404, detail='Time não encontrado na Sofascore')
    return {'cached': from_cache, 'data': document}


@app.get('/teams/{team_id}/players', tags=['teams'])
async def get_team_players(team_id: int, request: Request, refresh: bool = False):
    cache: CacheRepository = request.app.state.cache

    async def fetch():
        return await asyncio.to_thread(container.crawler.team_players, container.network, team_id)

    document, from_cache = await cache.get_or_fetch('team_players', 'id_team', team_id, fetch, refresh=refresh)
    if document is None:
        raise HTTPException(status_code=404, detail='Elenco não encontrado na Sofascore')
    return {'cached': from_cache, 'data': document['players']}


@app.get('/tournaments/{tournament_id}', tags=['tournaments'])
async def get_tournament(tournament_id: int, request: Request, refresh: bool = False):
    cache: CacheRepository = request.app.state.cache

    async def fetch():
        return await asyncio.to_thread(container.crawler.unique_tournament, container.network, tournament_id)

    document, from_cache = await cache.get_or_fetch(
        'tournaments', 'id_tournament', tournament_id, fetch, refresh=refresh)
    if document is None:
        raise HTTPException(status_code=404, detail='Campeonato não encontrado na Sofascore')
    return {'cached': from_cache, 'data': document}


@app.get('/tournaments/{tournament_id}/standings', tags=['tournaments'])
async def get_standings(tournament_id: int, season_id: int = None):
    if season_id is None:
        seasons = await asyncio.to_thread(
            container.crawler.unique_tournament_seasons, container.network, tournament_id)
        if not seasons:
            raise HTTPException(status_code=404, detail='Campeonato ou temporada não encontrados na Sofascore')
        season_id = seasons[0]['id']

    standings = await asyncio.to_thread(
        container.crawler.season_standings, container.network, tournament_id, season_id)
    if standings is None:
        raise HTTPException(status_code=404, detail='Tabela não encontrada para essa temporada')
    return {'season_id': season_id, 'data': standings}


@app.get('/events/{event_id}', tags=['events'])
async def get_event(event_id: int, request: Request, refresh: bool = False):
    cache: CacheRepository = request.app.state.cache

    async def fetch():
        return await asyncio.to_thread(container.crawler.event, container.network, event_id)

    document, from_cache = await cache.get_or_fetch('events', 'id_event', event_id, fetch, refresh=refresh)
    if document is None:
        raise HTTPException(status_code=404, detail='Partida não encontrada na Sofascore')
    return {'cached': from_cache, 'data': document}


@app.get('/events/{event_id}/h2h', tags=['events'])
async def get_event_h2h(event_id: int):
    h2h = await asyncio.to_thread(container.crawler.event_h2h, container.network, event_id)
    if h2h is None:
        raise HTTPException(status_code=404, detail='Confronto direto não encontrado na Sofascore')
    return {'data': h2h}
