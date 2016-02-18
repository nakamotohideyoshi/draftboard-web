#
# sports/nfl/test.py

from test.classes import AbstractTest
from django.test import TestCase
from sports.nfl.models import Team, Player, Game, PlayerStats
from datetime import datetime
from django.utils import timezone
from dataden.watcher import OpLogObj
from sports.nfl.parser import PlayPbp
from ast import literal_eval

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

class TestPlayPbp(AbstractTest):
    """
    test parse an actual object which once came from dataden. (sanity check)

    there is a more generic test in sports.sport.tests
    """

    def setUp(self):
        # passing play has some player srids we might care about
        self.obj_str = """{'o': {'yfd': 10.0, 'distance': 'Short', 'yard_line': 31.0, 'direction': 'Left', 'formation': 'Shotgun', 'summary': '12-A.Rodgers incomplete. Intended for 17-D.Adams.', 'updated': '2015-09-29T00:32:01+00:00', 'type': 'pass', 'side': 'GB', 'down': 1.0, 'participants__list': [{'player': '0ce48193-e2fa-466e-a986-33f751add206'}, {'player': 'e7d6ae25-bf15-4660-8b37-c37716551de3'}], 'game__id': 'af51f745-7e7d-4762-864c-bac67c2db7e4', 'clock': '14:53', '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZGFmNTFmNzQ1LTdlN2QtNDc2Mi04NjRjLWJhYzY3YzJkYjdlNHBhcmVudF9saXN0X19pZGRyaXZlX19saXN0aWQwM2ZmZDlkOC05NGQ2LTQ2NzUtOWE1MC00ZGNjMWY5NDFhODE=', 'id': '03ffd9d8-94d6-4675-9a50-4dcc1f941a81', 'dd_updated__id': 1443486878736, 'parent_list__id': 'drive__list', 'sequence': 3.0, 'links__list': {'link__list': {'href': '/2015/REG/3/KC/GB/plays/03ffd9d8-94d6-4675-9a50-4dcc1f941a81.xml', 'type': 'application/xml', 'rel': 'summary'}}, 'parent_api__id': 'pbp'}, 'ns': 'nfl.play', 'ts': 1454659978}"""
        # kick play may not have player srdis we care about
        # self.data = literal_eval(self.obj_str) # convert to dict
        # self.oplog_obj = OpLogObj(self.data)

        # the field we will try to get a game srid from
        self.game_srid_field        = 'game__id'
        # a list of the game_srids we expect to get back (only 1 for this test)
        self.target_game_srids      = ['af51f745-7e7d-4762-864c-bac67c2db7e4']

        # the field name we will search for player srid(s)
        self.player_srid_field      = 'player'
        # the list of player srids we expect to find in this object
        self.target_player_srids    = ['0ce48193-e2fa-466e-a986-33f751add206']

        self.player_stats_class     = PlayerStats

    def __play_pbp_parse(self, str_oplog_obj):
        data        = literal_eval( str_oplog_obj )
        oplog_obj   = OpLogObj( data )
        play_pbp    = PlayPbp()
        play_pbp.parse( oplog_obj )
        return play_pbp

    def test_play_pbp_parse(self):
        """
        """
        play_pbp = self.__play_pbp_parse(self.obj_str)

        game_srids = play_pbp.get_srids_for_field(self.game_srid_field)
        self.assertIsInstance( game_srids, list )
        self.assertEquals( set(game_srids), set(self.target_game_srids) )
        self.assertEquals( len(set(game_srids)), 1 )

        # we are going to use the game_srid for a PlayerStats filter()
        game_srid = list(set(game_srids))[0]
        self.assertIsInstance( game_srid, str ) # the srid should be a string

        # we are going to use the list of player srids for the PlayerStats filter()
        player_srids = play_pbp.get_srids_for_field(self.player_srid_field)
        self.assertTrue( set(self.target_player_srids) <= set(player_srids) )

    def test_play_pbp_for_kick_play(self):
        """
        we dont really care about kick plays for scoring, so lets
        just see how the PlayPbp / pbp+stats linker handles this object
        """
        obj_str2 = """{'o': {'yfd': 10.0, 'yard_line': 35.0, 'id': '85345fbd-d2f1-43e7-885f-925370a9828e', 'summary': '5-C.Santos kicks 70 yards from KC 35. 88-T.Montgomery to GB 31 for 36 yards (30-J.Fleming).', 'updated': '2015-09-29T00:32:06+00:00', 'type': 'kick', 'side': 'KC', 'down': 1.0, 'participants__list': [{'player': 'd96ff17c-841a-4768-8e08-3a4cfcb7f717'}, {'player': '0c39e276-7a5b-448f-a696-532506f1035a'}, {'player': '349a994b-4b6d-42e6-a2fe-bdb3359b0a31'}], 'game__id': 'af51f745-7e7d-4762-864c-bac67c2db7e4', 'clock': '15:00', '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZGFmNTFmNzQ1LTdlN2QtNDc2Mi04NjRjLWJhYzY3YzJkYjdlNHBhcmVudF9saXN0X19pZGRyaXZlX19saXN0aWQ4NTM0NWZiZC1kMmYxLTQzZTctODg1Zi05MjUzNzBhOTgyOGU=', 'parent_api__id': 'pbp', 'dd_updated__id': 1443486878736, 'parent_list__id': 'drive__list', 'sequence': 2.0, 'links__list': {'link__list': {'href': '/2015/REG/3/KC/GB/plays/85345fbd-d2f1-43e7-885f-925370a9828e.xml', 'type': 'application/xml', 'rel': 'summary'}}}, 'ns': 'nfl.play', 'ts': 1454659978}"""

        play_pbp = self.__play_pbp_parse(obj_str2)

