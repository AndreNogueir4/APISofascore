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
static/index.html               # dashboard de placares (zero dependências)
src/
├── __main__.py                 # CLI: serve | seed | crawl | methods
├── Api.py                      # API HTTP (FastAPI) + dashboard
├── Seeder.py                   # popula o catálogo no Mongo
├── Common/
│   ├── NetworkManager.py       # transporte HTTP puro (requests.Session)
│   ├── BrowserTransport.py     # transporte via Firefox (default) — passa pelo anti-bot
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

- **`BrowserNetworkManager`** (`BrowserTransport.py`) — transporte default. Faz a chamada de dentro da página (`fetch` via `page.evaluate`), herdando TLS, HTTP/2, headers `sec-*` e cookies do browser. Mantém a interface `get()/head()/close()` e devolve um `BrowserResponse` com `status_code`/`json()`/`text`/`raise_for_status()`, então **nenhum dos 120 `build_*`/`parse_*` mudou**. Um único browser por processo, com todas as chamadas serializadas num worker thread (a Sync API do Playwright só pode ser tocada pela thread que a criou) e espaçadas por `min_interval`.
- **`DatabaseManager`** — wrapper assíncrono (Motor) sobre o MongoDB: `upsert_one/many` (idempotente, por chave de negócio), `find_one/all`, `ensure_unique_index`. Usa os IDs do próprio Sofascore como chave (`id_team`, `id_event`, `id_tournament`, `alpha2`, `slug`), então reimportar o mesmo dado nunca duplica.
- **`CacheRepository`** — padrão **cache-aside**: consulta o Mongo antes de bater no Sofascore e grava o resultado no miss. Todo endpoint que usa cache aceita `?refresh=true` para forçar a ida à origem.
- **`SofascoreExtractors`** — funções puras que reduzem o payload gigante do Sofascore ao essencial. `extract_sports`/`extract_countries` derivam o catálogo da própria resposta (em vez de lista fixa, que envelhece); `find_teams` varre recursivamente procurando objetos com "cara" de time.
- **`Api.py`** — FastAPI. O `SofascoreContainer` é criado **fora** do event loop (o Playwright Sync API não roda dentro de um loop já em execução) e as chamadas bloqueantes do crawler vão para `asyncio.to_thread`, então o `requests` não travar o loop. Índices únicos são garantidos no `lifespan`.
- **`Seeder.py`** — seeder idempotente: popula `countries`, `sports` e `teams`, para a API já subir com catálogo quente. O `seed()` recebe quais alvos popular, então dá para rodar só uma parte.
- **`__main__.py`** — ponto de entrada único (`python -m src`). Traduz os argumentos de linha de comando nas variáveis de ambiente **antes** de qualquer import, então a escolha de transporte/banco vale para o processo inteiro, inclusive para o `uvicorn --reload` (que reimporta `src.Api:app` num subprocesso).

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
| `SOFASCORE_BROWSER` | `firefox` | engine do Playwright; `chromium` leva captcha (ver abaixo) |
| `SOFASCORE_HEADLESS` | `1` | `0` abre o browser com janela, para depurar |
| `SOFASCORE_X_REQUESTED_WITH` | captura no browser | pula a captura no boot |
| `SOFASCORE_BUILD_ID` | captura no browser | idem |

As duas últimas são o escape hatch: com ambas definidas, `build_container()` não abre o browser.
Sem elas ele tenta capturar e, se o Sofascore recusar, avisa no log e sobe com os defaults em vez
de derrubar a API.

Toda variável da tabela tem um argumento equivalente na CLI (`--transport`, `--browser`,
`--show-browser`, `--x-requested-with`, `--build-id`, `--mongo-uri`, `--mongo-db`), aceito
**antes** do comando.

```bash
.venv/bin/pip install -r requirements.txt
.venv/bin/playwright install firefox     # engine default; chromium é opcional

.venv/bin/python -m src seed                 # (opcional) popula o catálogo
.venv/bin/python -m src serve --port 8000    # API + dashboard
```

