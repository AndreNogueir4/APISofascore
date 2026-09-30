import json
import time
from concurrent.futures import ThreadPoolExecutor

from playwright.sync_api import sync_playwright
from requests.exceptions import ConnectionError as RequestsConnectionError, HTTPError

from src.Common.NetworkManager import NetworkManager

FORBIDDEN_HEADERS = frozenset({
    'accept-charset', 'accept-encoding', 'connection', 'content-length', 'cookie', 'date',
    'expect', 'host', 'keep-alive', 'origin', 'referer', 'te', 'trailer', 'transfer-encoding',
    'upgrade', 'user-agent', 'via',
})

FETCH_JS = """
async ({url, headers, method}) => {
    const response = await fetch(url, {method, headers, credentials: 'same-origin'});
    const body = await response.text();
    const responseHeaders = {};
    response.headers.forEach((value, key) => { responseHeaders[key] = value; });
    return {status: response.status, body: body, headers: responseHeaders};
}
"""


class BrowserResponse:
    def __init__(self, url: str, status_code: int, text: str, headers: dict):
        self.url = url
        self.status_code = status_code
        self.text = text
        self.headers = headers or {}

    @property
    def ok(self) -> bool:
        return self.status_code < 400

    @property
    def content(self) -> bytes:
        return self.text.encode('utf-8')

    def json(self):
        return json.loads(self.text)

    def raise_for_status(self):
        if 400 <= self.status_code < 500:
            kind = 'Client Error'
        elif 500 <= self.status_code < 600:
            kind = 'Server Error'
        else:
            return
        raise HTTPError(f'{self.status_code} {kind}: for url: {self.url}', response=self)

    def __repr__(self) -> str:
        return f'<BrowserResponse [{self.status_code}]>'


class BrowserNetworkManager(NetworkManager):
    def __init__(self, root_url: str = 'https://www.sofascore.com/pt', timeout: float = 30.0,
                 headless: bool = True, min_interval: float = 0.4, locale: str = 'pt-BR',
                 engine: str = 'firefox', capture_timeout: float = 20.0):
        super().__init__(timeout)
        self.root_url = root_url
        self.headless = headless
        self.min_interval = min_interval
        self.locale = locale
        self.engine = engine
        self.capture_timeout = capture_timeout

        self._executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix='sofascore-browser')
        self._playwright = None
        self._browser = None
        self._context = None
        self._page = None
        self._started = False
        self._last_request_at = 0.0
        self._dynamic_params = {'x_requested_with': None, 'next_build_id': None}

    def get(self, url: str, headers: dict = None, params: dict = None) -> BrowserResponse:
        return self._submit(self._request, 'GET', url, headers, params)

    def head(self, url: str, headers: dict = None, params: dict = None) -> BrowserResponse:
        return self._submit(self._request, 'HEAD', url, headers, params)

    def fetch_dynamic_params(self, url: str = None, timeout: float = None) -> dict:
        self._submit(self._ensure_started)
        params = dict(self._dynamic_params)
        if not params['x_requested_with'] or not params['next_build_id']:
            raise RuntimeError(
                f'Could not extract dynamic params from the page via "{self.engine}": {params}')
        return params

    def close(self):
        if self._started:
            try:
                self._submit(self._teardown)
            except Exception:
                pass
        self._executor.shutdown(wait=True)
        super().close()

    def _submit(self, fn, *args):
        return self._executor.submit(fn, *args).result()

    def _ensure_started(self):
        if self._started:
            return
        self._playwright = sync_playwright().start()
        self._browser = getattr(self._playwright, self.engine).launch(headless=self.headless)
        self._context = self._browser.new_context(locale=self.locale)
        self._page = self._context.new_page()
        self._page.on('request', self._capture_x_requested_with)
        self._started = True

        response = self._page.goto(self.root_url, wait_until='domcontentloaded',
                                   timeout=self.timeout * 1000)
        status = response.status if response else 'no response'
        if response is None or not response.ok:
            print(f'[aviso] não foi possível carregar {self.root_url} no browser (status: {status}).')
            return

        # A página de desafio é servida com 200, então o response.ok acima não a pega.
        if self._challenged():
            print(f'[aviso] o anti-bot da Sofascore devolveu um desafio (captcha) para o engine '
                  f'"{self.engine}" — a home não carregou, então não há parâmetros para capturar. '
                  f'O engine "firefox" passa sem desafio (--browser firefox).')
            return

        self._await_api_call()
        self._dynamic_params['next_build_id'] = self._page.evaluate(
            '() => window.__NEXT_DATA__?.buildId')

    def _challenged(self) -> bool:
        return 'captcha' in self._page.url or 'challenge' in self._page.url

    def _await_api_call(self):
        # O buildId já existe no domcontentloaded, mas o X-Requested-With só aparece quando a
        # página dispara o primeiro XHR — sem esperar por ele, a captura depende de sorte de
        # timing. Quem preenche é o _capture_x_requested_with; aqui só cedemos tempo a ele.
        deadline = time.monotonic() + self.capture_timeout
        while not self._dynamic_params['x_requested_with']:
            if time.monotonic() >= deadline:
                return
            self._page.wait_for_timeout(250)

    def _capture_x_requested_with(self, request):
        if self._dynamic_params['x_requested_with'] is None and '/api/v1/' in request.url:
            header = request.headers.get('x-requested-with')
            if header:
                self._dynamic_params['x_requested_with'] = header

    def _throttle(self):
        elapsed = time.monotonic() - self._last_request_at
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self._last_request_at = time.monotonic()

    def _request(self, method: str, url: str, headers: dict, params: dict) -> BrowserResponse:
        self._ensure_started()
        self._throttle()

        full_url = self._with_params(url, params)
        safe_headers = {k: str(v) for k, v in (headers or {}).items()
                        if k.lower() not in FORBIDDEN_HEADERS}
        try:
            result = self._page.evaluate(
                FETCH_JS, {'url': full_url, 'headers': safe_headers, 'method': method})
        except Exception as exc:
            raise RequestsConnectionError(f'Browser transport failed for {full_url}: {exc}') from exc

        return BrowserResponse(full_url, result['status'], result['body'], result['headers'])

    @staticmethod
    def _with_params(url: str, params: dict) -> str:
        if not params:
            return url
        from urllib.parse import urlencode
        query = urlencode({k: v for k, v in params.items() if v is not None})
        return f'{url}{"&" if "?" in url else "?"}{query}' if query else url

    def _teardown(self):
        for closer in (self._page, self._context, self._browser):
            try:
                closer.close()
            except Exception:
                pass
        try:
            self._playwright.stop()
        except Exception:
            pass
        self._started = False
