from ast import literal_eval

from model_mommy import mommy

import sports.nba.models
from dataden.watcher import OpLogObj, OpLogObjWrapper
from sports.nba.parser import (
    SeasonSchedule,
    GameSchedule,
    TeamHierarchy,
    PbpEventParser,
    GameBoxscoreParser,
    PlayerStatsParser,
)
from test.classes import AbstractTest
from django.core.cache import cache


class TestSeasonScheduleParser(AbstractTest):
    """
    tests sports.nba.parser.SeasonSchedule
    """

    def setUp(self):
        super().setUp()
        # ignoring E501 line too long PEP8 warning
        self.obj_str = """{'parent_api__id': 'schedule', 'year': 2015.0, 'games__list': {}, '_id': 'cGFyZW50X2FwaV9faWRzY2hlZHVsZWxlYWd1ZV9faWQ0MzUzMTM4ZC00YzIyLTQzOTYtOTVkOC01ZjU4N2QyZGYyNWNpZDUyOWJlZDM0LTVhOGQtNDZkNC05ZWVmLTExNGJkMTM0MDg2Nw==', 'id': '529bed34-5a8d-46d4-9eef-114bd1340867', 'type': 'PST', 'league__id': '4353138d-4c22-4396-95d8-5f587d2df25c', 'dd_updated__id': 1456944953067}"""  # noqa
        self.season_parser = SeasonSchedule()

    def __validate_season(self, season_model, expected_season_year, expected_season_type):
        self.assertEquals(season_model.season_year, expected_season_year)
        self.assertEquals(season_model.season_type, expected_season_type)

    def test_pst_season(self):
        obj = literal_eval(self.obj_str)
        srid = obj.get('id')  # the srid will be found in the 'id' field
        oplog_obj = OpLogObjWrapper('nba', 'season_schedule', obj)
        self.season_parser.parse(oplog_obj)
        season = sports.nba.models.Season.objects.get(srid=srid)
        self.__validate_season(season, 2015, 'pst')


