from src.Common.NetworkManager import NetworkManager
from src.Sofascore.SofascoreCrawler import SofascoreCrawler
from src.Sofascore.SofascoreParser import SofascoreParser
from src.Sofascore.SofascoreRequestFactory import SofascoreRequestFactory


class SofascoreContainer:

    def __init__(self, x_requested_with: str = None, next_build_id: str = None):
        self.network = NetworkManager()

        if x_requested_with is None or next_build_id is None:
            dynamic_params = self.network.fetch_dynamic_params()
            x_requested_with = x_requested_with or dynamic_params['x_requested_with']
            next_build_id = next_build_id or dynamic_params['next_build_id']

        self.factory = SofascoreRequestFactory(x_requested_with, next_build_id)
        self.parser = SofascoreParser()
        self.crawler = SofascoreCrawler(self.factory, self.parser)