- dashboard de placares: <http://localhost:8000/>
- Swagger: <http://localhost:8000/docs>

### CLI (`python -m src`)

Um ponto de entrada, quatro comandos. `python -m src --help` (ou `<comando> --help`) lista tudo.

| Comando | Para quê |
|---|---|
| `serve` | sobe a API + dashboard — `--host`, `--port`, `--reload`, `--log-level` |
| `seed` | popula o Mongo — `--only countries sports teams`, `--country` (repetível), `--sport` |
| `crawl` | chama **um** método do crawler e imprime o JSON — `--compact` |
| `methods` | lista os 120 métodos com a assinatura — `--grep TEXTO` |

```bash
.venv/bin/python -m src serve --port 8000 --reload
.venv/bin/python -m src seed --only teams --country BR --country AR
.venv/bin/python -m src --transport requests crawl country_alpha
.venv/bin/python -m src methods --grep standings
```

### Endpoints da API

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/live?sport=football` | jogos em andamento agora, com placar |
| `GET` | `/events/today?sport=football&on=YYYY-MM-DD` | agenda do dia — **quebrado na origem**, ver abaixo |
| `GET` | `/events/{id}` | detalhe da partida |
| `GET` | `/events/{id}/h2h` | confrontos diretos |
| `GET` | `/teams/{id}` | perfil do time |
| `GET` | `/teams/{id}/players` | elenco |
| `GET` | `/tournaments/{id}` | dados da competição |
| `GET` | `/tournaments/{id}/standings?season_id=` | classificação (temporada mais recente se omitido) |
| `GET` | `/countries`, `/sports` | catálogo |
| `GET` | `/health` | healthcheck |

### `/events/today` está quebrado na origem

A Sofascore **removeu** `/sport/{sport}/scheduled-events/{date}` (responde `404`). O site passou a
montar a agenda em duas etapas: `/sport/{sport}/scheduled-tournaments/{date}/page/{n}` para listar
os torneios do dia e depois `/unique-tournament/{id}/scheduled-events/{date}` para os jogos de cada
um. Os dois endpoints funcionam e já existem no crawler (`sport_scheduled_tournaments`,
`unique_tournament_scheduled_events`).

O problema é o custo: num dia medido foram **7 páginas / 454 torneios distintos = 461 requests**
(~3 min, serializadas pelo `min_interval`). Não cabe dentro de uma request HTTP. Usar só os
torneios em destaque (`default_unique_tournaments`, 22 torneios) não resolve: em data FIFA eles
têm zero jogos enquanto as seleções jogam.

Por ora o endpoint **falha alto** — `502` com a explicação no `detail` — em vez de devolver lista
vazia. O parser trata `404` como "dado ausente" e devolvia `None`, que o `extract_events`
transformava em `[]`, tornando o erro indistinguível de "não tem jogo hoje". Para jogos em
andamento use `/live`, que não foi afetado.

### Usando só o crawler (sem API/Mongo)

O comando `crawl` faz o bind dos argumentos pela própria assinatura do método: posicionais na
ordem declarada, `chave=valor` para nomeados, com `int`/`float`/`bool`/`None` convertidos. Nome de
método errado ou argumento faltando falha na hora (exit `2`), antes de subir o browser.

```bash
.venv/bin/python -m src methods --grep season          # descobre o que existe
.venv/bin/python -m src crawl country_alpha
.venv/bin/python -m src crawl sport_categories_all football
.venv/bin/python -m src crawl season_standings 325 87678
.venv/bin/python -m src crawl sport_events_live football --compact
```

Ou direto do Python, sem passar pela CLI:

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
headers `sec-*` de um browser real. Por isso o transporte default passou a ser o
`BrowserNetworkManager`:

```
crawler -> factory (monta URL + headers)
             -> BrowserNetworkManager.get()
                  -> worker thread (dono do browser)
                       -> page.evaluate(fetch(...))   # herda TLS/HTTP2/sec-*/cookies
                  <- BrowserResponse (status_code, json(), text, raise_for_status())
             <- parser (inalterado)
