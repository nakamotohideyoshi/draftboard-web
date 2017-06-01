#
# sports/nhl/tests.py

from ast import literal_eval
from test.classes import AbstractTest
import sports.nhl.models
from dataden.watcher import OpLogObj, OpLogObjWrapper
from sports.nhl.parser import (
    SeasonSchedule,
    GameSchedule,
    PbpEventParser,
    TeamHierarchy,
)

class TestSeasonScheduleParser(AbstractTest):
    """
    tests sports.nhl.parser.SeasonSchedule
    """

    def setUp(self):
        super().setUp()
        self.obj_str = """{'id': '350e419b-ffd6-49e3-957a-13626d94391f', 'games__list': {}, 'league__id': 'fd560107-a85b-4388-ab0d-655ad022aff7', '_id': 'cGFyZW50X2FwaV9faWRzY2hlZHVsZWxlYWd1ZV9faWRmZDU2MDEwNy1hODViLTQzODgtYWIwZC02NTVhZDAyMmFmZjdpZDM1MGU0MTliLWZmZDYtNDllMy05NTdhLTEzNjI2ZDk0MzkxZg==', 'type': 'PST', 'parent_api__id': 'schedule', 'year': 2015.0, 'dd_updated__id': 1456973805211}"""
        self.season_parser = SeasonSchedule()

    def __validate_season(self, season_model, expected_season_year, expected_season_type):
        self.assertEquals(season_model.season_year, expected_season_year)
        self.assertEquals(season_model.season_type, expected_season_type)

    def test_pst_season(self):
        obj = literal_eval(self.obj_str)
        srid = obj.get('id') # the srid will be found in the 'id' field
        oplog_obj = OpLogObjWrapper('nhl','season_schedule', obj)
        self.season_parser.parse( oplog_obj )
        season = sports.nhl.models.Season.objects.get(srid=srid)
        self.__validate_season( season, 2015, 'pst' )

