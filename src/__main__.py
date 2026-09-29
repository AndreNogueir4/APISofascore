import argparse
import asyncio
import inspect
import json
import os
import sys

SEED_TARGETS = ('countries', 'sports', 'teams')


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='python -m src',
        description='APISofascore: crawler da API interna do Sofascore, com API HTTP e cache em MongoDB.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            'exemplos:\n'
            '  python -m src serve --port 8000 --reload\n'
            '  python -m src seed --only countries sports\n'
            '  python -m src seed --only teams --country BR --country AR\n'
            '  python -m src crawl country_alpha\n'
            '  python -m src crawl sport_categories_all football\n'
            '  python -m src crawl sport_scheduled_events football 2026-09-29\n'
            '  python -m src crawl season_standings 325 72034 kind=home\n'
            '  python -m src methods --grep event\n'
        ),
    )

    transport = parser.add_argument_group('transporte')
    transport.add_argument('--transport', choices=('browser', 'requests'),
                           help='browser (default) passa pelo anti-bot; requests é leve mas leva 403')
    transport.add_argument('--show-browser', action='store_true',
                           help='abre o Chromium com janela, para depurar')
    transport.add_argument('--x-requested-with', metavar='TOKEN',
                           help='usa esse X-Requested-With e pula a captura no boot')
    transport.add_argument('--build-id', metavar='ID',
                           help='usa esse buildId do Next e pula a captura no boot')

    database = parser.add_argument_group('banco')
    database.add_argument('--mongo-uri', metavar='URI', help='default: mongodb://localhost:27017')
    database.add_argument('--mongo-db', metavar='NAME', help='default: apisofascore')

    commands = parser.add_subparsers(dest='command', metavar='comando', required=True)

    serve = commands.add_parser('serve', help='sobe a API HTTP (FastAPI) e o dashboard')
    serve.add_argument('--host', default='0.0.0.0')
    serve.add_argument('--port', type=int, default=8000)
    serve.add_argument('--reload', action='store_true', help='recarrega a cada alteração no código')
    serve.add_argument('--log-level', default='info',
                       choices=('critical', 'error', 'warning', 'info', 'debug', 'trace'))
    serve.set_defaults(handler=run_serve)

    seed = commands.add_parser('seed', help='popula o catálogo no MongoDB (idempotente)')
    seed.add_argument('--only', nargs='+', choices=SEED_TARGETS, default=list(SEED_TARGETS),
                      metavar='ALVO', help=f'o que popular: {", ".join(SEED_TARGETS)} (default: todos)')
    seed.add_argument('--country', action='append', dest='countries', metavar='ALPHA2',
                      help='país de onde descobrir os times (repetível, default: BR)')
    seed.add_argument('--sport', default='football', help='esporte usado no catálogo de países')
    seed.set_defaults(handler=run_seed)

    crawl = commands.add_parser(
        'crawl', help='chama um método do crawler e imprime o JSON',
        description='Chama um método do SofascoreCrawler. Os argumentos posicionais vão na ordem '
                    'da assinatura; use chave=valor para nomeados.')
    crawl.add_argument('method', help='nome do método (veja: python -m src methods)')
    crawl.add_argument('args', nargs='*', metavar='ARG', help='valor posicional ou chave=valor')
    crawl.add_argument('--compact', action='store_true', help='JSON em uma linha, sem indentação')
    crawl.set_defaults(handler=run_crawl)

    methods = commands.add_parser('methods', help='lista os métodos disponíveis no crawler')
    methods.add_argument('--grep', metavar='TEXTO', help='filtra por parte do nome')
    methods.set_defaults(handler=run_methods)

    return parser


def apply_environment(args: argparse.Namespace):
    environment = {
        'SOFASCORE_TRANSPORT': args.transport,
        'SOFASCORE_HEADLESS': '0' if args.show_browser else None,
        'SOFASCORE_X_REQUESTED_WITH': args.x_requested_with,
        'SOFASCORE_BUILD_ID': args.build_id,
        'MONGO_URI': args.mongo_uri,
        'MONGO_DB': args.mongo_db,
    }
    for key, value in environment.items():
        if value is not None:
            os.environ[key] = value


