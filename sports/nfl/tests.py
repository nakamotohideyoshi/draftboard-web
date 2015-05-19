#
# sports/nfl/test.py

from django.test import TestCase
from sports.nfl.models import Team, Player

class DstPlayerCreation(TestCase):

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