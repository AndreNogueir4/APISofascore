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
src/
├── Common/
│   └── NetworkManager.py       # transporte HTTP puro (requests.Session)
└── Sofascore/
    ├── SofascoreRequestFactory.py   # monta a Request (URL + headers) — 118x build_*
    ├── SofascoreParser.py           # extrai o dado útil da Response  — 118x parse_*
    ├── SofascoreCrawler.py          # factory -> parser, 1 método por endpoint (sem prefixo)
    └── SofascoreContainer.py        # injeção de dependência: liga tudo
```

- **`NetworkManager`** — não sabe nada de Sofascore. Só abre conexão HTTP (`get`/`head`) com timeout. Retry/backoff/rate-limit ficam de fora de propósito (ver [Roadmap](#roadmap--o-que-falta)).
- **`SofascoreRequestFactory`** — sabe montar a URL e os headers certos (`Accept`, `Accept-Language: pt-BR`, `X-Requested-With`, `Referer`) para cada padrão de endpoint. Variantes que só trocam esporte/país/provedor/data/página (ex.: `categories/all` para football/volleyball/basketball/tennis) foram parametrizadas num único método em vez de duplicadas.
- **`SofascoreParser`** — recebe a `Response` crua e devolve só o que importa. Trata `404` como **dado ausente, não erro** (muitos sub-recursos só existem em janelas de tempo específicas — ex.: `lineups` antes da escalação sair, `highlights` antes do jogo acabar).
- **`SofascoreCrawler`** — API de alto nível: um método por endpoint, mesmo nome do `build_*`/`parse_*` sem prefixo, chama a factory e devolve o parser já processado.
- **`SofascoreContainer`** — instancia as quatro peças acima e expõe `.network` e `.crawler` prontos pra uso.

## Como rodar

```bash
.venv/bin/pip install -r requirements.txt
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

## Cobertura de endpoints (118 métodos)

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

## Sobre o header anti-bot (`X-Requested-With`)

Esse header é gerado por JS de fingerprinting no navegador e muda por sessão. `SofascoreRequestFactory` aceita um valor fixo via construtor (`x_requested_with`, default é o observado na captura). Na prática, endpoints de baixo risco (ex.: `country/alpha2`) respondem normalmente mesmo com esse valor "velho" — não confirmamos ainda que isso vale para todos os 118 endpoints. **Não implementamos gerenciamento de sessão via Playwright de propósito**: é complexidade desnecessária até o momento em que o crawler realmente começar a levar `403`/`429`.

## Roadmap / o que falta

Este repositório cobre a camada de **acesso aos dados brutos** (Factory + Parser + Crawler).

- [ ] Rate limiting + retry com backoff exponencial no `NetworkManager` (hoje ele só faz a chamada crua)
- [ ] `SessionManager` (Playwright) — só se/quando começarmos a apanhar `403`/`429`
- [ ] Persistência em banco (Postgres) com os IDs do Sofascore como chave primária + `raw jsonb`
- [ ] Deduplicação/upsert e histórico para dados "de série no tempo" (odds, standings)
- [ ] Scheduler com frequência por tipo de dado (catálogo 1x/semana, jogos do dia 1x/hora, ao vivo a cada 15-30s)
- [ ] Cache (Redis) na frente da própria API
- [ ] API própria (FastAPI) servindo os dados já normalizados — nunca o Sofascore em tempo real
- [ ] Observabilidade: taxa de `403`/`429`, monitorar mudança do `next_build_id` (indica deploy novo)

## Considerações legais/éticas

- O endpoint `/api/v1/...` não é uma API pública documentada — é a API interna do próprio site.
- Cachear do seu lado é tanto boa prática técnica quanto forma de não pedir de novo um dado que você já tem.
