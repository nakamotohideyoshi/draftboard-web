#
# sports/nba/tests.py

from ast import literal_eval
from dataden.watcher import OpLogObj, OpLogObjWrapper
from sports.sport.base_parser import DataDenSeasonSchedule
from sports.nba.parser import (
    SeasonSchedule,
    GameSchedule,
)
from test.classes import AbstractTest
from datetime import datetime
from django.utils import timezone
from sports.nba.parser import EventPbp
import sports.nba.models

class TestSeasonScheduleParser(AbstractTest):
    """
    tests sports.nba.parser.SeasonSchedule
    """

    def setUp(self):
        self.obj_str = """{'parent_api__id': 'schedule', 'year': 2015.0, 'games__list': {}, '_id': 'cGFyZW50X2FwaV9faWRzY2hlZHVsZWxlYWd1ZV9faWQ0MzUzMTM4ZC00YzIyLTQzOTYtOTVkOC01ZjU4N2QyZGYyNWNpZDUyOWJlZDM0LTVhOGQtNDZkNC05ZWVmLTExNGJkMTM0MDg2Nw==', 'id': '529bed34-5a8d-46d4-9eef-114bd1340867', 'type': 'PST', 'league__id': '4353138d-4c22-4396-95d8-5f587d2df25c', 'dd_updated__id': 1456944953067}"""
        self.season_parser = SeasonSchedule()

    def __validate_season(self, season_model, expected_season_year, expected_season_type):
        self.assertEquals(season_model.season_year, expected_season_year)
        self.assertEquals(season_model.season_type, expected_season_type)

    def test_pst_season(self):
        obj = literal_eval(self.obj_str)
        srid = obj.get('id') # the srid will be found in the 'id' field
        oplog_obj = OpLogObjWrapper('nba','season_schedule', obj)
        self.season_parser.parse( oplog_obj )
        season = sports.nba.models.Season.objects.get(srid=srid)
        self.__validate_season( season, 2015, 'pst' )

#
# requires: Season and Team(s) to work
# class TestGameScheduleParser(AbstractTest):
#     """
#     tests sports.nba.parser.GameSchedule -- the parser for sports.nba.models.Game objects
#     """
#
#     def setUp(self):
#         self.obj_str = """{'parent_list__id': 'games__list', 'broadcast__list': {'satellite': 216.0, 'network': 'NBA TV'}, '_id': 'cGFyZW50X2FwaV9faWRzY2hlZHVsZWxlYWd1ZV9faWQ0MzUzMTM4ZC00YzIyLTQzOTYtOTVkOC01ZjU4N2QyZGYyNWNzZWFzb24tc2NoZWR1bGVfX2lkY2Y0YzU0NDMtZTIyNC00Zjk3LTg2OTgtMjc5OTZhMzIyZmQzcGFyZW50X2xpc3RfX2lkZ2FtZXNfX2xpc3RpZGQ1M2JjZmUyLTY4YWMtNDE2Mi1hYzJlLWQ3ZjkzMzg3ZmJhNQ==', 'league__id': '4353138d-4c22-4396-95d8-5f587d2df25c', 'id': 'd53bcfe2-68ac-4162-ac2e-d7f93387fba5', 'coverage': 'full', 'status': 'closed', 'home': '583ecdfb-fb46-11e1-82cb-f4ce4684ea4c', 'away_team': '583ed102-fb46-11e1-82cb-f4ce4684ea4c', 'parent_api__id': 'schedule', 'dd_updated__id': 1456944907982, 'away': '583ed102-fb46-11e1-82cb-f4ce4684ea4c', 'scheduled': '2015-10-03T02:30:00+00:00', 'venue': '792ec100-691e-5e16-8ef8-79b2b6ee38ba', 'home_team': '583ecdfb-fb46-11e1-82cb-f4ce4684ea4c', 'season_schedule__id': 'cf4c5443-e224-4f97-8698-27996a322fd3'}"""
#         self.game_parser = GameSchedule()
#
#     def test_game_schedule_parse(self):
#         obj = literal_eval(self.obj_str)
#         srid = obj.get('id') # the game's srid
#         oplog_obj = OpLogObjWrapper('nba','game', obj)
#         self.game_parser.parse( oplog_obj )
#         game = sports.nba.models.Game.objects.get(srid=srid)

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
        self.assertTrue( set(self.target_player_srids) <= set(player_srids) )
