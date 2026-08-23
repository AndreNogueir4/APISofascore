from src.Common.NetworkManager import NetworkManager
from src.Sofascore.SofascoreCrawler import SofascoreCrawler
from src.Sofascore.SofascoreParser import SofascoreParser
from src.Sofascore.SofascoreRequestFactory import SofascoreRequestFactory


class SofascoreContainer:

    def __init__(self, x_requested_with: str = '2589dc', next_build_id: str = 'ht9wCJpl-6PQSlY85cZ-r'):
        self.network = NetworkManager()
        self.factory = SofascoreRequestFactory(x_requested_with, next_build_id)
        self.parser = SofascoreParser()
        self.crawler = SofascoreCrawler(self.factory, self.parser)
