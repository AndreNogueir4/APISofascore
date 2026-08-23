import requests


class NetworkManager:
    """Wrapper fino sobre requests.Session — só o transporte HTTP básico.

    Retry/backoff/rate-limit ficam fora de escopo aqui (ver crawler_sofascore.md,
    Passo 2) — essa classe só sabe abrir conexão e devolver a Response crua.
    """

    def __init__(self, timeout: float = 10.0):
        self.timeout = timeout
        self.session = requests.Session()

    def get(self, url: str, headers: dict = None, params: dict = None) -> requests.Response:
        return self.session.get(url, headers=headers, params=params, timeout=self.timeout)

    def head(self, url: str, headers: dict = None, params: dict = None) -> requests.Response:
        return self.session.head(url, headers=headers, params=params, timeout=self.timeout)

    def close(self):
        self.session.close()
