#
# sports/nfl/test.py

from test.classes import AbstractTest
from django.test import TestCase
from sports.nfl.models import Team, Player, Game
from datetime import datetime
from django.utils import timezone

class GameStatusChangedSignal(AbstractTest):

    def __create_team(self, alias, market):
        team = Team()
        team.srid               = 'test-srid-' + alias
        team.alias              = alias
        team.market             = market

        team.srid_league        = '4353138d-4c22-4396-95d8-5f587d2df25c'
        team.srid_conference    = '3960cfac-7361-4b30-bc25-8d393de6f62f'
        team.srid_division      = '54dc7348-c1d2-40d8-88b3-c4c0138e085d'
        team.save()
        return team

    def setUp(self):
        self.SCHEDULED = 'scheduled' # the default game status
        self.COMPLETE  = 'complete'  # made up - does not actually reflect a real status, necessarily

        self.home = self.__create_team('alias-home', 'market-home')
        self.away = self.__create_team('alias-away', 'market-away')

        self.game = Game()
        self.game.srid      = '%s--test--%s' % (self.away.srid, self.home.srid)

        self.game.home      = self.home
        self.game.srid_home = self.home.srid

        self.game.away      = self.away
        self.game.srid_away = self.away.srid

        self.game.title         = 'testing game for status change signal'
        self.game.weather_json  = '{}'
        self.game.start         = timezone.now()

        self.game.status        = self.SCHEDULED

        self.game.save()

    def test_signal_sent_on_game_status_changed(self):
        self.game.status = self.COMPLETE
        self.game.save()

class DstPlayerCreation(AbstractTest):
    """
    Ensure that the nfl teams DST player objects get created
    when a new team is created.
    """
    def setUp(self):
        self.srid_team  = 'TEST'            # default team srid/alias
        self.player     = None

    def create_team(self, srid):
        t = Team()
        t.srid          = srid
        t.srid_venue    = srid + 'venue'    # doesnt have to be real for this test
        t.name          = 'Test Team'       # doesnt have to be valid
        t.alias         = srid              # alias is the id for nfl teams
        t.save() # this save should create dst Player object via signal
        return t

    def get_dst_player(self, srid_team):
        return Player.objects.get(srid=srid_team)

    def test_dst_player_is_created_when_new_team_is_saved(self):
        # it shouldnt exist now, and SHOULD throw DoesNotExist
        self.assertRaises(Player.DoesNotExist, lambda: self.get_dst_player(srid_team=self.srid_team) )

        # now create the Team object, and check again
        t = self.create_team( self.srid_team )
        try:
            self.player = self.get_dst_player( srid_team=self.srid_team )
        except:
            self.player = None

        self.assertIsNotNone( self.player )
        self.assertEquals( self.srid_team, t.srid )