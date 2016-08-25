#
# tests.py

from test.classes import AbstractTest
from statscom.classes import (
    Stats,
)

class StatsUrlAuthParamTest(AbstractTest):

    def setUp(self):
        self.sport = 'nfl'

    def test_1(self):
        """ ensure some fundamental settings are set - dont validate for correctness here """
        stats = Stats(self.sport)
        self.assertIsNotNone(stats.stats_keys)
        self.assertIsNotNone(stats.url_base)
        self.assertIsNotNone(stats.response_format)

    def test_2(self):
        """ make sure we can build the url authentication params """
        stats = Stats(self.sport)
        url_auth_params = stats.get_url_auth_params()
        print(url_auth_params)
        self.assertIsNotNone(url_auth_params)

class StatsProjectionsWeekTest(AbstractTest):

    def setUp(self):
        self.sport = 'nfl'

    def test_1(self):
        stats = Stats(self.sport)