class TestGameScheduleParser(AbstractTest):
    """
    tests sports.nba.parser.GameSchedule -- the parser for sports.nba.models.Game objects
    """

    def setUp(self):
        super().setUp()
        self.sport = 'nba'

        # ignoring E501 line too long PEP8 warnings
        self.season_str = """{'parent_api__id': 'schedule', 'year': 2015.0, 'games__list': [{'game': '3950bf88-7d69-45cb-957f-9b73ffca1d6e'}, {'game': 'f00b4cf7-4722-4ffb-8d6a-9d378f370228'}], '_id': 'cGFyZW50X2FwaV9faWRzY2hlZHVsZWxlYWd1ZV9faWQ0MzUzMTM4ZC00YzIyLTQzOTYtOTVkOC01ZjU4N2QyZGYyNWNpZDY5ODU5MGMyLTM1NzktNGQ0ZS1hOTMxLTNkNmRmZjQyN2VlMg==', 'id': '698590c2-3579-4d4e-a931-3d6dff427ee2', 'type': 'REG', 'league__id': '4353138d-4c22-4396-95d8-5f587d2df25c', 'dd_updated__id': 1456944928793}"""  # noqa
        self.away_team_str = """{'parent_api__id': 'hierarchy', 'market': 'Cleveland', 'league__id': '4353138d-4c22-4396-95d8-5f587d2df25c', 'conference__id': '3960cfac-7361-4b30-bc25-8d393de6f62f', 'division__id': 'f3aaf23a-1ceb-46ef-8fef-9403692e801b', 'alias': 'CLE', 'venue': '42cddf7a-0e1f-5f91-ae6f-c620582fdb01', 'id': '583ec773-fb46-11e1-82cb-f4ce4684ea4c', 'dd_updated__id': 1456973069473, 'name': 'Cavaliers', '_id': 'cGFyZW50X2FwaV9faWRoaWVyYXJjaHlsZWFndWVfX2lkNDM1MzEzOGQtNGMyMi00Mzk2LTk1ZDgtNWY1ODdkMmRmMjVjY29uZmVyZW5jZV9faWQzOTYwY2ZhYy03MzYxLTRiMzAtYmMyNS04ZDM5M2RlNmY2MmZkaXZpc2lvbl9faWRmM2FhZjIzYS0xY2ViLTQ2ZWYtOGZlZi05NDAzNjkyZTgwMWJpZDU4M2VjNzczLWZiNDYtMTFlMS04MmNiLWY0Y2U0Njg0ZWE0Yw=='}"""  # noqa
        self.home_team_str = """{'parent_api__id': 'hierarchy', 'market': 'Chicago', 'league__id': '4353138d-4c22-4396-95d8-5f587d2df25c', 'conference__id': '3960cfac-7361-4b30-bc25-8d393de6f62f', 'division__id': 'f3aaf23a-1ceb-46ef-8fef-9403692e801b', 'alias': 'CHI', 'venue': '38911649-acfd-551a-949b-68f0fcaa44e7', 'id': '583ec5fd-fb46-11e1-82cb-f4ce4684ea4c', 'dd_updated__id': 1456973069473, 'name': 'Bulls', '_id': 'cGFyZW50X2FwaV9faWRoaWVyYXJjaHlsZWFndWVfX2lkNDM1MzEzOGQtNGMyMi00Mzk2LTk1ZDgtNWY1ODdkMmRmMjVjY29uZmVyZW5jZV9faWQzOTYwY2ZhYy03MzYxLTRiMzAtYmMyNS04ZDM5M2RlNmY2MmZkaXZpc2lvbl9faWRmM2FhZjIzYS0xY2ViLTQ2ZWYtOGZlZi05NDAzNjkyZTgwMWJpZDU4M2VjNWZkLWZiNDYtMTFlMS04MmNiLWY0Y2U0Njg0ZWE0Yw=='}"""  # noqa
        self.game_str = """{'parent_api__id': 'schedule', 'season_schedule__id': '698590c2-3579-4d4e-a931-3d6dff427ee2', 'away': '583ec773-fb46-11e1-82cb-f4ce4684ea4c', 'scheduled': '2015-10-28T00:00:00+00:00', 'home_team': '583ec5fd-fb46-11e1-82cb-f4ce4684ea4c', 'parent_list__id': 'games__list', 'coverage': 'full', 'home': '583ec5fd-fb46-11e1-82cb-f4ce4684ea4c', 'status': 'closed', 'dd_updated__id': 1456973746005, '_id': 'cGFyZW50X2FwaV9faWRzY2hlZHVsZWxlYWd1ZV9faWQ0MzUzMTM4ZC00YzIyLTQzOTYtOTVkOC01ZjU4N2QyZGYyNWNzZWFzb24tc2NoZWR1bGVfX2lkNjk4NTkwYzItMzU3OS00ZDRlLWE5MzEtM2Q2ZGZmNDI3ZWUycGFyZW50X2xpc3RfX2lkZ2FtZXNfX2xpc3RpZGYwMGI0Y2Y3LTQ3MjItNGZmYi04ZDZhLTlkMzc4ZjM3MDIyOA==', 'id': 'f00b4cf7-4722-4ffb-8d6a-9d378f370228', 'broadcast__list': {'network': 'TNT', 'satellite': 245.0}, 'away_team': '583ec773-fb46-11e1-82cb-f4ce4684ea4c', 'league__id': '4353138d-4c22-4396-95d8-5f587d2df25c', 'venue': '38911649-acfd-551a-949b-68f0fcaa44e7'}"""  # noqa

        self.season_parser = SeasonSchedule()
        self.away_team_parser = TeamHierarchy()
        self.home_team_parser = TeamHierarchy()
        self.game_parser = GameSchedule()

    def test_game_schedule_parse(self):
        """
        as a prerequisite, parse the seasonschedule, and both home & away teams

        effectively tests the TeamHierarchy parser too
        """
        # parse the season_schedule obj
        season_oplog_obj = OpLogObjWrapper(
            self.sport, 'season_schedule', literal_eval(self.season_str))
        self.season_parser.parse(season_oplog_obj)
        self.assertEquals(1, sports.nba.models.Season.objects.filter(
            season_year=2015, season_type='reg').count())  # should have parsed 1 thing

        away_team_oplog_obj = OpLogObjWrapper(
            self.sport, 'team', literal_eval(self.away_team_str))
        self.away_team_parser.parse(away_team_oplog_obj)
        # should be 1 team in there now
        self.assertEquals(1, sports.nba.models.Team.objects.all().count())

        home_team_oplog_obj = OpLogObjWrapper(
            self.sport, 'team', literal_eval(self.home_team_str))
        self.home_team_parser.parse(home_team_oplog_obj)
        # should be 2 teams in there now
        self.assertEquals(2, sports.nba.models.Team.objects.all().count())

        # now attempt to parse the game
        game_oplog_obj = OpLogObjWrapper(
            self.sport, 'game', literal_eval(self.game_str))
        self.game_parser.parse(game_oplog_obj)
        self.assertEquals(1, sports.nba.models.Game.objects.all().count())


