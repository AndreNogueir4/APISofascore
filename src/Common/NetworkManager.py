import requests
from playwright.sync_api import sync_playwright


class NetworkManager:

    def __init__(self, timeout: float = 10.0):
        self.timeout = timeout
        self.session = requests.Session()

    def get(self, url: str, headers: dict = None, params: dict = None) -> requests.Response:
        return self.session.get(url, headers=headers, params=params, timeout=self.timeout)

    def head(self, url: str, headers: dict = None, params: dict = None) -> requests.Response:
        return self.session.head(url, headers=headers, params=params, timeout=self.timeout)

    def close(self):
        self.session.close()

    def fetch_dynamic_params(self, url: str = 'https://www.sofascore.com/pt', timeout: float = 20.0) -> dict:
        params = {'x_requested_with': None, 'next_build_id': None}

        def handle_request(request):
            if params['x_requested_with'] is None and '/api/v1/' in request.url:
                header = request.headers.get('x-requested-with')
                if header:
                    params['x_requested_with'] = header

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            page.on('request', handle_request)
            response = page.goto(url, wait_until='networkidle', timeout=timeout * 1000)

            if response is None or not response.ok:
                status = response.status if response else 'no response'
                browser.close()
                raise RuntimeError(f'Failed to load {url} via Playwright (status: {status}).')

            params['next_build_id'] = page.evaluate("() => window.__NEXT_DATA__?.buildId")
            user_agent = page.evaluate('() => navigator.userAgent')
            cookies = context.cookies()
            browser.close()

        if not params['x_requested_with'] or not params['next_build_id']:
            raise RuntimeError(f'Could not extract dynamic params from the page: {params}')

        self.session.headers['User-Agent'] = user_agent
        for cookie in cookies:
            self.session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'], path=cookie['path'])

        return params
