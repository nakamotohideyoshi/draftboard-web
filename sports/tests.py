from django.test import TestCase
from .classes import SiteSportManager
# Create your tests here.
from test.classes import AbstractTest
class SportTest(AbstractTest):
    def setUp(self):
        pass

    def test_proper_init(self):
        ssm = SiteSportManager()

        arr = ssm.get_player_stats_class('nfl')
        self.assertEquals(1, len(arr))

        arr = ssm.get_player_stats_class('nba')
        self.assertEquals(1, len(arr))

        arr = ssm.get_player_stats_class('nhl')
        self.assertEquals(1, len(arr))

        arr = ssm.get_player_stats_class('mlb')
        self.assertEquals(2, len(arr))