```

Decisões que isso implica:

- **Um browser por processo.** O browser sobe no primeiro `get()` e vive até o `close()`. O
  `SofascoreContainer` aceita `network=` justamente para o `build_container()` reaproveitar a
  mesma instância no caminho de fallback em vez de subir um segundo.
- **Tudo serializado.** A Sync API do Playwright só pode ser usada pela thread que criou os
  objetos, e a API chama o crawler via `asyncio.to_thread` (várias threads). Um
  `ThreadPoolExecutor(max_workers=1)` é o dono do browser e recebe todas as chamadas. Efeito
  colateral bem-vindo: rate limiting natural, com `min_interval` espaçando as requisições.
- **`raise_for_status()` levanta `requests.HTTPError`.** Assim o handler de `RequestException`
  da `Api.py` continua convertendo falha de origem em `502` sem saber qual transporte gerou.
- **`404` continua sendo "dado ausente"**, não erro — o contrato que o parser já esperava.
- **Headers proibidos pelo `fetch`** (`Referer`, `User-Agent`, `Cookie`, `Accept-Encoding`…) são
  filtrados de propósito: quem manda neles é o browser. O `X-Requested-With` passa normalmente.

O modo antigo continua disponível com `SOFASCORE_TRANSPORT=requests` — é bem mais leve (sem
browser) para quando a origem aceitar.

### O engine importa: Chromium leva captcha, Firefox não

Em setembro de 2026 o anti-bot apertou, e o Chromium do Playwright passou a ser **desafiado antes
de carregar a home**. O `page.goto('https://www.sofascore.com/pt')` é redirecionado para
`/captcha.html?redirectUrl=...`, uma página de Cloudflare Turnstile. A cascata:

- sem `__NEXT_DATA__` na página de desafio → `next_build_id` fica `None`
- nenhum XHR para `/api/v1/` → `x_requested_with` fica `None`
- `fetch_dynamic_params()` levanta, `build_container()` cai nos defaults
- todo request de dados volta `403 {"reason": "challenge"}` → `502` na API

O desafio não é algo que se resolva no código: é um veredito de fingerprint, dado antes de
qualquer validação existir. Mas ele **não é disparado em outro engine**. Medido no mesmo IP, na
mesma máquina:

| engine | captcha | `buildId` | requests `/api/v1/` | `x-requested-with` |
|---|---|---|---|---|
| chromium (headless e headed) | **sim** | `None` | 0 | — |
| firefox headless | não | capturado | 282 | capturado |
| firefox headed | não | capturado | 282 | capturado |

Nem UA realista nem `--disable-blink-features=AutomationControlled` nem rodar com janela salvam o
Chromium. Por isso o default é **`firefox`**, com `--browser chromium` mantido para quando a maré
virar. Se o engine for desafiado, o aviso no boot diz isso explicitamente em vez de reclamar
genericamente da captura.

**O valor do `X-Requested-With` não é o que libera a chamada.** Medido de dentro de uma página
Firefox não desafiada, o mesmo `/sport/football/events/live` respondeu `200` com 413891 bytes em
todos os casos:

| `X-Requested-With` | resposta |
|---|---|
| `2589dc` (default antigo) | `200` |
| `d063ba` (capturado horas antes) | `200` |
| `deadbeef` (lixo) | `200` |
| vazio | `200` |
| header ausente | `200` |

Ou seja: o token nunca foi a causa dos `403`, e os defaults vencidos eram inofensivos. O que a
origem avalia é o **contexto do browser** (fingerprint, TLS, cookies), não o header. O header
continua sendo capturado e enviado por fidelidade ao que o site faz, mas não conte com ele como
chave de acesso — e não gaste tempo caçando o valor "certo".

Dois detalhes que isso deixou claro:

- **A página de desafio vem com `200`.** Qualquer checagem de `response.ok` passa batido nela; o
  que denuncia é a URL (`_challenged()`).
- **O `X-Requested-With` só aparece no primeiro XHR**, depois do `domcontentloaded`. Ler os
  parâmetros logo após o `goto` funciona ou não conforme a sorte de timing — daí o
  `_await_api_call()` esperando o handler preencher.

### Estado da verificação

O transporte foi validado ponta a ponta contra um servidor local que confirma a origem da chamada
(`User-Agent` do browser + `sec-fetch-*` presentes), cobrindo: `200`/`404`/`500`, `json()`/`text`,
`params`, repasse de `X-Requested-With`, 16 threads simultâneas, `asyncio.to_thread` e o throttle.

**Contra o Sofascore real: confirmado** (Chromium, antes do captcha). A origem respondeu `200`:
`crawl country_alpha` devolveu o geo-IP correto, `sport_categories_all` 298 categorias,
`sport_events_live` 78 jogos com placar, e o `python -m src seed` gravou 274 países / 19 esportes
/ 69 times em 30s. Pela API, 12 dos 13 endpoints responderam `200` (o 13º é o `/events/today`,
quebrado na origem — ver acima).

**Reconfirmado em 2026-09-30, com Firefox headless.** Boot limpo, sem cair nos defaults
(`x_requested_with` e `next_build_id` capturados na home). `/live?sport=football` respondeu `200`
em três chamadas consecutivas — 99 jogos com placar, 4,5s / 1,8s / 0,7s (a primeira paga o boot do
browser). Também `200` em `/live?sport=basketball`, `/tournaments/325`,
`/tournaments/325/standings`, `/events/{id}`, `/teams/{id}`, `/countries`, `/sports` e `/health`.
Três boots seguidos da CLI sem nenhum `[aviso]`.

**O `403` é intermitente e sensível a volume.** Uma varredura de ~460 requests (paginação de
`scheduled-tournaments`) derrubou o IP em `403` de novo poucos minutos depois, inclusive em
`/country/alpha2`, mesmo com o `page.goto` continuando a carregar normalmente. Ou seja: o bloqueio
não é só de fingerprint, tem também um componente de rate limit por volume. O `min_interval` de
0,4s não é suficiente para uma varredura grande — reforça o item de backoff no roadmap.

## Roadmap / o que falta

Este repositório cobre a camada de **acesso aos dados brutos** (Factory + Parser + Crawler)
e a camada de **serviço** (API + cache + dashboard).

- [x] Persistência em banco (MongoDB) com os IDs do Sofascore como chave — `DatabaseManager`
- [x] Deduplicação/upsert via índice único + `bulk_write` idempotente
- [x] Cache na frente da própria API (Mongo, cache-aside) — `CacheRepository`
- [x] API própria (FastAPI) servindo os dados já normalizados — `src/Api.py`
- [x] Dashboard de placares ao vivo — `static/index.html`
- [x] **Transporte via browser** — `BrowserNetworkManager`, default (ver seção acima)
- [x] Rate limiting básico — `min_interval` entre chamadas, natural por serem serializadas
- [x] Confirmar o transporte contra o Sofascore real — `200` na origem com o transporte de browser
- [ ] Retry com backoff exponencial (hoje o erro sobe direto para o handler) — o `403` volta sob volume
- [ ] Reconstruir `/events/today` pelo caminho novo (`scheduled-tournaments` + por torneio), como job
  em background com cache no Mongo: 461 requests não cabem numa request HTTP
- [ ] Histórico para dados "de série no tempo" (odds, standings) — hoje o upsert sobrescreve
- [ ] Scheduler com frequência por tipo de dado (catálogo 1x/semana, jogos do dia 1x/hora, ao vivo a cada 15-30s)
- [ ] TTL no cache — hoje o documento salvo não expira, só o `?refresh=true` força a atualização
- [ ] Observabilidade: taxa de `403`/`429`, monitorar mudança do `next_build_id` (indica deploy novo)

## Considerações legais/éticas

- O endpoint `/api/v1/...` não é uma API pública documentada — é a API interna do próprio site.
- Cachear do seu lado é tanto boa prática técnica quanto forma de não pedir de novo um dado que você já tem.