class TestGameScheduleParser(AbstractTest):
    """
    tests sports.nhl.parser.GameSchedule -- the parser for sports.nhl.models.Game objects

    effectively tests the TeamHierarchy parser too
    """

    def setUp(self):
        super().setUp()
        self.sport = 'nhl'
        self.season_str = """{'parent_api__id': 'schedule', 'league__id': 'fd560107-a85b-4388-ab0d-655ad022aff7', 'games__list': [{'game': '0a5e53db-e150-4fef-919d-c8ae5dc68453'}, {'game': '9cbfad48-cc50-47f4-86d5-5d03a496e856'}, {'game': 'af0d964a-8720-4880-8cff-54fc98840626'}, {'game': 'f9a0088c-fce4-41ea-8825-3711082e893e'}, {'game': '22129c34-bca0-48ab-a31e-df9b18ac178b'}, {'game': '2a874b94-43f2-492e-9ceb-38e9eb2c2261'}], 'dd_updated__id': 1456973782980, 'id': '9618b7b0-2a86-486d-b256-88748191f854', 'year': 2015.0, '_id': 'cGFyZW50X2FwaV9faWRzY2hlZHVsZWxlYWd1ZV9faWRmZDU2MDEwNy1hODViLTQzODgtYWIwZC02NTVhZDAyMmFmZjdpZDk2MThiN2IwLTJhODYtNDg2ZC1iMjU2LTg4NzQ4MTkxZjg1NA==', 'type': 'REG'}"""
        self.away_team_str = """{'parent_api__id': 'hierarchy', 'market': 'San Jose', 'league__id': 'fd560107-a85b-4388-ab0d-655ad022aff7', 'conference__id': '64901512-9ca9-4bea-aa80-16dbcbdae230', 'division__id': '17101b65-e8b9-4cda-a963-eea874aed81f', 'alias': 'SJ', 'venue': '1da65282-af4c-4b81-a9de-344b76bb20b0', 'id': '44155909-0f24-11e2-8525-18a905767e44', 'dd_updated__id': 1456973147878, 'name': 'Sharks', '_id': 'cGFyZW50X2FwaV9faWRoaWVyYXJjaHlsZWFndWVfX2lkZmQ1NjAxMDctYTg1Yi00Mzg4LWFiMGQtNjU1YWQwMjJhZmY3Y29uZmVyZW5jZV9faWQ2NDkwMTUxMi05Y2E5LTRiZWEtYWE4MC0xNmRiY2JkYWUyMzBkaXZpc2lvbl9faWQxNzEwMWI2NS1lOGI5LTRjZGEtYTk2My1lZWE4NzRhZWQ4MWZpZDQ0MTU1OTA5LTBmMjQtMTFlMi04NTI1LTE4YTkwNTc2N2U0NA=='}"""
        self.home_team_str = """{'parent_api__id': 'hierarchy', 'market': 'Los Angeles', 'league__id': 'fd560107-a85b-4388-ab0d-655ad022aff7', 'conference__id': '64901512-9ca9-4bea-aa80-16dbcbdae230', 'division__id': '17101b65-e8b9-4cda-a963-eea874aed81f', 'alias': 'LA', 'venue': 'dec253d4-68df-470b-b8fc-d663a7fa4704', 'id': '44151f7a-0f24-11e2-8525-18a905767e44', 'dd_updated__id': 1456973147878, 'name': 'Kings', '_id': 'cGFyZW50X2FwaV9faWRoaWVyYXJjaHlsZWFndWVfX2lkZmQ1NjAxMDctYTg1Yi00Mzg4LWFiMGQtNjU1YWQwMjJhZmY3Y29uZmVyZW5jZV9faWQ2NDkwMTUxMi05Y2E5LTRiZWEtYWE4MC0xNmRiY2JkYWUyMzBkaXZpc2lvbl9faWQxNzEwMWI2NS1lOGI5LTRjZGEtYTk2My1lZWE4NzRhZWQ4MWZpZDQ0MTUxZjdhLTBmMjQtMTFlMi04NTI1LTE4YTkwNTc2N2U0NA=='}"""
        self.game_str = """{'parent_api__id': 'schedule', 'season_schedule__id': '9618b7b0-2a86-486d-b256-88748191f854', 'away': '44155909-0f24-11e2-8525-18a905767e44', 'scheduled': '2015-10-08T02:30:00+00:00', 'home_team': '44151f7a-0f24-11e2-8525-18a905767e44', 'parent_list__id': 'games__list', 'coverage': 'full', 'home': '44151f7a-0f24-11e2-8525-18a905767e44', 'status': 'closed', 'dd_updated__id': 1456973782980, '_id': 'cGFyZW50X2FwaV9faWRzY2hlZHVsZWxlYWd1ZV9faWRmZDU2MDEwNy1hODViLTQzODgtYWIwZC02NTVhZDAyMmFmZjdzZWFzb24tc2NoZWR1bGVfX2lkOTYxOGI3YjAtMmE4Ni00ODZkLWIyNTYtODg3NDgxOTFmODU0cGFyZW50X2xpc3RfX2lkZ2FtZXNfX2xpc3RpZGY5YTAwODhjLWZjZTQtNDFlYS04ODI1LTM3MTEwODJlODkzZQ==', 'id': 'f9a0088c-fce4-41ea-8825-3711082e893e', 'broadcast__list': {'network': 'NBCSN', 'satellite': 220.0}, 'away_team': '44155909-0f24-11e2-8525-18a905767e44', 'league__id': 'fd560107-a85b-4388-ab0d-655ad022aff7', 'venue': 'dec253d4-68df-470b-b8fc-d663a7fa4704'}"""

        self.season_parser = SeasonSchedule()
        self.away_team_parser = TeamHierarchy()
        self.home_team_parser = TeamHierarchy()
        self.game_parser = GameSchedule()

    def test_game_schedule_parse(self):
        """
        as a prerequisite, parse the seasonschedule, and both home & away teams
        """
        # parse the season_schedule obj
        season_oplog_obj = OpLogObjWrapper(self.sport,'season_schedule',literal_eval(self.season_str))
        self.season_parser.parse( season_oplog_obj )
        self.assertEquals( 1, sports.nhl.models.Season.objects.filter(season_year=2015,season_type='reg').count() ) # should have parsed 1 thing

        away_team_oplog_obj = OpLogObjWrapper(self.sport,'team',literal_eval(self.away_team_str))
        self.away_team_parser.parse( away_team_oplog_obj )
        self.assertEquals( 1, sports.nhl.models.Team.objects.all().count() ) # should be 1 team in there now

        home_team_oplog_obj = OpLogObjWrapper(self.sport,'team',literal_eval(self.home_team_str))
        self.home_team_parser.parse( home_team_oplog_obj )
        self.assertEquals( 2, sports.nhl.models.Team.objects.all().count() ) # should be 2 teams in there now

        # now attempt to parse the game
        game_oplog_obj = OpLogObjWrapper(self.sport,'game',literal_eval(self.game_str))
        self.game_parser.parse( game_oplog_obj )
        self.assertEquals( 1, sports.nhl.models.Game.objects.all().count() )