def coerce(value: str):
    if value.lower() in ('true', 'false'):
        return value.lower() == 'true'
    if value.lower() in ('none', 'null'):
        return None
    for cast in (int, float):
        try:
            return cast(value)
        except ValueError:
            continue
    return value


def split_arguments(raw: list[str]) -> tuple[list, dict]:
    positional, keyword = [], {}
    for item in raw:
        name, separator, value = item.partition('=')
        if separator and name.isidentifier():
            keyword[name] = coerce(value)
        elif keyword:
            raise SystemExit(f'erro: argumento posicional "{item}" veio depois de um chave=valor')
        else:
            positional.append(coerce(item))
    return positional, keyword


def bare_crawler():
    from src.Sofascore.SofascoreCrawler import SofascoreCrawler
    from src.Sofascore.SofascoreParser import SofascoreParser
    from src.Sofascore.SofascoreRequestFactory import SofascoreRequestFactory

    return SofascoreCrawler(SofascoreRequestFactory(), SofascoreParser())


def crawler_methods(crawler) -> dict[str, inspect.Signature]:
    return {
        name: inspect.signature(member)
        for name, member in inspect.getmembers(crawler, inspect.ismethod)
        if not name.startswith('_')
    }


def describe(name: str, signature: inspect.Signature) -> str:
    parameters = []
    for parameter in list(signature.parameters.values())[1:]:
        if parameter.default is inspect.Parameter.empty:
            parameters.append(parameter.name)
        else:
            parameters.append(f'{parameter.name}={parameter.default!r}')
    return f'{name}({", ".join(parameters)})'


def run_serve(args: argparse.Namespace) -> int:
    import uvicorn

    uvicorn.run('src.Api:app', host=args.host, port=args.port,
                reload=args.reload, log_level=args.log_level)
    return 0


def run_seed(args: argparse.Namespace) -> int:
    import requests

    from src.Seeder import seed
    from src.Sofascore.SofascoreContainer import build_container

    container = build_container()
    try:
        asyncio.run(seed(container, args.only, args.countries, args.sport))
    except requests.RequestException as exc:
        print(f'erro: a Sofascore recusou a chamada: {exc}', file=sys.stderr)
        return 1
    finally:
        container.network.close()
    return 0


def run_crawl(args: argparse.Namespace) -> int:
    import requests

    from src.Sofascore.SofascoreContainer import build_container

    available = crawler_methods(bare_crawler())
    if args.method not in available:
        print(f'erro: método "{args.method}" não existe. '
              f'Use "python -m src methods" para ver a lista.', file=sys.stderr)
        return 2

    signature = available[args.method]
    positional, keyword = split_arguments(args.args)
    try:
        signature.bind(None, *positional, **keyword)
    except TypeError as exc:
        print(f'erro: argumentos inválidos para {describe(args.method, signature)}: {exc}',
              file=sys.stderr)
        return 2

    container = build_container()
    try:
        bound = signature.bind(container.network, *positional, **keyword)
        data = getattr(container.crawler, args.method)(*bound.args, **bound.kwargs)
    except requests.RequestException as exc:
        print(f'erro: a Sofascore recusou a chamada: {exc}', file=sys.stderr)
        return 1
    finally:
        container.network.close()

    indent = None if args.compact else 2
    print(json.dumps(data, indent=indent, ensure_ascii=False, default=str))
    return 0


def run_methods(args: argparse.Namespace) -> int:
    available = crawler_methods(bare_crawler())

    names = sorted(available)
    if args.grep:
        needle = args.grep.lower()
        names = [name for name in names if needle in name.lower()]

    for name in names:
        print(describe(name, available[name]))

    print(f'\n{len(names)} de {len(available)} métodos.', file=sys.stderr)
    return 0


def main(argv: list[str] = None) -> int:
    args = build_parser().parse_args(argv)
    apply_environment(args)
    return args.handler(args)


if __name__ == '__main__':
    raise SystemExit(main())