# Okay, if you want to run this, you need to comment out
# the `self.update_boxscore_data_in_game(data)` in `sports.nba.parser.GameBoxscoreParser.send()
# This is because the update is looking for the game to already
# exist in the database, but we haven't set that up yet for this test

class TestGameBoxscoreParser(AbstractTest):
    """ tests the send() part only """

    def setUp(self):
        self.parser = GameBoxscoreParser()

    def __parse_and_send(self, unwrapped_obj, target):
        parts = target[0].split('.')
        oplog_obj = OpLogObjWrapper(parts[0], parts[1], unwrapped_obj)
        self.parser.parse(oplog_obj, target=target)
        self.parser.send()

    def test_parse(self):
        sport_db = 'nba'
        parent_api = 'boxscores'

        # I believe This is a typical game boxscore object we get from dataden.
        data = {
            'away_team': '583ecf50-fb46-11e1-82cb-f4ce4684ea4c',
            '_id': 'cGFyZW50X2FwaV9faWRib3hzY29yZXNpZDkyMTkzMWQ2LWYxMzctNGJhNy1iMjM3LTYwOTU3YTdkZmY5Yg==',
            'quarter': 4.0,
            'parent_api__id': 'boxscores',
            'dd_updated__id': 1482384853598,
            'teams': [
                {'team': '583ed056-fb46-11e1-82cb-f4ce4684ea4c'},
                {'team': '583ecf50-fb46-11e1-82cb-f4ce4684ea4c'}
            ],
            'coverage': 'full',
            'home_team': '583ed056-fb46-11e1-82cb-f4ce4684ea4c',
            'id': '921931d6-f137-4ba7-b237-60957a7dff9b',
            'xmlns': 'http://feed.elasticstats.com/schema/basketball/game-v2.0.xsd',
            'clock': '00:00',
            'scheduled': '2016-12-22T03:00:00+00:00',
            'neutral_site': 'false',
            'status': 'inprogress'
        }

        # Create a nba.Team models
        mommy.make(
            sports.nba.models.Team,
            srid=data['home_team']
        )
        mommy.make(
            sports.nba.models.Team,
            srid=data['away_team']
        )
        # Create a Game model so this boxcore can be parsed.
        mommy.make(
            sports.nba.models.Game,
            srid=data['id']
        )
        # Parse it!
        self.__parse_and_send(data, (sport_db + '.' + 'game', parent_api))


