from django.test import TestCase
from .classes import SiteSportManager
# Create your tests here.
from test.classes import AbstractTest
from sports.models import SiteSport

class SportTest(AbstractTest):
    def setUp(self):
        pass

    def test_proper_init(self):
        ssm = SiteSportManager()

        arr = ssm.get_player_stats_class(self.get_site_sport('nfl'))
        self.assertEquals(1, len(arr))

        arr = ssm.get_player_stats_class(self.get_site_sport('nba'))
        self.assertEquals(1, len(arr))

        arr = ssm.get_player_stats_class(self.get_site_sport('nhl'))
        self.assertEquals(1, len(arr))

        arr = ssm.get_player_stats_class(self.get_site_sport('mlb'))
        self.assertEquals(2, len(arr))

    def get_site_sport(self, name):
        try:
            ss = SiteSport.objects.get( name=name )
        except SiteSport.DoesNotExist:
            ss = SiteSport()
            ss.name = name
            ss.save()
        return ss