class TestEventPbp(AbstractTest):
    """
    test parse an actual object which once came from dataden. (sanity check)

    there is a more generic test in sports.sport.tests
    """

    def setUp(self):
        super().setUp()
        self.obj_str = """{'o': {'parent_list__id': 'events__list', 'description': 'Kris Letang shot blocked by Tyler Seguin', 'id': '6c55cd4a-ceef-4a16-ad25-92295246e1b0', 'event_type': 'shotmissed', '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDg2NDViYzQ0LWEyYmYtNDkyYi1hMGU3LTg1MDAyYWM2OTc4Y3BlcmlvZF9faWQ4NTY4OGVmZS0zN2YxLTRjOTMtYmE3MS00YzA1NmQ2MTk5NzJwYXJlbnRfbGlzdF9faWRldmVudHNfX2xpc3RpZDZjNTVjZDRhLWNlZWYtNGExNi1hZDI1LTkyMjk1MjQ2ZTFiMA==', 'zone': 'offensive', 'dd_updated__id': 1444379408289, 'statistics__list': {'block__list': {'player': '42ea7555-0f24-11e2-8525-18a905767e44', 'strength': 'even', 'team': '44157522-0f24-11e2-8525-18a905767e44'}, 'attemptblocked__list': {'player': '4342422b-0f24-11e2-8525-18a905767e44', 'strength': 'even', 'team': '4417b7d7-0f24-11e2-8525-18a905767e44'}}, 'parent_api__id': 'pbp', 'period__id': '85688efe-37f1-4c93-ba71-4c056d619972', 'clock': '5:47', 'attribution': '4417b7d7-0f24-11e2-8525-18a905767e44', 'updated': '2015-10-09T01:12:33+00:00', 'location__list': {'coord_x': 1683.0, 'coord_y': 282.0}, 'game__id': '8645bc44-a2bf-492b-a0e7-85002ac6978c'}, 'ns': 'nhl.event', 'ts': 1454659978}"""
        self.data = literal_eval(self.obj_str) # convert to dict
        self.oplog_obj = OpLogObj(self.data)

        # the field we will try to get a game srid from
        self.game_srid_field        = 'game__id'
        # a list of the game_srids we expect to get back (only 1 for this test)
        self.target_game_srids      = ['8645bc44-a2bf-492b-a0e7-85002ac6978c']

        # the field name we will search for player srid(s)
        self.player_srid_field      = 'player'
        # the list of player srids we expect to find in this object
        self.target_player_srids    = ['4342422b-0f24-11e2-8525-18a905767e44']

        self.player_stats_class     = sports.nhl.models.PlayerStats

    def test_event_pbp_parse(self):
        """
        """
        event_pbp = PbpEventParser()
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
        #print('player_srids', player_srids)
        self.assertTrue( set(self.target_player_srids) <= set(player_srids) )