class TestEventPbp(AbstractTest):
    """
    test parse an actual object which once came from dataden. (sanity check)

    there is a more generic test in sports.sport.tests
    """

    def tearDown(self):
        cache.clear()
        super().tearDown()

    def setUp(self):
        cache.clear()
        super().setUp()
        self.dataden_obj = {'o': {
            'ns': 'nba.event',
            'ts': 1454659978,
            'event_type': 'threepointmiss',
            'attribution': '583ed056-fb46-11e1-82cb-f4ce4684ea4c',
            'description': 'Damian Lillard misses three point jump shot',
            'parent_list__id': 'events__list',
            'location__list': {'coord_x': 370.0,
                               'coord_y': 209.0},
            'parent_api__id': 'pbp',
            'quarter__id': '715a0977-ab1e-4d13-9425-7d776b69615e',
            'game__id': 'dcecc6c6-d6f8-40e2-a83c-d22953e55112',
            'id': 'fb8be809-6822-439e-aaf0-e5d334ed25aa',
            'dd_updated__id': 1454641970660,
            '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZGRjZWNjNmM2LWQ2ZjgtNDBlMi1hODNjLWQy',
            'updated': '2016-02-05T03:12:41+00:00',
            'clock': '11:41',
            'statistics__list': {
                'fieldgoal__list': {
                    'team': '583ed056-fb46-11e1-82cb-f4ce4684ea4c',
                    'made': 'false',
                    'three_point_shot': 'true',
                    'player': '5382cf43-3a79-4a5a-a7fd-153906fe65dd',
                    'shot_type': 'jump shot'
                }
            },
        }
        }

        # create the OpLogOjb wrapper. This is what the parse is expecting.
        self.oplog_object = OpLogObj(self.dataden_obj)
        # get the raw event data.
        self.event_data = self.oplog_object.get_o()

        # the field we will try to get a game srid from
        self.game_srid_field = 'game__id'
        # a list of the game_srids we expect to get back (only 1 for this test)
        self.target_game_srids = ['dcecc6c6-d6f8-40e2-a83c-d22953e55112']

        # the field name we will search for player srid(s)
        self.player_srid_field = 'player'
        # the list of player srids we expect to find in this object
        self.target_player_srids = ['5382cf43-3a79-4a5a-a7fd-153906fe65dd']

        self.player_stats_class = sports.nba.models.PlayerStats

    def test_event_pbp_parse(self):
        """
        This test only parses, no assertions. I guess it makes sure parsing
        doesn't blow up.
        """
        parser = PbpEventParser()
        parser.parse(self.oplog_object)

        game_srids = parser.get_srids_for_field(self.game_srid_field)
        self.assertIsInstance(game_srids, list)
        self.assertEquals(set(game_srids), set(self.target_game_srids))
        self.assertEquals(len(set(game_srids)), 1)

        # we are going to use the game_srid for a PlayerStats filter()
        game_srid = list(set(game_srids))[0]
        self.assertIsInstance(game_srid, str)  # the srid should be a string

        # we are going to use the list of player srids for the PlayerStats
        # filter()
        player_srids = parser.get_srids_for_field(self.player_srid_field)
        self.assertTrue(set(self.target_player_srids) <= set(player_srids))
        parser.send()

    def test_player_names(self):
        """
        Test that player names are being added to the parser output data.
        :return: 
        """

        player = mommy.make(
            sports.nba.models.Player,
            srid=self.event_data['statistics__list']['fieldgoal__list']['player'],
            make_m2m=True,
            first_name="Damian",
            last_name="Lillard",
        )

        player_stats = mommy.make(
            sports.nba.models.PlayerStats,
            srid_game=self.event_data['game__id'],
            srid_player=player.srid,
            make_m2m=True,
        )
        player_stats.player = player
        player_stats.save()

        self.assertEqual(
            player_stats.player.srid,
            self.event_data['statistics__list']['fieldgoal__list']['player']
        )

        parser = PbpEventParser()
        parser.parse(self.oplog_object)

        # parser.send()
        sent_data = parser.get_send_data()

        # Ensure that both the first and last names are set, match the player's
        # and are not empty.
        self.assertEqual(
            sent_data['stats'][0]['first_name'],
            player.first_name
        )
        self.assertNotEqual(
            sent_data['stats'][0]['first_name'],
            ''
        )

        self.assertEqual(
            sent_data['stats'][0]['last_name'],
            player.last_name
        )
        self.assertNotEqual(
            sent_data['stats'][0]['last_name'],
            ''
        )

    def test_game_info(self):
        """
        Make sure that game info is being added into the 'game' attribute of the pbp. 
        """
        # Create some teams and a game.
        home_team = mommy.make(
            sports.nba.models.Team,
            alias="DEN"
        )
        away_team = mommy.make(
            sports.nba.models.Team,
            alias="SLC"
        )
        game = mommy.make(
            sports.nba.models.Game,
            srid=self.event_data['game__id'],
            srid_home=home_team.srid,
            home=home_team,
            srid_away=away_team.srid,
            away=away_team,
            make_m2m=True,
        )

        # Parse the event
        parser = PbpEventParser()
        parser.parse(self.oplog_object)

        parser.send()
        sent_data = parser.get_send_data()

        # ensure the teams were added to the event as it was parsed and sent.
        self.assertEqual(
            sent_data['game']['away']['alias'],
            away_team.alias
        )
        self.assertEqual(
            sent_data['game']['home']['alias'],
            home_team.alias
        )


