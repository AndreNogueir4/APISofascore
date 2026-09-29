import asyncio
from src.Common.DatabaseManager import DatabaseManager
from src.Common.SofascoreExtractors import extract_countries, extract_sports, find_teams
from src.Sofascore.SofascoreContainer import SofascoreContainer

DEFAULT_COUNTRIES = ['BR']
DEFAULT_SPORT = 'football'

INDEXES = {
    'countries': 'alpha2',
    'sports': 'slug',
    'teams': 'id_team',
}


async def populate_countries(container: SofascoreContainer, mongo: DatabaseManager,
                             sport: str = DEFAULT_SPORT) -> int:
    categories = await asyncio.to_thread(container.crawler.sport_categories_all, container.network, sport)
    documents = extract_countries(categories)
    return await mongo.upsert_many('countries', documents, key='alpha2')


async def populate_sports(container: SofascoreContainer, mongo: DatabaseManager) -> int:
    data = await asyncio.to_thread(container.crawler.sport_event_count, container.network)
    slugs = extract_sports(data)

    documents = [{'slug': slug} for slug in slugs]
    return await mongo.upsert_many('sports', documents, key='slug')


async def populate_teams(container: SofascoreContainer, mongo: DatabaseManager,
                         countries: list[str] = None) -> int:
    team_ids = set()
    for country in countries or DEFAULT_COUNTRIES:
        data = await asyncio.to_thread(container.crawler.popular_entities, container.network, country)
        for team in find_teams(data):
            team_ids.add(team['id_team'])

    documents = []
    for team_id in team_ids:
        raw = await asyncio.to_thread(container.crawler.team, container.network, team_id)
        team = (raw or {}).get('team')
        if team is not None:
            documents.append({**team, 'id_team': team_id})

    return await mongo.upsert_many('teams', documents, key='id_team')


async def seed(container: SofascoreContainer, targets: list[str],
               countries: list[str] = None, sport: str = DEFAULT_SPORT) -> dict[str, int]:
    mongo = DatabaseManager()
    counts = {}

    try:
        for collection, key in INDEXES.items():
            await mongo.ensure_unique_index(collection, key)

        if 'countries' in targets:
            counts['countries'] = await populate_countries(container, mongo, sport)
            print(f'Países salvos: {counts["countries"]}')

        if 'sports' in targets:
            counts['sports'] = await populate_sports(container, mongo)
            print(f'Esportes salvos: {counts["sports"]}')

        if 'teams' in targets:
            counts['teams'] = await populate_teams(container, mongo, countries)
            print(f'Times salvos: {counts["teams"]}')
    finally:
        await mongo.close()

    return counts
