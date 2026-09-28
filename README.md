# APISofascore

Cliente/crawler em Python para a API interna (não-oficial) do [Sofascore](https://www.sofascore.com) — o mesmo backend `/api/v1/...` que o site usa.

> Uso pessoal / estudo / portfólio. Este não é um cliente oficial.

## Visão geral

O fluxo de descoberta de dados do Sofascore é sempre em cadeia — nenhum ID é inventado, todos vêm de uma resposta anterior:

```
sport (football | volleyball | basketball | tennis | mma)
  -> category (país/confederação)
    -> unique-tournament (a competição, ex.: Brasileirão Série A)
      -> season (a temporada, ex.: 2026)
        -> events (os jogos) / standings / rounds / top-players / ...
          -> event (o jogo em si) -> odds / incidents / lineups / h2h / statistics / ...
          -> team (os times) -> players / transfers / achievements / ...
```

## Arquitetura

Separação por responsabilidade, uma classe por camada:

```
api.py                          # API HTTP (FastAPI) + dashboard
start.py                        # seeder: popula o catálogo no Mongo
static/index.html               # dashboard de placares (zero dependências)
src/
├── Common/
│   ├── NetworkManager.py       # transporte HTTP puro (requests.Session)
│   ├── BrowserTransport.py     # transporte via Chromium (default) — passa pelo anti-bot
│   ├── DatabaseManager.py      # acesso assíncrono ao MongoDB (Motor)
│   ├── CacheRepository.py      # cache-aside: Mongo primeiro, Sofascore em miss
│   └── SofascoreExtractors.py  # normaliza a resposta crua (eventos, países, esportes, times)
└── Sofascore/
    ├── SofascoreRequestFactory.py   # monta a Request (URL + headers) — 120x build_*
    ├── SofascoreParser.py           # extrai o dado útil da Response  — 120x parse_*
    ├── SofascoreCrawler.py          # factory -> parser, 1 método por endpoint (sem prefixo)
    └── SofascoreContainer.py        # injeção de dependência: liga tudo
```

### Camada de crawler (dados brutos)

- **`NetworkManager`** — não sabe nada de Sofascore. Só abre conexão HTTP (`get`/`head`) com timeout. Retry/backoff/rate-limit ficam de fora de propósito (ver [Roadmap](#roadmap--o-que-falta)).
- **`SofascoreRequestFactory`** — sabe montar a URL e os headers certos (`Accept`, `Accept-Language: pt-BR`, `X-Requested-With`, `Referer`) para cada padrão de endpoint. Variantes que só trocam esporte/país/provedor/data/página (ex.: `categories/all` para football/volleyball/basketball/tennis) foram parametrizadas num único método em vez de duplicadas.
- **`SofascoreParser`** — recebe a `Response` crua e devolve só o que importa. Trata `404` como **dado ausente, não erro** (muitos sub-recursos só existem em janelas de tempo específicas — ex.: `lineups` antes da escalação sair, `highlights` antes do jogo acabar).
- **`SofascoreCrawler`** — API de alto nível: um método por endpoint, mesmo nome do `build_*`/`parse_*` sem prefixo, chama a factory e devolve o parser já processado.
- **`SofascoreContainer`** — instancia as quatro peças acima e expõe `.network` e `.crawler` prontos pra uso.

### Camada de serviço (API + cache)

- **`BrowserNetworkManager`** (`BrowserTransport.py`) — transporte default. Faz a chamada de dentro da página (`fetch` via `page.evaluate`), herdando TLS, HTTP/2, headers `sec-*` e cookies do Chromium. Mantém a interface `get()/head()/close()` e devolve um `BrowserResponse` com `status_code`/`json()`/`text`/`raise_for_status()`, então **nenhum dos 120 `build_*`/`parse_*` mudou**. Um único browser por processo, com todas as chamadas serializadas num worker thread (a Sync API do Playwright só pode ser tocada pela thread que a criou) e espaçadas por `min_interval`.
- **`DatabaseManager`** — wrapper assíncrono (Motor) sobre o MongoDB: `upsert_one/many` (idempotente, por chave de negócio), `find_one/all`, `ensure_unique_index`. Usa os IDs do próprio Sofascore como chave (`id_team`, `id_event`, `id_tournament`, `alpha2`, `slug`), então reimportar o mesmo dado nunca duplica.
- **`CacheRepository`** — padrão **cache-aside**: consulta o Mongo antes de bater no Sofascore e grava o resultado no miss. Todo endpoint que usa cache aceita `?refresh=true` para forçar a ida à origem.
- **`SofascoreExtractors`** — funções puras que reduzem o payload gigante do Sofascore ao essencial. `extract_sports`/`extract_countries` derivam o catálogo da própria resposta (em vez de lista fixa, que envelhece); `find_teams` varre recursivamente procurando objetos com "cara" de time.
- **`api.py`** — FastAPI. O `SofascoreContainer` é criado **fora** do event loop (o Playwright Sync API não roda dentro de um loop já em execução) e as chamadas bloqueantes do crawler vão para `asyncio.to_thread`, então o `requests` não travar o loop. Índices únicos são garantidos no `lifespan`.
- **`start.py`** — seeder idempotente: popula `countries`, `sports` e `teams` de uma vez, para a API já subir com catálogo quente.

### Divisão do cache

| Endpoint | Cache | Por quê |
|---|---|---|
| `/live`, `/events/today` | ❌ nenhum | o placar envelhece em segundos |
| `/teams/*`, `/tournaments/*`, `/events/{id}` | ✅ Mongo | dado estável, vale guardar |
| `/countries`, `/sports` | ✅ Mongo | catálogo, muda raramente |
| `/events/{id}/h2h`, `/standings` | ❌ nenhum | consulta secundária, pouco repetida |

## Como rodar

Requer **MongoDB** em `localhost:27017`.

| Variável | Default | Para quê |
|---|---|---|
| `MONGO_URI` | `mongodb://localhost:27017` | conexão do Mongo |
| `MONGO_DB` | `apisofascore` | nome do banco |
| `SOFASCORE_TRANSPORT` | `browser` | `requests` volta para a `requests.Session` (leve, mas leva 403) |
| `SOFASCORE_HEADLESS` | `1` | `0` abre o Chromium com janela, para depurar |
| `SOFASCORE_X_REQUESTED_WITH` | captura no browser | pula a captura no boot |
| `SOFASCORE_BUILD_ID` | captura no browser | idem |

As duas últimas são o escape hatch: com ambas definidas, `build_container()` não abre o browser.
Sem elas ele tenta capturar e, se o Sofascore recusar, avisa no log e sobe com os defaults em vez
de derrubar a API.

```bash
.venv/bin/pip install -r requirements.txt
.venv/bin/playwright install chromium

.venv/bin/python start.py                              # (opcional) popula o catálogo
.venv/bin/uvicorn api:app --host 0.0.0.0 --port 8000   # API + dashboard
```

- dashboard de placares: <http://localhost:8000/>
- Swagger: <http://localhost:8000/docs>

### Endpoints da API

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/live?sport=football` | jogos em andamento agora, com placar |
| `GET` | `/events/today?sport=football&on=YYYY-MM-DD` | agenda do dia |
| `GET` | `/events/{id}` | detalhe da partida |
| `GET` | `/events/{id}/h2h` | confrontos diretos |
| `GET` | `/teams/{id}` | perfil do time |
| `GET` | `/teams/{id}/players` | elenco |
| `GET` | `/tournaments/{id}` | dados da competição |
| `GET` | `/tournaments/{id}/standings?season_id=` | classificação (temporada mais recente se omitido) |
| `GET` | `/countries`, `/sports` | catálogo |
| `GET` | `/health` | healthcheck |

### Usando só o crawler (sem API/Mongo)

```bash
.venv/bin/python main.py
```

```python
from src.Sofascore.SofascoreContainer import SofascoreContainer

container = SofascoreContainer()

# geolocalização de quem está chamando
print(container.crawler.country_alpha(container.network))

# cadeia completa: categoria -> competição -> temporada -> tabela
categorias = container.crawler.sport_categories_all(container.network, sport="football")
competicoes = container.crawler.category_unique_tournaments(container.network, category_id=13)  # Brasil
temporadas = container.crawler.unique_tournament_seasons(container.network, unique_tournament_id=325)  # Brasileirão
tabela = container.crawler.season_standings(container.network, unique_tournament_id=325, season_id=87678)

# um jogo específico e seus sub-recursos
jogo = container.crawler.event(container.network, event_id=16287044)
odds = container.crawler.event_odds_all(container.network, event_id=16287044)
incidentes = container.crawler.event_incidents(container.network, event_id=16287044)
```

## Cobertura de endpoints (120 métodos)

| Seção | Conteúdo |
|---|---|
| Geral / Localização | país detectado, prioridade de esportes, contagem de jogos do dia, branding |
| Descoberta Esporte → Categoria → Torneio | categorias por esporte, competições por categoria, ao vivo/por data |
| Vitrine por Esporte | torneios em destaque, jogadores em alta, SEO, torneios "top"/default por país |
| Odds / Provedores | provedores de odds por país, eventos em destaque por provedor |
| Notícias e Transferências | posts por torneio/time/jogo, mercado de transferências |
| Torneio (unique-tournament) | info geral, temporadas, vencedores, mídia, calendário |
| Temporada (season) | classificação, rodadas, chaveamento (cuptrees), estatísticas, artilheiros, "jogador da temporada" |
| Tournament (sub-grupos) | standings e estatísticas de sub-competições dentro de um torneio maior |
| Time (team) | elenco, transferências, títulos, próximos/últimos jogos, mídia, estatísticas por temporada |
| Evento / Jogo (event) | odds, incidentes (gols/cartões), h2h, lineups, estatísticas ao vivo, votos, highlights, tv |
| Tradução | i18n de conteúdo dinâmico |
| Páginas Next.js | dados SSR usados para navegação client-side (build ID configurável) |

## Transporte: por que sai pelo browser

O edge do Sofascore (Varnish) recusa com `403` qualquer chamada cujo *fingerprint* não seja de
browser — mesmo com `X-Requested-With`, `User-Agent` e cookies corretos:

```
{"error": {"code": 403, "reason": "Forbidden" }}
```

O bloqueio não é de IP nem de endpoint: a mesma URL, no mesmo IP, chamada de dentro do contexto
do browser respondeu `200`. O que a `requests.Session` não reproduz é o TLS/HTTP2 e o conjunto de
headers `sec-*` do Chromium. Por isso o transporte default passou a ser o `BrowserNetworkManager`:

```
crawler -> factory (monta URL + headers)
             -> BrowserNetworkManager.get()
                  -> worker thread (dono do Chromium)
                       -> page.evaluate(fetch(...))   # herda TLS/HTTP2/sec-*/cookies
                  <- BrowserResponse (status_code, json(), text, raise_for_status())
             <- parser (inalterado)
```

Decisões que isso implica:

- **Um browser por processo.** O Chromium sobe no primeiro `get()` e vive até o `close()`. O
  `SofascoreContainer` aceita `network=` justamente para o `build_container()` reaproveitar a
  mesma instância no caminho de fallback em vez de subir um segundo.
- **Tudo serializado.** A Sync API do Playwright só pode ser usada pela thread que criou os
  objetos, e a API chama o crawler via `asyncio.to_thread` (várias threads). Um
  `ThreadPoolExecutor(max_workers=1)` é o dono do browser e recebe todas as chamadas. Efeito
  colateral bem-vindo: rate limiting natural, com `min_interval` espaçando as requisições.
- **`raise_for_status()` levanta `requests.HTTPError`.** Assim o handler de `RequestException`
  da `api.py` continua convertendo falha de origem em `502` sem saber qual transporte gerou.
- **`404` continua sendo "dado ausente"**, não erro — o contrato que o parser já esperava.
- **Headers proibidos pelo `fetch`** (`Referer`, `User-Agent`, `Cookie`, `Accept-Encoding`…) são
  filtrados de propósito: quem manda neles é o browser. O `X-Requested-With` passa normalmente.

O modo antigo continua disponível com `SOFASCORE_TRANSPORT=requests` — é bem mais leve (sem
Chromium) para quando a origem aceitar.

### Estado da verificação

O transporte foi validado ponta a ponta contra um servidor local que confirma a origem da chamada
(`User-Agent` do Chromium + `sec-fetch-*` presentes), cobrindo: `200`/`404`/`500`, `json()`/`text`,
`params`, repasse de `X-Requested-With`, 16 threads simultâneas, `asyncio.to_thread` e o throttle.

**Contra o Sofascore real ainda não foi confirmado:** durante o desenvolvimento o IP levou um
bloqueio mais amplo e passou a receber `403` até no `page.goto`, o que impede a validação final.
Quando o bloqueio sair, o teste é `SOFASCORE_TRANSPORT=browser` + `GET /live`. Se o `403`
persistir mesmo com a página carregando, o próximo suspeito é o `HeadlessChrome` no `User-Agent`
e no `sec-ch-ua` (visível para a origem) — daí valeria rodar com `SOFASCORE_HEADLESS=0` ou com
o Chrome real (`channel='chrome'`) para comparar.

## Roadmap / o que falta

Este repositório cobre a camada de **acesso aos dados brutos** (Factory + Parser + Crawler)
e a camada de **serviço** (API + cache + dashboard).

- [x] Persistência em banco (MongoDB) com os IDs do Sofascore como chave — `DatabaseManager`
- [x] Deduplicação/upsert via índice único + `bulk_write` idempotente
- [x] Cache na frente da própria API (Mongo, cache-aside) — `CacheRepository`
- [x] API própria (FastAPI) servindo os dados já normalizados — `api.py`
- [x] Dashboard de placares ao vivo — `static/index.html`
- [x] **Transporte via browser** — `BrowserNetworkManager`, default (ver seção acima)
- [x] Rate limiting básico — `min_interval` entre chamadas, natural por serem serializadas
- [ ] Retry com backoff exponencial (hoje o erro sobe direto para o handler)
- [ ] Confirmar o transporte contra o Sofascore real (IP bloqueado durante o desenvolvimento)
- [ ] Histórico para dados "de série no tempo" (odds, standings) — hoje o upsert sobrescreve
- [ ] Scheduler com frequência por tipo de dado (catálogo 1x/semana, jogos do dia 1x/hora, ao vivo a cada 15-30s)
- [ ] TTL no cache — hoje o documento salvo não expira, só o `?refresh=true` força a atualização
- [ ] Observabilidade: taxa de `403`/`429`, monitorar mudança do `next_build_id` (indica deploy novo)

## Considerações legais/éticas

- O endpoint `/api/v1/...` não é uma API pública documentada — é a API interna do próprio site.
- Cachear do seu lado é tanto boa prática técnica quanto forma de não pedir de novo um dado que você já tem.