class TestPlayerStats(AbstractTest):
    """
    Test the PlayerStats Parser. It should take an update object from mongo and create a PlayerStat
    from it.
    """

    def setUp(self):
        super().setUp()
        self.parser = PlayerStatsParser()
        # some info needed for the parser
        self.sport_db = 'nba'
        self.parent_api = 'stats'

        # An example nba.player stats object from mongo.
        self.obj = {
            'team__id': '583ec97e-fb46-11e1-82cb-f4ce4684ea4c',
            'dd_updated__id': 1482278107385,
            'first_name': 'Michael',
            'id': 'ea8a18e4-1341-48f1-b75d-5bbac8d789d4',
            'position': 'F',
            'game__id': '7a4cc8a0-1ab1-4f76-8d7c-7b1017518c8d',
            'parent_api__id': 'stats',
            '_id': 'cGFyZW50X2FwaV9faWRzdGF0c2dhbWVfX2lkN2E0Y2M4YTAtMWFiMS00=',
            'full_name': 'Michael Kidd-Gilchrist',
            'active': 'true',
            'starter': 'true',
            'statistics__list': {
                'defensive_rebounds': 1.0, 'two_points_made': 0.0,
                'free_throws_pct': 0.0, 'field_goals_made': 0.0, 'blocks': 0.0,
                'pls_min': 0.0, 'free_throws_made': 0.0, 'two_points_pct': 0.0,
                'three_points_att': 0.0, 'points': 0.0,
                'three_points_made': 0.0, 'field_goals_pct': 0.0,
                'blocked_att': 0.0, 'assists_turnover_ratio': 0.0,
                'flagrant_fouls': 0.0, 'assists': 0.0, 'two_points_att': 0.0,
                'three_points_pct': 0.0, 'tech_fouls': 0.0,
                'field_goals_att': 0.0, 'personal_fouls': 0.0, 'steals': 0.0,
                'free_throws_att': 0.0, 'minutes': '00:00',
                'offensive_rebounds': 0.0, 'rebounds': 0.0, 'turnovers': 0.0
            },
            'last_name': 'Kidd-Gilchrist',
            'played': 'true',
            'parent_list__id': 'players__list',
            'primary_position': 'SF',
            'jersey_number': 14.0
        }

    def __parse_and_send(self, unwrapped_obj, target):
        parts = target[0].split('.')
        oplog_obj = OpLogObjWrapper(parts[0], parts[1], unwrapped_obj)
        self.parser.parse(oplog_obj, target=target)
        self.parser.send()

    def test_parse(self):
        # Create the Player this update is for
        player = mommy.make(
            sports.nba.models.Player,
            srid=self.obj['id']
        )
        # Create the Game this update is for.
        game = mommy.make(
            sports.nba.models.Game,
            srid=self.obj['game__id']
        )

        # Fetch any existing PlayerStats. should be none.
        existing_player_stat = self.parser.player_stats_model.objects.filter(
            srid_game=game.srid,
            srid_player=player.srid
        )
        # Ensure none exist.
        self.assertEquals(existing_player_stat.count(), 0)

        # Parse the update object.
        self.__parse_and_send(self.obj, ('%s.game' % self.sport_db, self.parent_api))

        # Fetch the new PlayerStat that was created.
        new_player_stat = self.parser.player_stats_model.objects.filter(
            srid_game=game.srid,
            srid_player=player.srid
        )
        # Make sure it exists.
        self.assertEquals(new_player_stat.count(), 1)

        # Now send another update just to make sure it doesn't bomb out.
        self.__parse_and_send(self.obj, ('%s.game' % self.sport_db, self.parent_api))
        self.assertEquals(new_player_stat.count(), 1)
