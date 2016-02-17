#
# sports/nba/tests.py

from test.classes import AbstractTest
from django.test import TestCase
from datetime import datetime
from django.utils import timezone
from dataden.watcher import OpLogObj
from sports.nba.parser import EventPbp
from ast import literal_eval
import sports.nba.models

class TestEventPbp(AbstractTest):
    """
    test parse an actual object which once came from dataden. (sanity check)

    there is a more generic test in sports.sport.tests
    """

    def setUp(self):
        self.obj_str = """{'o': {'parent_list__id': 'events__list', 'location__list': {'coord_x': 370.0, 'coord_y': 209.0}, 'parent_api__id': 'pbp', 'quarter__id': '715a0977-ab1e-4d13-9425-7d776b69615e', 'game__id': 'dcecc6c6-d6f8-40e2-a83c-d22953e55112', 'id': 'fb8be809-6822-439e-aaf0-e5d334ed25aa', 'dd_updated__id': 1454641970660, '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZGRjZWNjNmM2LWQ2ZjgtNDBlMi1hODNjLWQyMjk1M2U1NTExMnF1YXJ0ZXJfX2lkNzE1YTA5NzctYWIxZS00ZDEzLTk0MjUtN2Q3NzZiNjk2MTVlcGFyZW50X2xpc3RfX2lkZXZlbnRzX19saXN0aWRmYjhiZTgwOS02ODIyLTQzOWUtYWFmMC1lNWQzMzRlZDI1YWE=', 'updated': '2016-02-05T03:12:41+00:00', 'clock': '11:41', 'statistics__list': {'fieldgoal__list': {'team': '583ed056-fb46-11e1-82cb-f4ce4684ea4c', 'made': 'false', 'three_point_shot': 'true', 'player': '5382cf43-3a79-4a5a-a7fd-153906fe65dd', 'shot_type': 'jump shot'}}, 'event_type': 'threepointmiss', 'attribution': '583ed056-fb46-11e1-82cb-f4ce4684ea4c', 'description': 'Damian Lillard misses three point jump shot'}, 'ns': 'nba.event', 'ts': 1454659978}"""
        self.data = literal_eval(self.obj_str) # convert to dict
        self.oplog_obj = OpLogObj(self.data)

        # the field we will try to get a game srid from
        self.game_srid_field        = 'game__id'
        # a list of the game_srids we expect to get back (only 1 for this test)
        self.target_game_srids      = ['dcecc6c6-d6f8-40e2-a83c-d22953e55112']

        # the field name we will search for player srid(s)
        self.player_srid_field      = 'player'
        # the list of player srids we expect to find in this object
        self.target_player_srids    = ['5382cf43-3a79-4a5a-a7fd-153906fe65dd']

        self.player_stats_class     = sports.nba.models.PlayerStats

    def test_event_pbp_parse(self):
        """
        """
        event_pbp = EventPbp()
        event_pbp.parse(self.oplog_obj)

        game_srids = event_pbp.get_srids_for_field(self.game_srid_field)
        self.assertIsInstance( game_srids, list )
        self.assertEquals( set(game_srids), set(self.target_game_srids) )
        self.assertEquals( len(set(game_srids)), 1 )

        # we are going to use the game_srid for a PlayerStats filter()
        game_srid = list(set(game_srids))[0]
        self.assertIsInstance( game_srid, str ) # the srid should be a string

        # we are going to use the list of player srids for the PlayerStats filter()
        player_srids = event_pbp.get_srids_for_field(self.player_srid_field)
        self.assertEquals( set(player_srids), set(self.target_player_srids) )
