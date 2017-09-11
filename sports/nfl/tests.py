from ast import literal_eval

from django.core.cache import cache
from django.utils import timezone
from model_mommy import mommy

import sports.nfl.models
from dataden.watcher import OpLogObjWrapper
from sports.nfl.models import (
    Team,
    Season,
    Game,
    GameBoxscore,
    PlayerStats,
    Player
)
from sports.nfl.parser import (
    DataDenNfl,

    SeasonSchedule,
    TeamHierarchy,
    PbpEventParser,
    GameBoxscoreParser,
    GameSchedule,
    # reducers, shrinkers, managers
    PlayReducer,
    PlayShrinker,
    PlayManager,

    # extra data "description parser"
    ExtraInfo,
)
from test.classes import AbstractTest

from .pbp_mock_data import PbpMockData
from logging import getLogger

logger = getLogger('sports.nfl.tests')


class TeamHierarchyParserTest(AbstractTest):
    def setUp(self):
        super().setUp()
        self.parser = TeamHierarchy()

    def __parse_and_send(self, unwrapped_obj, target):
        # oplog_obj = OpLogObjWrapper('nflo', 'play', unwrapped_obj)
        # self.parser.parse(oplog_obj, target=('nflo.play', 'pbp'))
        parts = target[0].split('.')
        oplog_obj = OpLogObjWrapper(parts[0], parts[1], unwrapped_obj)
        self.parser.parse(oplog_obj, target=target)
        # self.parser.send()

    def test_1(self):
        sport_db = 'nflo'
        parent_api = 'hierarchy'

        data = {
            "_id": "cGFyZW50X2FwaV9faWRoaWVyYXJjaHlsZWFndWVfX2lkM2M2ZDMxOGEtNjE2NC00MjkwLTliYmMtYmY5YmIyMWNjNGI4Y29uZmVyZW5jZV9faWQxYmRlZmUxMi02Y2IyLTRkNmEtYjIwOC1iMDQ2MDJhZTc5YzNkaXZpc2lvbl9faWRiOTVjZDI3ZC1kNjMxLTRmZTEtYmMwNS0wYWU0N2ZjMGIxNGJpZDQ4MDllY2IwLWFiZDMtNDUxZC05YzRhLTkyYTkwYjgzY2EwNg==",
            "alias": "MIA",
            "id": "4809ecb0-abd3-451d-9c4a-92a90b83ca06",
            "market": "Miami",
            "name": "Dolphins",
            "parent_api__id": "hierarchy",
            "dd_updated__id": 1470773235406,
            "league__id": "3c6d318a-6164-4290-9bbc-bf9bb21cc4b8",
            "conference__id": "1bdefe12-6cb2-4d6a-b208-b04602ae79c3",
            "division__id": "b95cd27d-d631-4fe1-bc05-0ae47fc0b14b",
            "references__list": {
                "reference": "MIA"
            },
            "venue": "50a5c833-1570-4c38-abc7-7914cf87dbde"
        }

        self.__parse_and_send(data, (sport_db + '.' + 'team', parent_api))

        # check if the team is there and the alias is correct now
        self.assertEquals(self.parser.team.alias, data.get('alias'))


# examples for TestPlayManagerRegexScraping
# (14:35) (No Huddle, Shotgun) R.Tannehill pass incomplete short right to J.Landry (D.Hall).
# (13:51) (Shotgun) A.Morris right guard to WAS 39 for 6 yards (K.Misi).
# (13:19) K.Cousins pass short left to J.Reed to MIA 49 for 12 yards (Br.McCain, J.Taylor).
# (12:40) PENALTY on WAS-Trent.Williams, False Start, 5 yards, enforced at MIA 49 - No Play.
# (12:16) A.Morris right guard to MIA 45 for 9 yards (K.Misi, R.Jones).
# (11:40) A.Morris left end to MIA 45 for no gain (K.Misi, K.Sheppard).
# (11:40) (Shotgun) K.Cousins pass short left to J.Reed to MIA 36 for 9 yards (N.Suh; R.Jones).
# (10:20) A.Morris left end to MIA 26 for 10 yards (J.Jenkins).
# (9:40) K.Cousins sacked at MIA 34 for -8 yards (J.Phillips).
# (9:00) A.Morris up the middle to MIA 29 for 5 yards (K.Misi).
# (8:24) (Shotgun) C.Thompson right guard to MIA 27 for 2 yards (K.Misi).
# (7:45) K.Forbath 45 yard field goal is GOOD, Center-N.Sundberg, Holder-T.Way.
# K.Forbath kicks 73 yards from WAS 35 to MIA -8. L.James to MIA 21 for 29 yards (K.Jarrett, J.Johnson).
# (7:33) (Shotgun) R.Tannehill pass short middle to G.Jennings to MIA 29 for 8 yards (K.Robinson).
# (7:01) L.Miller right end to MIA 30 for 1 yard (K.Robinson; D.Ihenacho).
# (6:21) (Shotgun) L.Miller right guard to MIA 30 for no gain (D.Ihenacho, J.Hatcher).
# (6:02) M.Darr punts 57 yards to WAS 13, Center-J.Denney. J.Crowder to WAS 23 for 10 yards (Z.Bowman; M.Thomas).
# (5:49) K.Cousins pass incomplete deep right to D.Jackson. WAS-D.Jackson was injured during the play. He is Out.  11-Jackson has a hamstring injury
# (5:41) A.Morris right guard to WAS 29 for 6 yards (K.Sheppard).
# (4:59) (Shotgun) K.Cousins pass short middle to P.Garcon to WAS 41 for 12 yards (J.Taylor, J.Jenkins).
# (4:19) (No Huddle, Shotgun) M.Jones right guard to WAS 43 for 2 yards (N.Suh). PENALTY on MIA-C.Wake, Defensive Offside, 5 yards, enforced at WAS 41 - No Play.
# (3:56) M.Jones right end to WAS 46 for no gain (C.Mosley, K.Misi).
# (3:16) K.Cousins pass incomplete short left to J.Reed. MIA-O.Vernon was injured during the play. His return is Questionable.  50- Vernon has an ankle injury
# (3:11) (Shotgun) K.Cousins pass deep right to P.Garcon pushed ob at MIA 36 for 18 yards (W.Aikens).
# (2:31) A.Morris left end to MIA 32 for 4 yards (T.Fede, E.Mitchell).
# (1:58) A.Morris up the middle to MIA 29 for 3 yards (J.Jenkins).
# (1:20) (Shotgun) C.Thompson left end to MIA 27 for 2 yards (J.Jenkins, Br.McCain).
# (:32) K.Forbath 46 yard field goal is No Good, Wide Right, Center-N.Sundberg, Holder-T.Way.
# (:27) (Shotgun) R.Tannehill pass incomplete short right to J.Cameron (J.Hatcher).
# (:22) (Shotgun) R.Tannehill pass short left to J.Landry to MIA 44 for 8 yards (D.Goldson, K.Robinson).
# (15:00) (Shotgun) R.Tannehill pass short middle to J.Landry to MIA 49 for 5 yards (K.Robinson).
# (14:35) (No Huddle, Shotgun) R.Tannehill pass incomplete short right to J.Landry (D.Hall).
# (14:32) (Shotgun) L.Miller right tackle to 50 for 1 yard (D.Ihenacho; T.Murphy). WAS-D.Ihenacho was injured during the play. He is Out.  24-Ihenacho has a wrist injury
# (14:00) (Shotgun) R.Tannehill pass incomplete short middle to J.Landry. Penalty on MIA-J.James, Illegal Formation, declined."""

class TestRushPlayManagerRegexScraping(AbstractTest):
    def setUp(self):
        super().setUp()
        self.play_type = 'rush'  # this would come in the SportRadar play data

    def test_rush_1(self):
        """ test wildcat this one is a rush """
        description = """(2:00) (Shotgun) Direct snap to M.Bennett.  M.Bennett up the middle to 50 for 7 yards (F.Cox)."""
        extra_info_instance = ExtraInfo(self.play_type, description)
        data = extra_info_instance.get_data()
        # print('data:', str(data))
        self.assertIsNotNone(data.get(self.play_type))

        # more tests
        self.assertTrue(data.get(ExtraInfo.wildcat))

    def test_rush_2(self):
        """ test QB scramble, side: middle"""
        description = """(6:22) T.Taylor scrambles right end pushed ob at RIC 36 for 11 yards (A.Barr)."""
        extra_info_instance = ExtraInfo(self.play_type, description)
        data = extra_info_instance.get_data()
        # print('data:', str(data))
        self.assertIsNotNone(data.get(self.play_type))

        # more tests
        rush_data = data.get(self.play_type)
        self.assertTrue(rush_data.get(ExtraInfo.scramble))
        self.assertEquals(ExtraInfo.side_right, rush_data.get(ExtraInfo.side))

    def test_rush_3(self):
        """ handoff to rusher up the middle """
        description = """(7:37) L.Murray up the middle to 50 for 7 yards (C.Woodson)."""
        extra_info_instance = ExtraInfo(self.play_type, description)
        data = extra_info_instance.get_data()
        # print('data:', str(data))
        self.assertIsNotNone(data.get(self.play_type))

        # more tests
        rush_data = data.get(self.play_type)
        self.assertFalse(rush_data.get(ExtraInfo.scramble))
        self.assertEquals(ExtraInfo.side_middle, rush_data.get(ExtraInfo.side))


class TestPassPlayManagerRegexScraping(AbstractTest):
    """
    the nfl play will have some datapoints extracted from the text description.

    lets make sure were doing it right.

    a few notes on regular expressions

        In [1]: import re
        In [2]: description = "(:27) (Shotgun) R.Tannehill pass incomplete short right to J.Cameron (J.Hatcher)."
        In [3]: l_description = description.lower()
        In [19]: re.findall(r'(short|deep|left|middle|right)', l_description)
        Out[19]: ['short', 'right']
        In [42]: re.findall(r'shotgun', l_description)
        Out[42]: ['shotgun']

        In [22]: d2 = "(14:35) (No Huddle, Shotgun) R.Tannehill pass incomplete short right to J.Landry (D.Hall)."
        In [23]: l_d2 = d2.lower()
        In [39]: re.findall(r'(no[\s]+huddle|shotgun)', l_d2)
        Out[39]: ['no huddle', 'shotgun']
        In [41]: re.findall(r'no[\s]+huddle', l_d2)
        Out[41]: ['no huddle']

    """

    def setUp(self):
        super().setUp()
        self.play_type = 'pass'  # this would come in the SportRadar play data

    def test_pass_1(self):
        """ test formation: shotgun """
        description = """(:27) (Shotgun) R.Tannehill pass incomplete short right to J.Cameron (J.Hatcher)."""
        extra_info_instance = ExtraInfo(self.play_type, description)
        data = extra_info_instance.get_data()
        # print('data:', str(data))
        self.assertIsNotNone(data.get(self.play_type))

        # more tests
        self.assertEquals(ExtraInfo.str_formation_shotgun, data.get(ExtraInfo.formation))

    def test_pass_2(self):
        """ test no huddle and formation: shotgun """
        description = """(14:35) (No Huddle, Shotgun) R.Tannehill pass incomplete short right to J.Landry (D.Hall)."""
        extra_info_instance = ExtraInfo(self.play_type, description)
        data = extra_info_instance.get_data()
        # print('data:', str(data))
        pass_data = data.get(self.play_type)
        self.assertIsNotNone(pass_data)

        # more tests
        self.assertTrue(data.get(ExtraInfo.no_huddle))
        self.assertEquals(ExtraInfo.str_formation_shotgun, data.get(ExtraInfo.formation))
        # distance: short
        self.assertEquals(ExtraInfo.distance_short, pass_data.get(ExtraInfo.distance))
        # side: right
        self.assertEquals(ExtraInfo.side_right, pass_data.get(ExtraInfo.side))

    def test_pass_3(self):
        """ test formation: default """
        description = """(9:37) D.Carr pass short right to O.Beckham pushed ob at IRV 3 for 14 yards (H.Smith)."""
        extra_info_instance = ExtraInfo(self.play_type, description)
        data = extra_info_instance.get_data()
        # print('data:', str(data))
        self.assertIsNotNone(data.get(self.play_type))

        # more tests
        self.assertFalse(data.get(ExtraInfo.no_huddle))
        self.assertEquals(ExtraInfo.default_formation, data.get(ExtraInfo.formation))

    def test_pass_4(self):
        """ test intercepted flag """
        description = """(3:46) T.Taylor pass deep left intended for O.Beckham INTERCEPTED by D.Rodgers-Cromartie [E.Ansah] at IRV 0. D.Rodgers-Cromartie to IRV 32 for 32 yards (T.Kelce)."""
        extra_info_instance = ExtraInfo(self.play_type, description)
        data = extra_info_instance.get_data()
        # print('data:', str(data))
        self.assertIsNotNone(data.get(self.play_type))

        # more tests
        self.assertTrue(data.get(ExtraInfo.intercepted))
        self.assertEquals(ExtraInfo.default_formation, data.get(ExtraInfo.formation))


class TestPlayManager(AbstractTest):
    """ parse some information out of the human readable text description """

    def setUp(self):
        super().setUp()
        # actual example from mongo of an NFL official feed play object (from the pbp feed)
        self.data = {
            "_id": "cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDAxNDFhMGE1LTEzZTUtNGIyOC1iMTlmLTBjMzkyM2FhZWY2ZXF1YXJ0ZXJfX2lkZmQzMTM2OGItYTE1OS00ZjU2LWEwMjItYWZjNjkxZTM0NzU1cGFyZW50X2xpc3RfX2lkcGxheV9ieV9wbGF5X19saXN0ZHJpdmVfX2lkMGIxYWVhNzAtNmRhMC00YzZkLWIzZjUtMTUwZDVmZTczYWY2aWRkNTYzZjkzYy02ZjlmLTQ5MzEtOGNmYi1lNTRmZDlkNWZhMTc=",
            "away_points": 0,
            "clock": "5:49",
            "home_points": 3,
            "id": "d563f93c-6f9f-4931-8cfb-e54fd9d5fa17",
            "play_clock": 14,
            "reference": 508,
            "sequence": 508,
            "type": "pass",
            "wall_clock": "2015-09-13T17:21:38+00:00",
            "parent_api__id": "pbp",
            "dd_updated__id": 1464841517401,
            "game__id": "0141a0a5-13e5-4b28-b19f-0c3923aaef6e",
            "quarter__id": "fd31368b-a159-4f56-a022-afc691e34755",
            "parent_list__id": "play_by_play__list",
            "drive__id": "0b1aea70-6da0-4c6d-b3f5-150d5fe73af6",
            "start_situation__list": {
                "clock": "5:49",
                "down": 1,
                "yfd": 10,
                "possession": "22052ff7-c065-42ee-bc8f-c4691c50e624",
                "location": "22052ff7-c065-42ee-bc8f-c4691c50e624"
            },
            "end_situation__list": {
                "clock": "5:41",
                "down": 2,
                "yfd": 10,
                "possession": "22052ff7-c065-42ee-bc8f-c4691c50e624",
                "location": "22052ff7-c065-42ee-bc8f-c4691c50e624"
            },
            "description": "(5:49) 8-K.Cousins pass incomplete deep right to 11-D.Jackson. WAS-11-D.Jackson was injured during the play. He is Out.  11-Jackson has a hamstring injury",
            "alt_description": "(5:49) K.Cousins pass incomplete deep right to D.Jackson. WAS-D.Jackson was injured during the play. He is Out.  11-Jackson has a hamstring injury",
            "statistics__list": {
                "pass__list": {
                    "att_yards": 47,
                    "attempt": 1,
                    "complete": 0,
                    "confirmed": "true",
                    "goaltogo": 0,
                    "inside_20": 0,
                    "team": "22052ff7-c065-42ee-bc8f-c4691c50e624",
                    "player": "bbd0942c-6f77-4f83-a6d0-66ec6548019e"
                },
                "receive__list": {
                    "confirmed": "true",
                    "goaltogo": 0,
                    "inside_20": 0,
                    "target": 1,
                    "team": "22052ff7-c065-42ee-bc8f-c4691c50e624",
                    "player": "3e618eb6-41f2-4f20-ad70-2460f9366f43"
                }
            }
        }

    def test_reducer(self):
        """ reduce() method should remove the key-values in the data """
        play_reducer = PlayReducer(self.data)
        reduced = play_reducer.reduce()
        # ensure the fields named in the reducer no longer exist in the 'reduced' data
        for field in PlayReducer.remove_fields:
            self.assertIsNone(reduced.get(field))

    def test_shrinker(self):
        """ shrink() method should rename the top level keys in the data using its 'fields' property """
        play_shrinker = PlayShrinker(self.data)
        shrunk = play_shrinker.shrink()
        # this is not a great test, but at the very least it ensures
        # we didnt add additional key-values on accident, plus
        # it provides a straightforward usage example

    def test_manager(self):
        """
        manager get_data() performs (in order)
            1.  a reduce
            2.  a shrink
            3.  optionally updates its data with an additional dict
        """
        additional_data = {'special_field_1': 'special_value_1'}
        play_manager = PlayManager(self.data)

        # the fields in additional_data should NOT show up in the
        # data returned by get_data() -- because we didnt add additional_data
        play_data = play_manager.get_data()
        for field in additional_data.keys():
            self.assertFalse(field in play_data.keys())

        # the fields in additional_data should show up in the
        # data because we called get_data() with additional_data
        play_data_with_additions = play_manager.get_data(additional_data)
        for field in additional_data.keys():
            self.assertTrue(field in play_data_with_additions.keys())

    def test_manager(self):
        """
        PlayManager get_data() adds the custom, desired fields from parsing 'description' field.
        """
        play_manager = PlayManager(self.data)
        # TODO


class TestTeamBoxscoreParser(AbstractTest):
    """ tests the send() part only """

    def setUp(self):
        super().setUp()
        self.parser = DataDenNfl()

    def __parse_and_send(self, unwrapped_obj, target):
        # oplog_obj = OpLogObjWrapper('nflo', 'play', unwrapped_obj)
        # self.parser.parse(oplog_obj, target=('nflo.play', 'pbp'))
        parts = target[0].split('.')
        oplog_obj = OpLogObjWrapper(parts[0], parts[1], unwrapped_obj)
        self.parser.parse(oplog_obj)

    def test_1(self):
        sport_db = 'nflo'
        parent_api = 'boxscores'

        data = {
            "_id": "cGFyZW50X2FwaV9faWRib3hzY29yZX==",
            "alias": "TB",
            "id": "4254d319-1bc7-4f81-b4ab-b5e6f3402b69",
            "market": "Tampa Bay",
            "name": "Buccaneers",
            "points": 14,
            "reference": 4970,
            "remaining_timeouts": 2,
            "used_timeouts": 1,
            "parent_api__id": "boxscores",
            "dd_updated__id": 1464834061361,
            "game__id": "1ca9a0c1-d145-4acb-aca2-cb2b5fe529b9",
            "parent_list__id": "summary__list"
        }

        # Parse it!
        self.__parse_and_send(data, (sport_db + '.' + 'play', parent_api))


class TestGameBoxscoreParser(AbstractTest):
    """ tests the send() part only """

    def setUp(self):
        cache.clear()
        super().setUp()
        self.parser = GameBoxscoreParser()

    def __parse_and_send(self, unwrapped_obj, target):
        # oplog_obj = OpLogObjWrapper('nflo', 'play', unwrapped_obj)
        # self.parser.parse(oplog_obj, target=('nflo.play', 'pbp'))
        parts = target[0].split('.')
        oplog_obj = OpLogObjWrapper(parts[0], parts[1], unwrapped_obj)
        self.parser.parse(oplog_obj, target=target)
        return self.parser
        # self.parser.send()

    def test_1(self):
        sport_db = 'nflo'
        parent_api = 'boxscores'

        data = {
            "_id": "cGFyZW50X2FwaV9faWRib3hzY29yZXNpZDAxNDFhMGE1LTEzZTUtNGIyOC1iMTlmLTBjMzkyM2FhZWY2ZQ==",
            "attendance": 76512,
            "clock": "00:00",
            "entry_mode": "INGEST",
            "id": "0141a0a5-13e5-4b28-b19f-0c3923aaef6e",
            "number": 8,
            "quarter": 4,
            "reference": 56510,
            "scheduled": "2015-09-13T17:02:41+00:00",
            "status": "closed",
            "utc_offset": -5,
            "weather": "Partly Cloudy Temp: 69 F, Humidity: 58%, Wind: NW 10 mph",
            "xmlns": "http://feed.elasticstats.com/schema/nfl/premium/boxscore-v2.0.xsd",
            "parent_api__id": "boxscores",
            "dd_updated__id": 1464834044370,
            "summary__list": {
                "season": "46aa2ca3-c2fc-455d-8256-1f7893a87113",
                "week": "581edacd-e641-43d6-9e69-76b29a306643",
                "venue": "7c11bb2d-4a53-4842-b842-0f1c63ed78e9",
                "home": "22052ff7-c065-42ee-bc8f-c4691c50e624",
                "away": "4809ecb0-abd3-451d-9c4a-92a90b83ca06"
            },
            "situation__list": {
                "clock": "00:00",
                "down": 2,
                "yfd": 11,
                "possession": "4809ecb0-abd3-451d-9c4a-92a90b83ca06",
                "location": "4809ecb0-abd3-451d-9c4a-92a90b83ca06"
            },
            "last_event__list": {
                "event": "c68447b0-425f-4e7b-8200-581ca222c03d"
            },
            "scoring__list": [
                {
                    "quarter": "fd31368b-a159-4f56-a022-afc691e34755"
                },
                {
                    "quarter": "17ee8c4c-3e1c-4dbb-83eb-f54fabe2a117"
                },
                {
                    "quarter": "da1c72aa-a5eb-44db-a23f-f9e2284d7968"
                },
                {
                    "quarter": "99063002-e5ee-4239-b686-f5aaa192e5d8"
                }
            ],
            "scoring_drives__list": [
                {
                    "drive": "a956d9cb-d8ab-408c-91fc-442f06e338ff"
                },
                {
                    "drive": "37c135a1-9d50-4da7-a975-f93a5bc2bfb5"
                },
                {
                    "drive": "d7474f02-e785-4638-b604-1065174d4a67"
                },
                {
                    "drive": "3b6e7850-bfa5-4ac8-90f4-9bd14a5a12c9"
                }
            ]
        }

        home_team = mommy.make(
            sports.nfl.models.Team,
            alias="DEN",
            srid="22052ff7-c065-42ee-bc8f-c4691c50e624"
        )

        away_team = mommy.make(
            sports.nfl.models.Team,
            alias="OKC",
            srid="4809ecb0-abd3-451d-9c4a-92a90b83ca06"
        )

        # Create a Game model so this boxcore can be parsed.
        game = mommy.make(
            Game,
            srid=data['id'],
            away=away_team,
            srid_away=away_team.srid,
            home=home_team,
            srid_home=home_team.srid,
            status='inprogress'
        )

        parser = self.__parse_and_send(data, (sport_db + '.' + 'game', parent_api))

        parser.send()
        sent_data = parser.get_send_data()
        # Make sure that by parsing a boxscore, we don't change the game's status.
        # This is because NFL statuses should be automatically set to 'verify' in the
        # Schedule parser and we don't want to goof up that logic in the Boxscore praser.
        game.refresh_from_db()
        self.assertEqual(game.status, 'inprogress')


class TestPlayParser(AbstractTest):
    """
    parsers and sends PBP objects from the official feed

    NOTE: because the test database does parse the stats previously,
    we will NOT HAVE the PlayerStats objects.
    """

    def setUp(self):
        cache.clear()
        super().setUp()
        self.parser = PbpEventParser()

    def __parse_and_send(self, unwrapped_obj, target, tag=None):
        # oplog_obj = OpLogObjWrapper('nflo', 'play', unwrapped_obj)
        # self.parser.parse(oplog_obj, target=('nflo.play', 'pbp'))
        parts = target[0].split('.')
        oplog_obj = OpLogObjWrapper(parts[0], parts[1], unwrapped_obj)
        if tag is not None:
            print('tag:', tag)

        self.parser.parse(oplog_obj, target=target)

        return self.parser
        # #
        # # get the 'player' srids
        # player_srids = self.parser.get_srids_for_field('player')
        # print('"player" field srids:', str(player_srids))
        #
        # # get the game srid from the 'game__id' field
        # #game_srid = self.parser.get_srids_for_field('game__id')
        # game_srid = self.parser.get_game_srid('game__id')
        # print('"game" field srid:', str(game_srid))
        #
        # #
        # # look up the player stats (TODO get the game srid as well)
        # player_stats_found = self.parser.find_player_stats()
        # print('player_stats_found:', str(player_stats_found), ' BECAUSE THERE ARE NONE IN THE TEST DB!')

        # print('get_send_data:', self.parser.get_send_data())

        # print('SL', self.parser.StartLocationCache().fetch(self.parser.ts, self.parser.play_srid))
        # print('SP', self.parser.StartPossessionCache().fetch(self.parser.ts, self.parser.play_srid))
        # print('EL', self.parser.EndLocationCache().fetch(self.parser.ts, self.parser.play_srid))
        # print('EP', self.parser.EndPossessionCache().fetch(self.parser.ts, self.parser.play_srid))

        # test sending with pusher. we cant do this with codeship though! (so remove it when done)
        # for x in range(20): # try to get rate limited to see the response data
        #     self.parser.send(force=True) # fun times

    def test_1(self):
        """ kickoff (touchback) """
        sport_db = 'nflo'
        parent_api = 'pbp'
        play = {
            'start_situation__list': {'yfd': 0.0,
                                      'location': '4809ecb0-abd3-451d-9c4a-92a90b83ca06',
                                      'clock': '15:00',
                                      'possession': '4809ecb0-abd3-451d-9c4a-92a90b83ca06',
                                      'down': 0.0},
            'away_points': 0.0, 'reference': 63.0,
            'end_situation__list': {'yfd': 10.0, 'location': '22052ff7-c065-42ee-bc8f-c4691c50e624',
                                    'clock': '15:00',
                                    'possession': '22052ff7-c065-42ee-bc8f-c4691c50e624',
                                    'down': 1.0},
            'alt_description': 'A.Franks kicks 65 yards from MIA 35 to end zone, Touchback.',
            'game__id': '0141a0a5-13e5-4b28-b19f-0c3923aaef6e', 'parent_api__id': 'pbp',
            'clock': '15:00',
            'drive__id': 'a956d9cb-d8ab-408c-91fc-442f06e338ff', 'statistics__list': {
                'kick__list': {'gross_yards': 74.0, 'team': '4809ecb0-abd3-451d-9c4a-92a90b83ca06',
                               'yards': 65.0,
                               'attempt': 1.0, 'touchback': 1.0,
                               'player': '59da7aea-f21a-43c5-b0bf-2d1e8b19da80',
                               'confirmed': 'true'},
                'return__list': {'team': '22052ff7-c065-42ee-bc8f-c4691c50e624', 'touchback': 1.0,
                                 'confirmed': 'true',
                                 'category': 'kick_return'}},
            'id': '9de4c5df-5e94-4fe2-b646-ba1dca0a1afd',
            'sequence': 63.0, 'parent_list__id': 'play_by_play__list', 'home_points': 0.0,
            'description': '3-A.Franks kicks 65 yards from MIA 35 to end zone, Touchback.',
            '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDAxNDFhMGE1LTEzZTUtNGIyOC1iMTlmLTBjMzkyM2FhZWY2ZXF1YXJ0ZXJfX2lkZmQzMTM2OGItYTE1OS00ZjU2LWEwMjItYWZjNjkxZTM0NzU1cGFyZW50X2xpc3RfX2lkcGxheV9ieV9wbGF5X19saXN0ZHJpdmVfX2lkYTk1NmQ5Y2ItZDhhYi00MDhjLTkxZmMtNDQyZjA2ZTMzOGZmaWQ5ZGU0YzVkZi01ZTk0LTRmZTItYjY0Ni1iYTFkY2EwYTFhZmQ=',
            'type': 'kickoff', 'play_clock': 12.0,
            'quarter__id': 'fd31368b-a159-4f56-a022-afc691e34755',
            'dd_updated__id': 1464841517401, 'wall_clock': '2015-09-13T17:02:41+00:00'}

        # self.__parse_and_send(unwrapped_obj)
        self.__parse_and_send(play, (sport_db + '.' + 'play', parent_api))

    def test_2(self):
        """ rushing play """
        sport_db = 'nflo'
        parent_api = 'pbp'

        start_location = {'parent_api__id': 'pbp', 'id': '22052ff7-c065-42ee-bc8f-c4691c50e624',
                          'market': 'Washington',
                          'quarter__id': 'fd31368b-a159-4f56-a022-afc691e34755',
                          'reference': 4971.0, 'yardline': 20.0,
                          'parent_list__id': 'start_situation__list',
                          'dd_updated__id': 1464841517401,
                          'drive__id': 'a956d9cb-d8ab-408c-91fc-442f06e338ff', 'name': 'Redskins',
                          '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDAxNDFhMGE1LTEzZTUtNGIyOC1iMTlmLTBjMzkyM2FhZWY2ZXF1YXJ0ZXJfX2lkZmQzMTM2OGItYTE1OS00ZjU2LWEwMjItYWZjNjkxZTM0NzU1cGFyZW50X2xpc3RfX2lkc3RhcnRfc2l0dWF0aW9uX19saXN0ZHJpdmVfX2lkYTk1NmQ5Y2ItZDhhYi00MDhjLTkxZmMtNDQyZjA2ZTMzOGZmcGxheV9faWQzYTJlOWJiNC02Yjc5LTQ3M2EtYjg2YS01MjJiOTJlODhjNzFpZDIyMDUyZmY3LWMwNjUtNDJlZS1iYzhmLWM0NjkxYzUwZTYyNA==',
                          'alias': 'WAS', 'play__id': '3a2e9bb4-6b79-473a-b86a-522b92e88c71',
                          'game__id': '0141a0a5-13e5-4b28-b19f-0c3923aaef6e'}
        self.__parse_and_send(start_location, (sport_db + '.' + 'location', parent_api))

        start_possession = {'parent_api__id': 'pbp', 'id': '22052ff7-c065-42ee-bc8f-c4691c50e624',
                            'market': 'Washington',
                            'quarter__id': 'fd31368b-a159-4f56-a022-afc691e34755',
                            'reference': 4971.0, 'game__id': '0141a0a5-13e5-4b28-b19f-0c3923aaef6e',
                            'parent_list__id': 'start_situation__list',
                            'dd_updated__id': 1464841517401,
                            'name': 'Redskins',
                            '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDAxNDFhMGE1LTEzZTUtNGIyOC1iMTlmLTBjMzkyM2FhZWY2ZXF1YXJ0ZXJfX2lkZmQzMTM2OGItYTE1OS00ZjU2LWEwMjItYWZjNjkxZTM0NzU1cGFyZW50X2xpc3RfX2lkc3RhcnRfc2l0dWF0aW9uX19saXN0ZHJpdmVfX2lkYTk1NmQ5Y2ItZDhhYi00MDhjLTkxZmMtNDQyZjA2ZTMzOGZmcGxheV9faWQzYTJlOWJiNC02Yjc5LTQ3M2EtYjg2YS01MjJiOTJlODhjNzFpZDIyMDUyZmY3LWMwNjUtNDJlZS1iYzhmLWM0NjkxYzUwZTYyNA==',
                            'alias': 'WAS', 'play__id': '3a2e9bb4-6b79-473a-b86a-522b92e88c71',
                            'drive__id': 'a956d9cb-d8ab-408c-91fc-442f06e338ff'}
        self.__parse_and_send(start_possession, (sport_db + '.' + 'possession', parent_api))

        end_location = {'parent_api__id': 'pbp', 'id': '22052ff7-c065-42ee-bc8f-c4691c50e624',
                        'market': 'Washington',
                        'quarter__id': 'fd31368b-a159-4f56-a022-afc691e34755', 'reference': 4971.0,
                        'yardline': 25.0,
                        'parent_list__id': 'end_situation__list', 'dd_updated__id': 1464841517401,
                        'drive__id': 'a956d9cb-d8ab-408c-91fc-442f06e338ff', 'name': 'Redskins',
                        '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDAxNDFhMGE1LTEzZTUtNGIyOC1iMTlmLTBjMzkyM2FhZWY2ZXF1YXJ0ZXJfX2lkZmQzMTM2OGItYTE1OS00ZjU2LWEwMjItYWZjNjkxZTM0NzU1cGFyZW50X2xpc3RfX2lkZW5kX3NpdHVhdGlvbl9fbGlzdGRyaXZlX19pZGE5NTZkOWNiLWQ4YWItNDA4Yy05MWZjLTQ0MmYwNmUzMzhmZnBsYXlfX2lkM2EyZTliYjQtNmI3OS00NzNhLWI4NmEtNTIyYjkyZTg4YzcxaWQyMjA1MmZmNy1jMDY1LTQyZWUtYmM4Zi1jNDY5MWM1MGU2MjQ=',
                        'alias': 'WAS', 'play__id': '3a2e9bb4-6b79-473a-b86a-522b92e88c71',
                        'game__id': '0141a0a5-13e5-4b28-b19f-0c3923aaef6e'}
        self.__parse_and_send(end_location, (sport_db + '.' + 'location', parent_api))

        end_possession = {'parent_api__id': 'pbp', 'id': '22052ff7-c065-42ee-bc8f-c4691c50e624',
                          'market': 'Washington',
                          'quarter__id': 'fd31368b-a159-4f56-a022-afc691e34755',
                          'reference': 4971.0,
                          'game__id': '0141a0a5-13e5-4b28-b19f-0c3923aaef6e',
                          'parent_list__id': 'end_situation__list',
                          'dd_updated__id': 1464841517401, 'name': 'Redskins',
                          '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDAxNDFhMGE1LTEzZTUtNGIyOC1iMTlmLTBjMzkyM2FhZWY2ZXF1YXJ0ZXJfX2lkZmQzMTM2OGItYTE1OS00ZjU2LWEwMjItYWZjNjkxZTM0NzU1cGFyZW50X2xpc3RfX2lkZW5kX3NpdHVhdGlvbl9fbGlzdGRyaXZlX19pZGE5NTZkOWNiLWQ4YWItNDA4Yy05MWZjLTQ0MmYwNmUzMzhmZnBsYXlfX2lkM2EyZTliYjQtNmI3OS00NzNhLWI4NmEtNTIyYjkyZTg4YzcxaWQyMjA1MmZmNy1jMDY1LTQyZWUtYmM4Zi1jNDY5MWM1MGU2MjQ=',
                          'alias': 'WAS', 'play__id': '3a2e9bb4-6b79-473a-b86a-522b92e88c71',
                          'drive__id': 'a956d9cb-d8ab-408c-91fc-442f06e338ff'}
        self.__parse_and_send(end_possession, (sport_db + '.' + 'possession', parent_api))

        play = {'parent_api__id': 'pbp', 'id': '3a2e9bb4-6b79-473a-b86a-522b92e88c71',
                'start_situation__list': {'location': '22052ff7-c065-42ee-bc8f-c4691c50e624',
                                          'down': 1.0, 'yfd': 10.0,
                                          'clock': '15:00',
                                          'possession': '22052ff7-c065-42ee-bc8f-c4691c50e624'},
                'drive__id': 'a956d9cb-d8ab-408c-91fc-442f06e338ff',
                'game__id': '0141a0a5-13e5-4b28-b19f-0c3923aaef6e',
                'statistics__list': {'defense__list': {'confirmed': 'true', 'tackle': 1.0,
                                                       'player': '7190fb71-0916-4f9d-88a0-8c1a8c1c9d0d',
                                                       'team': '4809ecb0-abd3-451d-9c4a-92a90b83ca06'},
                                     'rush__list': {'inside_20': 0.0, 'yards': 5.0,
                                                    'player': 'bd10efdf-d8e7-4e23-ab1a-1e42fb65131b',
                                                    'team': '22052ff7-c065-42ee-bc8f-c4691c50e624',
                                                    'confirmed': 'true',
                                                    'attempt': 1.0, 'goaltogo': 0.0}},
                'reference': 82.0,
                'type': 'rush', 'wall_clock': '2015-09-13T17:03:26+00:00',
                'description': '(15:00) 46-A.Morris left tackle to WAS 25 for 5 yards (52-K.Sheppard).',
                'dd_updated__id': 1464841517401, 'play_clock': 12.0,
                'quarter__id': 'fd31368b-a159-4f56-a022-afc691e34755', 'clock': '15:00',
                '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDAxNDFhMGE1LTEzZTUtNGIyOC1iMTlmLTBjMzkyM2FhZWY2ZXF1YXJ0ZXJfX2lkZmQzMTM2OGItYTE1OS00ZjU2LWEwMjItYWZjNjkxZTM0NzU1cGFyZW50X2xpc3RfX2lkcGxheV9ieV9wbGF5X19saXN0ZHJpdmVfX2lkYTk1NmQ5Y2ItZDhhYi00MDhjLTkxZmMtNDQyZjA2ZTMzOGZmaWQzYTJlOWJiNC02Yjc5LTQ3M2EtYjg2YS01MjJiOTJlODhjNzE=',
                'parent_list__id': 'play_by_play__list', 'away_points': 0.0, 'home_points': 0.0,
                'end_situation__list': {'location': '22052ff7-c065-42ee-bc8f-c4691c50e624',
                                        'down': 2.0, 'yfd': 5.0,
                                        'clock': '14:30',
                                        'possession': '22052ff7-c065-42ee-bc8f-c4691c50e624'},
                'alt_description': '(15:00) A.Morris left tackle to WAS 25 for 5 yards (K.Sheppard).',
                'sequence': 82.0}
        self.__parse_and_send(play, (sport_db + '.' + 'play', parent_api))

    def test_3(self):
        """ passing play """
        sport_db = 'nflo'
        parent_api = 'pbp'

        start_possession = {'alias': 'WAS', 'quarter__id': 'fd31368b-a159-4f56-a022-afc691e34755',
                            'parent_api__id': 'pbp',
                            'play__id': '7e49db54-68d0-444d-b244-690f3930b77b', 'reference': 4971.0,
                            'market': 'Washington',
                            '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDAxNDFhMGE1LTEzZTUtNGIyOC1iMTlmLTBjMzkyM2FhZWY2ZXF1YXJ0ZXJfX2lkZmQzMTM2OGItYTE1OS00ZjU2LWEwMjItYWZjNjkxZTM0NzU1cGFyZW50X2xpc3RfX2lkc3RhcnRfc2l0dWF0aW9uX19saXN0ZHJpdmVfX2lkYTk1NmQ5Y2ItZDhhYi00MDhjLTkxZmMtNDQyZjA2ZTMzOGZmcGxheV9faWQ3ZTQ5ZGI1NC02OGQwLTQ0NGQtYjI0NC02OTBmMzkzMGI3N2JpZDIyMDUyZmY3LWMwNjUtNDJlZS1iYzhmLWM0NjkxYzUwZTYyNA==',
                            'drive__id': 'a956d9cb-d8ab-408c-91fc-442f06e338ff', 'name': 'Redskins',
                            'dd_updated__id': 1464841517401,
                            'game__id': '0141a0a5-13e5-4b28-b19f-0c3923aaef6e',
                            'id': '22052ff7-c065-42ee-bc8f-c4691c50e624',
                            'parent_list__id': 'start_situation__list'}
        self.__parse_and_send(start_possession, (sport_db + '.' + 'possession', parent_api))
        # required_parts = self.parser.update_required_parts(self.parser.ts, self.parser.play_srid)
        # self.assertTrue(None in required_parts)

        end_possession = {'alias': 'WAS', 'quarter__id': 'fd31368b-a159-4f56-a022-afc691e34755',
                          'parent_api__id': 'pbp',
                          'play__id': '7e49db54-68d0-444d-b244-690f3930b77b', 'reference': 4971.0,
                          'market': 'Washington',
                          '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDAxNDFhMGE1LTEzZTUtNGIyOC1iMTlmLTBjMzkyM2FhZWY2ZXF1YXJ0ZXJfX2lkZmQzMTM2OGItYTE1OS00ZjU2LWEwMjItYWZjNjkxZTM0NzU1cGFyZW50X2xpc3RfX2lkZW5kX3NpdHVhdGlvbl9fbGlzdGRyaXZlX19pZGE5NTZkOWNiLWQ4YWItNDA4Yy05MWZjLTQ0MmYwNmUzMzhmZnBsYXlfX2lkN2U0OWRiNTQtNjhkMC00NDRkLWIyNDQtNjkwZjM5MzBiNzdiaWQyMjA1MmZmNy1jMDY1LTQyZWUtYmM4Zi1jNDY5MWM1MGU2MjQ=',
                          'drive__id': 'a956d9cb-d8ab-408c-91fc-442f06e338ff', 'name': 'Redskins',
                          'dd_updated__id': 1464841517401,
                          'game__id': '0141a0a5-13e5-4b28-b19f-0c3923aaef6e',
                          'id': '22052ff7-c065-42ee-bc8f-c4691c50e624',
                          'parent_list__id': 'end_situation__list'}
        self.__parse_and_send(end_possession, (sport_db + '.' + 'possession', parent_api))
        # required_parts = self.parser.update_required_parts(self.parser.ts, self.parser.play_srid)
        # self.assertTrue(None in required_parts)

        start_location = {'play__id': '7e49db54-68d0-444d-b244-690f3930b77b', 'alias': 'WAS',
                          'quarter__id': 'fd31368b-a159-4f56-a022-afc691e34755',
                          'parent_api__id': 'pbp', 'yardline': 25.0,
                          'reference': 4971.0, 'market': 'Washington',
                          '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDAxNDFhMGE1LTEzZTUtNGIyOC1iMTlmLTBjMzkyM2FhZWY2ZXF1YXJ0ZXJfX2lkZmQzMTM2OGItYTE1OS00ZjU2LWEwMjItYWZjNjkxZTM0NzU1cGFyZW50X2xpc3RfX2lkc3RhcnRfc2l0dWF0aW9uX19saXN0ZHJpdmVfX2lkYTk1NmQ5Y2ItZDhhYi00MDhjLTkxZmMtNDQyZjA2ZTMzOGZmcGxheV9faWQ3ZTQ5ZGI1NC02OGQwLTQ0NGQtYjI0NC02OTBmMzkzMGI3N2JpZDIyMDUyZmY3LWMwNjUtNDJlZS1iYzhmLWM0NjkxYzUwZTYyNA==',
                          'drive__id': 'a956d9cb-d8ab-408c-91fc-442f06e338ff', 'name': 'Redskins',
                          'dd_updated__id': 1464841517401,
                          'game__id': '0141a0a5-13e5-4b28-b19f-0c3923aaef6e',
                          'id': '22052ff7-c065-42ee-bc8f-c4691c50e624',
                          'parent_list__id': 'start_situation__list'}
        self.__parse_and_send(start_location, (sport_db + '.' + 'location', parent_api))
        # required_parts = self.parser.update_required_parts(self.parser.ts, self.parser.play_srid)
        # self.assertTrue(None in required_parts)

        end_location = {'play__id': '7e49db54-68d0-444d-b244-690f3930b77b', 'alias': 'WAS',
                        'quarter__id': 'fd31368b-a159-4f56-a022-afc691e34755',
                        'parent_api__id': 'pbp', 'yardline': 29.0,
                        'reference': 4971.0, 'market': 'Washington',
                        '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDAxNDFhMGE1LTEzZTUtNGIyOC1iMTlmLTBjMzkyM2FhZWY2ZXF1YXJ0ZXJfX2lkZmQzMTM2OGItYTE1OS00ZjU2LWEwMjItYWZjNjkxZTM0NzU1cGFyZW50X2xpc3RfX2lkZW5kX3NpdHVhdGlvbl9fbGlzdGRyaXZlX19pZGE5NTZkOWNiLWQ4YWItNDA4Yy05MWZjLTQ0MmYwNmUzMzhmZnBsYXlfX2lkN2U0OWRiNTQtNjhkMC00NDRkLWIyNDQtNjkwZjM5MzBiNzdiaWQyMjA1MmZmNy1jMDY1LTQyZWUtYmM4Zi1jNDY5MWM1MGU2MjQ=',
                        'drive__id': 'a956d9cb-d8ab-408c-91fc-442f06e338ff', 'name': 'Redskins',
                        'dd_updated__id': 1464841517401,
                        'game__id': '0141a0a5-13e5-4b28-b19f-0c3923aaef6e',
                        'id': '22052ff7-c065-42ee-bc8f-c4691c50e624',
                        'parent_list__id': 'end_situation__list'}
        self.__parse_and_send(end_location, (sport_db + '.' + 'location', parent_api))
        # required_parts = self.parser.update_required_parts(self.parser.ts, self.parser.play_srid)
        # self.assertTrue(None in required_parts)

        play = {
            'start_situation__list': {'yfd': 5.0,
                                      'location': '22052ff7-c065-42ee-bc8f-c4691c50e624',
                                      'clock': '14:30',
                                      'possession': '22052ff7-c065-42ee-bc8f-c4691c50e624',
                                      'down': 2.0},
            'away_points': 0.0, 'reference': 103.0,
            'end_situation__list': {'yfd': 1.0, 'location': '22052ff7-c065-42ee-bc8f-c4691c50e624',
                                    'clock': '13:56',
                                    'possession': '22052ff7-c065-42ee-bc8f-c4691c50e624',
                                    'down': 3.0},
            'alt_description': '(14:30) (Shotgun) K.Cousins pass short right to A.Roberts to WAS 29 for 4 yards (B.Grimes).',
            'game__id': '0141a0a5-13e5-4b28-b19f-0c3923aaef6e', 'parent_api__id': 'pbp',
            'clock': '14:30',
            'drive__id': 'a956d9cb-d8ab-408c-91fc-442f06e338ff',
            'id': '7e49db54-68d0-444d-b244-690f3930b77b',
            'sequence': 103.0, 'parent_list__id': 'play_by_play__list', 'home_points': 0.0,
            'description': '(14:30) (Shotgun) 8-K.Cousins pass short right to 12-A.Roberts to WAS 29 for 4 yards (21-B.Grimes).',
            '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDAxNDFhMGE1LTEzZTUtNGIyOC1iMTlmLTBjMzkyM2FhZWY2ZXF1YXJ0ZXJfX2lkZmQzMTM2OGItYTE1OS00ZjU2LWEwMjItYWZjNjkxZTM0NzU1cGFyZW50X2xpc3RfX2lkcGxheV9ieV9wbGF5X19saXN0ZHJpdmVfX2lkYTk1NmQ5Y2ItZDhhYi00MDhjLTkxZmMtNDQyZjA2ZTMzOGZmaWQ3ZTQ5ZGI1NC02OGQwLTQ0NGQtYjI0NC02OTBmMzkzMGI3N2I=',
            'type': 'pass', 'statistics__list': {
                'receive__list': {'team': '22052ff7-c065-42ee-bc8f-c4691c50e624', 'yards': 4.0,
                                  'goaltogo': 0.0,
                                  'player': '9691f874-be36-4529-a7eb-dde22ee4a848',
                                  'confirmed': 'true',
                                  'reception': 1.0, 'yards_after_catch': 2.0, 'inside_20': 0.0,
                                  'target': 1.0},
                'pass__list': {'team': '22052ff7-c065-42ee-bc8f-c4691c50e624', 'yards': 4.0,
                               'goaltogo': 0.0,
                               'att_yards': 2.0, 'attempt': 1.0,
                               'player': 'bbd0942c-6f77-4f83-a6d0-66ec6548019e',
                               'complete': 1.0, 'inside_20': 0.0, 'confirmed': 'true'},
                'defense__list': {'team': '4809ecb0-abd3-451d-9c4a-92a90b83ca06', 'tackle': 1.0,
                                  'player': '7979b613-6dbf-4534-8166-6430433c1ec3',
                                  'confirmed': 'true'}},
            'quarter__id': 'fd31368b-a159-4f56-a022-afc691e34755', 'dd_updated__id': 1464841517401,
            'wall_clock': '2015-09-13T17:03:57+00:00'}
        self.__parse_and_send(play, (sport_db + '.' + 'play', parent_api))

    def test_4(self):
        """ kick_return example """
        sport_db = 'nflo'
        parent_api = 'pbp'

        start_location = {'quarter__id': '7b99cfe4-ca29-4868-8577-01b2b6cd34e9',
                          'play__id': '9098ec62-d4c2-49df-a452-60170c144715', 'reference': 4944.0,
                          'dd_updated__id': 1464854648745, 'yardline': 35.0,
                          '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDYzYjRkMzc0LTljN2MtNDE2ZS04YWE5LTQ1NmUyMmEzNmFmNnF1YXJ0ZXJfX2lkN2I5OWNmZTQtY2EyOS00ODY4LTg1NzctMDFiMmI2Y2QzNGU5cGFyZW50X2xpc3RfX2lkc3RhcnRfc2l0dWF0aW9uX19saXN0ZHJpdmVfX2lkYTU3ZTdmYTktY2MyYS00ZWI0LTg5MzQtOTQ4MTA3ZTczZmQ2cGxheV9faWQ5MDk4ZWM2Mi1kNGMyLTQ5ZGYtYTQ1Mi02MDE3MGMxNDQ3MTVpZGU2YWExM2E0LTAwNTUtNDhhOS1iYzQxLWJlMjhkYzEwNjkyOQ==',
                          'parent_api__id': 'pbp', 'name': 'Falcons',
                          'id': 'e6aa13a4-0055-48a9-bc41-be28dc106929',
                          'alias': 'ATL', 'drive__id': 'a57e7fa9-cc2a-4eb4-8934-948107e73fd6',
                          'game__id': '63b4d374-9c7c-416e-8aa9-456e22a36af6',
                          'parent_list__id': 'start_situation__list', 'market': 'Atlanta'}
        self.__parse_and_send(start_location, (sport_db + '.' + 'location', parent_api))

        start_possession = {'quarter__id': '7b99cfe4-ca29-4868-8577-01b2b6cd34e9',
                            'play__id': '9098ec62-d4c2-49df-a452-60170c144715', 'reference': 4944.0,
                            'dd_updated__id': 1464854648745,
                            'parent_list__id': 'start_situation__list',
                            '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDYzYjRkMzc0LTljN2MtNDE2ZS04YWE5LTQ1NmUyMmEzNmFmNnF1YXJ0ZXJfX2lkN2I5OWNmZTQtY2EyOS00ODY4LTg1NzctMDFiMmI2Y2QzNGU5cGFyZW50X2xpc3RfX2lkc3RhcnRfc2l0dWF0aW9uX19saXN0ZHJpdmVfX2lkYTU3ZTdmYTktY2MyYS00ZWI0LTg5MzQtOTQ4MTA3ZTczZmQ2cGxheV9faWQ5MDk4ZWM2Mi1kNGMyLTQ5ZGYtYTQ1Mi02MDE3MGMxNDQ3MTVpZGU2YWExM2E0LTAwNTUtNDhhOS1iYzQxLWJlMjhkYzEwNjkyOQ==',
                            'parent_api__id': 'pbp', 'name': 'Falcons',
                            'id': 'e6aa13a4-0055-48a9-bc41-be28dc106929',
                            'alias': 'ATL', 'game__id': '63b4d374-9c7c-416e-8aa9-456e22a36af6',
                            'drive__id': 'a57e7fa9-cc2a-4eb4-8934-948107e73fd6',
                            'market': 'Atlanta'}
        self.__parse_and_send(start_possession, (sport_db + '.' + 'possession', parent_api))

        end_location = {'quarter__id': '7b99cfe4-ca29-4868-8577-01b2b6cd34e9',
                        'play__id': '9098ec62-d4c2-49df-a452-60170c144715', 'reference': 4953.0,
                        'dd_updated__id': 1464854648745, 'yardline': 25.0,
                        '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDYzYjRkMzc0LTljN2MtNDE2ZS04YWE5LTQ1NmUyMmEzNmFmNnF1YXJ0ZXJfX2lkN2I5OWNmZTQtY2EyOS00ODY4LTg1NzctMDFiMmI2Y2QzNGU5cGFyZW50X2xpc3RfX2lkZW5kX3NpdHVhdGlvbl9fbGlzdGRyaXZlX19pZGE1N2U3ZmE5LWNjMmEtNGViNC04OTM0LTk0ODEwN2U3M2ZkNnBsYXlfX2lkOTA5OGVjNjItZDRjMi00OWRmLWE0NTItNjAxNzBjMTQ0NzE1aWRkMjZhMWNhNS03MjJkLTQyNzQtOGY5Ny1jOTJlNDljOTYzMTU=',
                        'parent_api__id': 'pbp', 'name': 'Titans',
                        'id': 'd26a1ca5-722d-4274-8f97-c92e49c96315',
                        'alias': 'TEN', 'drive__id': 'a57e7fa9-cc2a-4eb4-8934-948107e73fd6',
                        'game__id': '63b4d374-9c7c-416e-8aa9-456e22a36af6',
                        'parent_list__id': 'end_situation__list',
                        'market': 'Tennessee'}
        self.__parse_and_send(end_location, (sport_db + '.' + 'location', parent_api))

        end_possession = {'quarter__id': '7b99cfe4-ca29-4868-8577-01b2b6cd34e9',
                          'play__id': '9098ec62-d4c2-49df-a452-60170c144715', 'reference': 4953.0,
                          'dd_updated__id': 1464854648745, 'parent_list__id': 'end_situation__list',
                          '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDYzYjRkMzc0LTljN2MtNDE2ZS04YWE5LTQ1NmUyMmEzNmFmNnF1YXJ0ZXJfX2lkN2I5OWNmZTQtY2EyOS00ODY4LTg1NzctMDFiMmI2Y2QzNGU5cGFyZW50X2xpc3RfX2lkZW5kX3NpdHVhdGlvbl9fbGlzdGRyaXZlX19pZGE1N2U3ZmE5LWNjMmEtNGViNC04OTM0LTk0ODEwN2U3M2ZkNnBsYXlfX2lkOTA5OGVjNjItZDRjMi00OWRmLWE0NTItNjAxNzBjMTQ0NzE1aWRkMjZhMWNhNS03MjJkLTQyNzQtOGY5Ny1jOTJlNDljOTYzMTU=',
                          'parent_api__id': 'pbp', 'name': 'Titans',
                          'id': 'd26a1ca5-722d-4274-8f97-c92e49c96315',
                          'alias': 'TEN', 'game__id': '63b4d374-9c7c-416e-8aa9-456e22a36af6',
                          'drive__id': 'a57e7fa9-cc2a-4eb4-8934-948107e73fd6',
                          'market': 'Tennessee'}
        self.__parse_and_send(end_possession, (sport_db + '.' + 'possession', parent_api))

        play = {'wall_clock': '2015-08-14T01:39:07+00:00',
                'quarter__id': '7b99cfe4-ca29-4868-8577-01b2b6cd34e9',
                'away_points': 24.0, 'end_situation__list': {'down': 1.0, 'clock': '7:29',
                                                             'location': 'd26a1ca5-722d-4274-8f97-c92e49c96315',
                                                             'yfd': 10.0,
                                                             'possession': 'd26a1ca5-722d-4274-8f97-c92e49c96315'},
                'reference': 3493.0, 'dd_updated__id': 1464854648745,
                'description': '5-M.Bosher kicks 69 yards from ATL 35 to TEN -4. 16-T.McBride to TEN 25 for 29 yards (27-K.White).',
                '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDYzYjRkMzc0LTljN2MtNDE2ZS04YWE5LTQ1NmUyMmEzNmFmNnF1YXJ0ZXJfX2lkN2I5OWNmZTQtY2EyOS00ODY4LTg1NzctMDFiMmI2Y2QzNGU5cGFyZW50X2xpc3RfX2lkcGxheV9ieV9wbGF5X19saXN0ZHJpdmVfX2lkYTU3ZTdmYTktY2MyYS00ZWI0LTg5MzQtOTQ4MTA3ZTczZmQ2aWQ5MDk4ZWM2Mi1kNGMyLTQ5ZGYtYTQ1Mi02MDE3MGMxNDQ3MTU=',
                'start_situation__list': {'down': 0.0, 'clock': '7:35',
                                          'location': 'e6aa13a4-0055-48a9-bc41-be28dc106929',
                                          'yfd': 0.0,
                                          'possession': 'e6aa13a4-0055-48a9-bc41-be28dc106929'},
                'game__id': '63b4d374-9c7c-416e-8aa9-456e22a36af6',
                'alt_description': 'M.Bosher kicks 69 yards from ATL 35 to TEN -4. T.McBride to TEN 25 for 29 yards (K.White).',
                'home_points': 31.0, 'parent_api__id': 'pbp', 'statistics__list': {
                'kick__list': {'confirmed': 'true', 'yards': 69.0, 'endzone': 1.0, 'attempt': 1.0,
                               'team': 'e6aa13a4-0055-48a9-bc41-be28dc106929',
                               'player': '947ba5a9-71de-4cc5-839a-884cfa49544b'},
                'defense__list': {'confirmed': 'true', 'tackle': 1.0,
                                  'team': 'e6aa13a4-0055-48a9-bc41-be28dc106929',
                                  'player': 'aada7f5b-2b2b-456f-a3fa-7b834dbdb52b'},
                'return__list': {'return': 1.0, 'yards': 29.0, 'category': 'kick_return',
                                 'confirmed': 'true',
                                 'team': 'd26a1ca5-722d-4274-8f97-c92e49c96315',
                                 'player': '24779156-67f5-45ac-a73e-09184d4d314a'}},
                'id': '9098ec62-d4c2-49df-a452-60170c144715',
                'parent_list__id': 'play_by_play__list', 'clock': '7:35',
                'play_clock': 5.0, 'sequence': 3493.0,
                'drive__id': 'a57e7fa9-cc2a-4eb4-8934-948107e73fd6',
                'type': 'kickoff'}
        self.__parse_and_send(play, (sport_db + '.' + 'play', parent_api))

    def test_5(self):
        """ pass example that shows a QB sack """
        sport_db = 'nflo'
        parent_api = 'pbp'

        start_location = {
            '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDAxNDFhMGE1LTEzZTUtNGIyOC1iMTlmLTBjMzkyM2FhZWY2ZXF1YXJ0ZXJfX2lkZmQzMTM2OGItYTE1OS00ZjU2LWEwMjItYWZjNjkxZTM0NzU1cGFyZW50X2xpc3RfX2lkc3RhcnRfc2l0dWF0aW9uX19saXN0ZHJpdmVfX2lkYTk1NmQ5Y2ItZDhhYi00MDhjLTkxZmMtNDQyZjA2ZTMzOGZmcGxheV9faWQ1NTZiMzE4YS1mOTQ0LTRiMzctODZkZC00YjBkYmE0ZDA2NDRpZDQ4MDllY2IwLWFiZDMtNDUxZC05YzRhLTkyYTkwYjgzY2EwNg==',
            'play__id': '556b318a-f944-4b37-86dd-4b0dba4d0644',
            'game__id': '0141a0a5-13e5-4b28-b19f-0c3923aaef6e',
            'market': 'Miami', 'yardline': 26.0,
            'quarter__id': 'fd31368b-a159-4f56-a022-afc691e34755',
            'reference': 4958.0, 'alias': 'MIA', 'id': '4809ecb0-abd3-451d-9c4a-92a90b83ca06',
            'drive__id': 'a956d9cb-d8ab-408c-91fc-442f06e338ff', 'name': 'Dolphins',
            'dd_updated__id': 1464841517401,
            'parent_api__id': 'pbp', 'parent_list__id': 'start_situation__list'}
        self.__parse_and_send(start_location, (sport_db + '.' + 'location', parent_api))

        start_possession = {
            '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDAxNDFhMGE1LTEzZTUtNGIyOC1iMTlmLTBjMzkyM2FhZWY2ZXF1YXJ0ZXJfX2lkZmQzMTM2OGItYTE1OS00ZjU2LWEwMjItYWZjNjkxZTM0NzU1cGFyZW50X2xpc3RfX2lkc3RhcnRfc2l0dWF0aW9uX19saXN0ZHJpdmVfX2lkYTk1NmQ5Y2ItZDhhYi00MDhjLTkxZmMtNDQyZjA2ZTMzOGZmcGxheV9faWQ1NTZiMzE4YS1mOTQ0LTRiMzctODZkZC00YjBkYmE0ZDA2NDRpZDIyMDUyZmY3LWMwNjUtNDJlZS1iYzhmLWM0NjkxYzUwZTYyNA==',
            'play__id': '556b318a-f944-4b37-86dd-4b0dba4d0644',
            'game__id': '0141a0a5-13e5-4b28-b19f-0c3923aaef6e',
            'market': 'Washington', 'reference': 4971.0,
            'quarter__id': 'fd31368b-a159-4f56-a022-afc691e34755',
            'name': 'Redskins', 'alias': 'WAS', 'id': '22052ff7-c065-42ee-bc8f-c4691c50e624',
            'drive__id': 'a956d9cb-d8ab-408c-91fc-442f06e338ff', 'dd_updated__id': 1464841517401,
            'parent_api__id': 'pbp', 'parent_list__id': 'start_situation__list'}
        self.__parse_and_send(start_possession, (sport_db + '.' + 'possession', parent_api))

        end_location = {
            '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDAxNDFhMGE1LTEzZTUtNGIyOC1iMTlmLTBjMzkyM2FhZWY2ZXF1YXJ0ZXJfX2lkZmQzMTM2OGItYTE1OS00ZjU2LWEwMjItYWZjNjkxZTM0NzU1cGFyZW50X2xpc3RfX2lkZW5kX3NpdHVhdGlvbl9fbGlzdGRyaXZlX19pZGE5NTZkOWNiLWQ4YWItNDA4Yy05MWZjLTQ0MmYwNmUzMzhmZnBsYXlfX2lkNTU2YjMxOGEtZjk0NC00YjM3LTg2ZGQtNGIwZGJhNGQwNjQ0aWQ0ODA5ZWNiMC1hYmQzLTQ1MWQtOWM0YS05MmE5MGI4M2NhMDY=',
            'play__id': '556b318a-f944-4b37-86dd-4b0dba4d0644',
            'game__id': '0141a0a5-13e5-4b28-b19f-0c3923aaef6e',
            'market': 'Miami', 'yardline': 34.0,
            'quarter__id': 'fd31368b-a159-4f56-a022-afc691e34755',
            'reference': 4958.0, 'alias': 'MIA', 'id': '4809ecb0-abd3-451d-9c4a-92a90b83ca06',
            'drive__id': 'a956d9cb-d8ab-408c-91fc-442f06e338ff', 'name': 'Dolphins',
            'dd_updated__id': 1464841517401,
            'parent_api__id': 'pbp', 'parent_list__id': 'end_situation__list'}
        self.__parse_and_send(end_location, (sport_db + '.' + 'location', parent_api))

        end_possession = {
            '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDAxNDFhMGE1LTEzZTUtNGIyOC1iMTlmLTBjMzkyM2FhZWY2ZXF1YXJ0ZXJfX2lkZmQzMTM2OGItYTE1OS00ZjU2LWEwMjItYWZjNjkxZTM0NzU1cGFyZW50X2xpc3RfX2lkZW5kX3NpdHVhdGlvbl9fbGlzdGRyaXZlX19pZGE5NTZkOWNiLWQ4YWItNDA4Yy05MWZjLTQ0MmYwNmUzMzhmZnBsYXlfX2lkNTU2YjMxOGEtZjk0NC00YjM3LTg2ZGQtNGIwZGJhNGQwNjQ0aWQyMjA1MmZmNy1jMDY1LTQyZWUtYmM4Zi1jNDY5MWM1MGU2MjQ=',
            'play__id': '556b318a-f944-4b37-86dd-4b0dba4d0644',
            'game__id': '0141a0a5-13e5-4b28-b19f-0c3923aaef6e',
            'market': 'Washington', 'reference': 4971.0,
            'quarter__id': 'fd31368b-a159-4f56-a022-afc691e34755',
            'name': 'Redskins', 'alias': 'WAS', 'id': '22052ff7-c065-42ee-bc8f-c4691c50e624',
            'drive__id': 'a956d9cb-d8ab-408c-91fc-442f06e338ff', 'dd_updated__id': 1464841517401,
            'parent_api__id': 'pbp', 'parent_list__id': 'end_situation__list'}
        self.__parse_and_send(end_possession, (sport_db + '.' + 'possession', parent_api))

        play = {
            '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDAxNDFhMGE1LTEzZTUtNGIyOC1iMTlmLTBjMzkyM2FhZWY2ZXF1YXJ0ZXJfX2lkZmQzMTM2OGItYTE1OS00ZjU2LWEwMjItYWZjNjkxZTM0NzU1cGFyZW50X2xpc3RfX2lkcGxheV9ieV9wbGF5X19saXN0ZHJpdmVfX2lkYTk1NmQ5Y2ItZDhhYi00MDhjLTkxZmMtNDQyZjA2ZTMzOGZmaWQ1NTZiMzE4YS1mOTQ0LTRiMzctODZkZC00YjBkYmE0ZDA2NDQ=',
            'away_points': 0.0,
            'end_situation__list': {'location': '4809ecb0-abd3-451d-9c4a-92a90b83ca06', 'yfd': 18.0,
                                    'possession': '22052ff7-c065-42ee-bc8f-c4691c50e624',
                                    'down': 2.0, 'clock': '9:00'},
            'alt_description': '(9:40) K.Cousins sacked at MIA 34 for -8 yards (J.Phillips).',
            'play_clock': 6.0,
            'clock': '9:40', 'game__id': '0141a0a5-13e5-4b28-b19f-0c3923aaef6e', 'reference': 315.0,
            'quarter__id': 'fd31368b-a159-4f56-a022-afc691e34755', 'type': 'pass',
            'drive__id': 'a956d9cb-d8ab-408c-91fc-442f06e338ff', 'home_points': 0.0,
            'id': '556b318a-f944-4b37-86dd-4b0dba4d0644',
            'start_situation__list': {'location': '4809ecb0-abd3-451d-9c4a-92a90b83ca06',
                                      'yfd': 10.0,
                                      'possession': '22052ff7-c065-42ee-bc8f-c4691c50e624',
                                      'down': 1.0,
                                      'clock': '9:40'},
            'description': '(9:40) 8-K.Cousins sacked at MIA 34 for -8 yards (97-J.Phillips).',
            'wall_clock': '2015-09-13T17:09:46+00:00', 'sequence': 315.0,
            'dd_updated__id': 1464841517401,
            'statistics__list': {
                'pass__list': {'sack': 1.0, 'goaltogo': 0.0,
                               'team': '22052ff7-c065-42ee-bc8f-c4691c50e624',
                               'sack_yards': -8.0, 'player': 'bbd0942c-6f77-4f83-a6d0-66ec6548019e',
                               'inside_20': 0.0,
                               'confirmed': 'true'},
                'defense__list': {'sack': 1.0, 'tlost': 1.0, 'tlost_yards': 8.0, 'qb_hit': 1.0,
                                  'player': '023af11a-3aa1-4266-b163-31cf6369ef3b',
                                  'team': '4809ecb0-abd3-451d-9c4a-92a90b83ca06',
                                  'sack_yards': -8.0, 'tackle': 1.0,
                                  'confirmed': 'true'}}, 'parent_api__id': 'pbp',
            'parent_list__id': 'play_by_play__list'}
        self.__parse_and_send(play, (sport_db + '.' + 'play', parent_api))

    def test_10(self):
        sport_db = 'nflo'
        parent_api = 'pbp'

        start_location = {'parent_list__id': 'start_situation__list',
                          'id': '97354895-8c77-4fd4-a860-32e62ea7382a',
                          'game__id': 'acbb3001-6bb6-41ce-9e91-942abd284e4c',
                          'market': 'New England',
                          'reference': 4960.0,
                          'quarter__id': '8075b247-bb26-4f49-a342-968f04835d2d',
                          'dd_updated__id': 1464842199562, 'alias': 'NE', 'name': 'Patriots',
                          'play__id': 'da1dbdf1-b501-48dd-a728-72b9d8f31ec8',
                          '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZGFjYmIzMDAxLTZiYjYtNDFjZS05ZTkxLTk0MmFiZDI4NGU0Y3F1YXJ0ZXJfX2lkODA3NWIyNDctYmIyNi00ZjQ5LWEzNDItOTY4ZjA0ODM1ZDJkcGFyZW50X2xpc3RfX2lkc3RhcnRfc2l0dWF0aW9uX19saXN0ZHJpdmVfX2lkMjFkZGViN2QtMTNmYS00YjgxLWJiMWYtZDA4MDQ4NDFlMDk3cGxheV9faWRkYTFkYmRmMS1iNTAxLTQ4ZGQtYTcyOC03MmI5ZDhmMzFlYzhpZDk3MzU0ODk1LThjNzctNGZkNC1hODYwLTMyZTYyZWE3MzgyYQ==',
                          'yardline': 35.0, 'parent_api__id': 'pbp',
                          'drive__id': '21ddeb7d-13fa-4b81-bb1f-d0804841e097'}
        self.__parse_and_send(start_location, (sport_db + '.' + 'location', parent_api))

        start_possession = {'parent_list__id': 'start_situation__list',
                            'id': '97354895-8c77-4fd4-a860-32e62ea7382a',
                            'game__id': 'acbb3001-6bb6-41ce-9e91-942abd284e4c',
                            'market': 'New England',
                            'reference': 4960.0,
                            'quarter__id': '8075b247-bb26-4f49-a342-968f04835d2d',
                            'dd_updated__id': 1464842199562, 'alias': 'NE', 'name': 'Patriots',
                            'play__id': 'da1dbdf1-b501-48dd-a728-72b9d8f31ec8',
                            '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZGFjYmIzMDAxLTZiYjYtNDFjZS05ZTkxLTk0MmFiZDI4NGU0Y3F1YXJ0ZXJfX2lkODA3NWIyNDctYmIyNi00ZjQ5LWEzNDItOTY4ZjA0ODM1ZDJkcGFyZW50X2xpc3RfX2lkc3RhcnRfc2l0dWF0aW9uX19saXN0ZHJpdmVfX2lkMjFkZGViN2QtMTNmYS00YjgxLWJiMWYtZDA4MDQ4NDFlMDk3cGxheV9faWRkYTFkYmRmMS1iNTAxLTQ4ZGQtYTcyOC03MmI5ZDhmMzFlYzhpZDk3MzU0ODk1LThjNzctNGZkNC1hODYwLTMyZTYyZWE3MzgyYQ==',
                            'parent_api__id': 'pbp',
                            'drive__id': '21ddeb7d-13fa-4b81-bb1f-d0804841e097'}
        self.__parse_and_send(start_possession, (sport_db + '.' + 'possession', parent_api))

        end_location = {'parent_list__id': 'end_situation__list',
                        'id': 'cb2f9f1f-ac67-424e-9e72-1475cb0ed398',
                        'game__id': 'acbb3001-6bb6-41ce-9e91-942abd284e4c', 'market': 'Pittsburgh',
                        'reference': 4966.0,
                        'quarter__id': '8075b247-bb26-4f49-a342-968f04835d2d',
                        'dd_updated__id': 1464842199562,
                        'alias': 'PIT', 'name': 'Steelers',
                        'play__id': 'da1dbdf1-b501-48dd-a728-72b9d8f31ec8',
                        '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZGFjYmIzMDAxLTZiYjYtNDFjZS05ZTkxLTk0MmFiZDI4NGU0Y3F1YXJ0ZXJfX2lkODA3NWIyNDctYmIyNi00ZjQ5LWEzNDItOTY4ZjA0ODM1ZDJkcGFyZW50X2xpc3RfX2lkZW5kX3NpdHVhdGlvbl9fbGlzdGRyaXZlX19pZDIxZGRlYjdkLTEzZmEtNGI4MS1iYjFmLWQwODA0ODQxZTA5N3BsYXlfX2lkZGExZGJkZjEtYjUwMS00OGRkLWE3MjgtNzJiOWQ4ZjMxZWM4aWRjYjJmOWYxZi1hYzY3LTQyNGUtOWU3Mi0xNDc1Y2IwZWQzOTg=',
                        'yardline': 20.0, 'parent_api__id': 'pbp',
                        'drive__id': '21ddeb7d-13fa-4b81-bb1f-d0804841e097'}
        self.__parse_and_send(end_location, (sport_db + '.' + 'location', parent_api))

        end_possession = {'parent_list__id': 'end_situation__list',
                          'id': 'cb2f9f1f-ac67-424e-9e72-1475cb0ed398',
                          'game__id': 'acbb3001-6bb6-41ce-9e91-942abd284e4c',
                          'market': 'Pittsburgh',
                          'reference': 4966.0,
                          'quarter__id': '8075b247-bb26-4f49-a342-968f04835d2d',
                          'dd_updated__id': 1464842199562, 'alias': 'PIT', 'name': 'Steelers',
                          'play__id': 'da1dbdf1-b501-48dd-a728-72b9d8f31ec8',
                          '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZGFjYmIzMDAxLTZiYjYtNDFjZS05ZTkxLTk0MmFiZDI4NGU0Y3F1YXJ0ZXJfX2lkODA3NWIyNDctYmIyNi00ZjQ5LWEzNDItOTY4ZjA0ODM1ZDJkcGFyZW50X2xpc3RfX2lkZW5kX3NpdHVhdGlvbl9fbGlzdGRyaXZlX19pZDIxZGRlYjdkLTEzZmEtNGI4MS1iYjFmLWQwODA0ODQxZTA5N3BsYXlfX2lkZGExZGJkZjEtYjUwMS00OGRkLWE3MjgtNzJiOWQ4ZjMxZWM4aWRjYjJmOWYxZi1hYzY3LTQyNGUtOWU3Mi0xNDc1Y2IwZWQzOTg=',
                          'parent_api__id': 'pbp',
                          'drive__id': '21ddeb7d-13fa-4b81-bb1f-d0804841e097'}
        self.__parse_and_send(end_possession, (sport_db + '.' + 'possession', parent_api))

        play = {'parent_list__id': 'play_by_play__list',
                'id': 'da1dbdf1-b501-48dd-a728-72b9d8f31ec8',
                'game__id': 'acbb3001-6bb6-41ce-9e91-942abd284e4c',
                'start_situation__list': {'down': 0.0,
                                          'possession': '97354895-8c77-4fd4-a860-32e62ea7382a',
                                          'location': '97354895-8c77-4fd4-a860-32e62ea7382a',
                                          'yfd': 0.0,
                                          'clock': '15:00'}, 'reference': 36.0,
                'quarter__id': '8075b247-bb26-4f49-a342-968f04835d2d',
                'dd_updated__id': 1464842199562,
                'statistics__list': {
                    'return__list': {'team': 'cb2f9f1f-ac67-424e-9e72-1475cb0ed398',
                                     'confirmed': 'true',
                                     'touchback': 1.0, 'category': 'kick_return'},
                    'kick__list': {'gross_yards': 74.0, 'confirmed': 'true', 'touchback': 1.0,
                                   'attempt': 1.0,
                                   'team': '97354895-8c77-4fd4-a860-32e62ea7382a',
                                   'player': 'a527b7db-0b52-4379-9e4c-2e08c1fe1bed',
                                   'yards': 65.0}},
                'alt_description': 'S.Gostkowski kicks 65 yards from NE 35 to end zone, Touchback.',
                'wall_clock': '2015-09-11T00:41:06+00:00', 'type': 'kickoff', 'home_points': 0.0,
                'end_situation__list': {'down': 1.0,
                                        'possession': 'cb2f9f1f-ac67-424e-9e72-1475cb0ed398',
                                        'location': 'cb2f9f1f-ac67-424e-9e72-1475cb0ed398',
                                        'yfd': 10.0,
                                        'clock': '15:00'}, 'sequence': 36.0, 'away_points': 0.0,
                '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZGFjYmIzMDAxLTZiYjYtNDFjZS05ZTkxLTk0MmFiZDI4NGU0Y3F1YXJ0ZXJfX2lkODA3NWIyNDctYmIyNi00ZjQ5LWEzNDItOTY4ZjA0ODM1ZDJkcGFyZW50X2xpc3RfX2lkcGxheV9ieV9wbGF5X19saXN0ZHJpdmVfX2lkMjFkZGViN2QtMTNmYS00YjgxLWJiMWYtZDA4MDQ4NDFlMDk3aWRkYTFkYmRmMS1iNTAxLTQ4ZGQtYTcyOC03MmI5ZDhmMzFlYzg=',
                'drive__id': '21ddeb7d-13fa-4b81-bb1f-d0804841e097',
                'description': '3-S.Gostkowski kicks 65 yards from NE 35 to end zone, Touchback.',
                'parent_api__id': 'pbp', 'clock': '15:00'}
        self.__parse_and_send(play, (sport_db + '.' + 'play', parent_api))

    def test_player_names(self):
        """
        Test that player names are being added to the parser output data.
        :return:
        """

        sport_db = 'nflo'
        parent_api = 'pbp'

        player = mommy.make(
            Player,
            srid=PbpMockData.sack_play['statistics__list']['pass__list']['player'],
            make_m2m=True
        )

        player_stats = mommy.make(
            PlayerStats,
            srid_game=PbpMockData.sack_play['game__id'],
            srid_player=player.srid,
            make_m2m=True,
        )
        player_stats.player = player
        player_stats.save()

        self.assertEqual(
            player_stats.player.srid,
            PbpMockData.sack_play['statistics__list']['pass__list']['player']
        )

        parser = self.__parse_and_send(PbpMockData.sack_play, (sport_db + '.' + 'play', parent_api))
        parser.send()
        sent_data = parser.get_send_data()
        # for NFL, We can also use `parser.send_data`. None of the others
        # are setting their sent data in a local state yet.

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
        # Ensure home + away scores are in PBP
        self.assertEqual(
            sent_data['pbp']['away_points'],
            PbpMockData.sack_play['away_points']
        )
        self.assertEqual(
            sent_data['pbp']['home_points'],
            PbpMockData.sack_play['home_points']
        )

    def test_fp_value_pass_play(self):
        """
        Test that player names are being added to the parser output data.
        :return:
        """
        sport_db = 'nflo'
        parent_api = 'pbp'

        parser = self.__parse_and_send(PbpMockData.pass_play, (sport_db + '.' + 'play', parent_api))

        parser.send()
        sent_data = parser.get_send_data()

        # These are hard-coded stat value calculations, so if we ever change the value of
        # statPoints, these will fail (and that's probably fine)
        self.assertEqual(sent_data['pbp']['statistics']['pass__list']['fp_value'], .16)
        self.assertEqual(sent_data['pbp']['statistics']['receive__list']['fp_value'], .9)

        # check the fp_values dict
        pass_player_srid = sent_data['pbp']['statistics']['pass__list']['player']
        self.assertEqual(
            sent_data['fp_values'][pass_player_srid], .16)
        recieve_player_srid = sent_data['pbp']['statistics']['receive__list']['player']
        self.assertEqual(
            sent_data['fp_values'][recieve_player_srid], .9)


    def test_fp_value_pass_intercepted(self):
        sport_db = 'nflo'
        parent_api = 'pbp'

        parser = self.__parse_and_send(PbpMockData.interception_pass, (sport_db + '.' + 'play', parent_api))

        parser.send()
        sent_data = parser.get_send_data()

        # These are hard-coded stat value calculations, so if we ever change the value of
        # statPoints, these will fail (and that's probably fine)
        self.assertEqual(sent_data['pbp']['statistics']['pass__list']['fp_value'], -1)
        self.assertEqual(sent_data['pbp']['statistics']['receive__list']['fp_value'], 0)

    def test_fp_value_pass_incomplete(self):
        sport_db = 'nflo'
        parent_api = 'pbp'

        parser = self.__parse_and_send(PbpMockData.incomplete_pass, (sport_db + '.' + 'play', parent_api))

        parser.send()
        sent_data = parser.get_send_data()

        # These are hard-coded stat value calculations, so if we ever change the value of
        # statPoints, these will fail (and that's probably fine)
        self.assertEqual(sent_data['pbp']['statistics']['pass__list']['fp_value'], 0)
        self.assertEqual(sent_data['pbp']['statistics']['receive__list']['fp_value'], 0)

    def test_fp_value_qb_sneak(self):
        sport_db = 'nflo'
        parent_api = 'pbp'

        parser = self.__parse_and_send(PbpMockData.qb_sneak, (sport_db + '.' + 'play', parent_api))

        parser.send()
        sent_data = parser.get_send_data()

        # These are hard-coded stat value calculations, so if we ever change the value of
        # statPoints, these will fail (and that's probably fine)
        self.assertEqual(sent_data['pbp']['statistics']['rush__list']['fp_value'], .9)

    def test_pbp_has_necessary_fields(self):
        """
        A quick test to make sure that these various fields exist in the pbp object.
        :return:
        """
        sport_db = 'nflo'
        parent_api = 'pbp'

        parser = self.__parse_and_send(PbpMockData.pass_play, (sport_db + '.' + 'play', parent_api))

        parser.send()
        sent_data = parser.get_send_data()

        self.assertIsNotNone(sent_data['pbp']['statistics'])
        self.assertIsNotNone(sent_data['pbp']['start_situation'])
        self.assertIsNotNone(sent_data['pbp']['description'])
        self.assertIsNotNone(sent_data['pbp']['away_points'])
        self.assertIsNotNone(sent_data['pbp']['home_points'])
        self.assertIsNotNone(sent_data['pbp']['extra_info'])
        self.assertIsNotNone(sent_data['pbp']['type'])
        self.assertIsNotNone(sent_data['game'])
        self.assertIsNotNone(sent_data['stats'])

    def test_pbp_has_participating_players(self):
        """
        A quick test to make sure that the  'players' key gets filled in with all participating
        players.
        :return:
        """
        sport_db = 'nflo'
        parent_api = 'pbp'

        player_1 = mommy.make(
            Player,
            srid=PbpMockData.pass_play['statistics__list']['pass__list']['player'],
            first_name = 'p1_first',
            last_name = 'p1_last'
        )
        player_2 = mommy.make(
            Player,
            srid=PbpMockData.pass_play['statistics__list']['receive__list']['player'],
            first_name='p2_first',
            last_name='p2_last'
        )

        parser = self.__parse_and_send(PbpMockData.pass_play, (sport_db + '.' + 'play', parent_api))

        parser.send()
        sent_data = parser.get_send_data()
        # from pprint import pprint
        # pprint(sent_data)

        self.assertIsNotNone(sent_data['players'])
        self.assertEqual(2, len(sent_data['players']))


    def test_game_info(self):
        sport_db = 'nflo'
        parent_api = 'pbp'
        """
        Make sure that game info is being added into the 'game' attribute of the pbp. 
        """
        # Create some teams and a game.
        home_team = mommy.make(
            sports.nfl.models.Team,
            alias="DEN"
        )
        away_team = mommy.make(
            sports.nfl.models.Team,
            alias="SLC"
        )
        game = mommy.make(
            sports.nfl.models.Game,
            srid=PbpMockData.sack_play['game__id'],
            srid_home=home_team.srid,
            home=home_team,
            srid_away=away_team.srid,
            away=away_team,
            make_m2m=True,
        )

        # Create a boxscore so we can embed quarter info.
        game_boxscore = mommy.make(
            GameBoxscore,
            srid_game=game.srid,
            quarter='3',
        )

        # Parse the event
        parser = self.__parse_and_send(PbpMockData.sack_play, (sport_db + '.' + 'play', parent_api))
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

        # check that the quarter info is being linked to the parsed pbp
        self.assertEqual(
            str(sent_data['game']['period']),
            str(game_boxscore.quarter)
        )


class GameStatusChangedSignal(AbstractTest):
    @staticmethod
    def __create_team(alias, market):
        team = Team()
        team.srid = 'test-srid-' + alias
        team.alias = alias
        team.market = market

        team.srid_league = '4353138d-4c22-4396-95d8-5f587d2df25c'
        team.srid_conference = '3960cfac-7361-4b30-bc25-8d393de6f62f'
        team.srid_division = '54dc7348-c1d2-40d8-88b3-c4c0138e085d'
        team.save()
        return team

    def setUp(self):
        super().setUp()
        self.SCHEDULED = 'scheduled'  # the default game status
        self.COMPLETE = 'complete'  # made up - does not actually reflect a real status, necessarily

        self.home = self.__create_team('alias-home', 'market-home')
        self.away = self.__create_team('alias-away', 'market-away')

        self.game = Game()

        self.game.season, created = Season.objects.get_or_create(srid='nflsrid', season_year=2015,
                                                                 season_type='reg')
        self.game.srid = '%s--test--%s' % (self.away.srid, self.home.srid)

        self.game.home = self.home
        self.game.srid_home = self.home.srid

        self.game.away = self.away
        self.game.srid_away = self.away.srid

        self.game.title = 'testing game for status change signal'
        self.game.weather_json = '{}'
        self.game.start = timezone.now()

        self.game.status = self.SCHEDULED

        self.game.save()

    def test_signal_sent_on_game_status_changed(self):
        self.game.status = self.COMPLETE
        self.game.save()


# class DstPlayerCreation(AbstractTest):
#     """
#     Ensure that the nfl teams DST player objects get created
#     when a new team is created.
#     """
#     def setUp(self):
#         self.srid_team  = 'TEST'            # default team srid/alias
#         self.player     = None
#
#     def create_team(self, srid):
#         t = Team()
#         t.srid          = srid
#         t.srid_venue    = srid + 'venue'    # doesnt have to be real for this test
#         t.name          = 'Test Team'       # doesnt have to be valid
#         t.alias         = srid              # alias is the id for nfl teams
#         t.save() # this save should create dst Player object via signal
#         return t
#
#     def get_dst_player(self, srid_team):
#         return Player.objects.get(srid=srid_team)
#
#     def test_dst_player_is_created_when_new_team_is_saved(self):
#         # it shouldnt exist now, and SHOULD throw DoesNotExist
#         self.assertRaises(Player.DoesNotExist, lambda: self.get_dst_player(srid_team=self.srid_team) )
#
#         # now create the Team object, and check again
#         t = self.create_team( self.srid_team )
#         try:
#             self.player = self.get_dst_player( srid_team=self.srid_team )
#         except:
#             self.player = None
#
#         self.assertIsNotNone( self.player )
#         self.assertEquals( self.srid_team, t.srid )

class SeasonScheduleParserTest(AbstractTest):
    """
    tests sports.nfl.parser.SeasonSchedule
    """

    def setUp(self):
        super().setUp()
        self.sport = 'nflo'
        self.obj_str = """{'_id': 'cGFyZW50X2FwaV9faWRzY2hlZHVsZWlkNjU5ZDJiZDAtYzQzZS00YmIwLTg1MDMtOWQ1NzY5MTFkMDI5',
            'dd_updated__id': 1471578967708,
            'id': '659d2bd0-c43e-4bb0-8503-9d576911d029',
            'name': 'PRE',
            'parent_api__id': 'schedule',
            'type': 'PRE',
            'weeks': [{'week': '60bfeef5-51db-4e2f-bb85-377a6386ac6d'},
             {'week': '1d810a06-3f3b-4865-a0ba-f28091dd8d6f'},
             {'week': '79300bc5-2fc5-489a-9d4f-ef641e6f5885'},
             {'week': '051e133e-75ef-4818-835a-87e84fdc53b2'},
             {'week': 'acd0b2ac-8d64-4eac-8f34-365b807e996d'}],
            'xmlns': 'http://feed.elasticstats.com/schema/nfl/premium/schedule-v2.0.xsd',
            'year': 2016.0
        }"""
        self.season_parser = SeasonSchedule()

    def test_pst_season(self):
        obj = literal_eval(self.obj_str)
        srid = obj.get(SeasonSchedule.field_srid)  # the srid will be found in the 'id' field
        obj_season_year = obj.get(SeasonSchedule.field_season_year)
        obj_season_type = obj.get(SeasonSchedule.field_season_type)
        oplog_obj = OpLogObjWrapper(self.sport, 'season', obj)
        self.season_parser.parse(oplog_obj)
        season = sports.nfl.models.Season.objects.get(srid=srid)

        self.assertEquals(season.season_year, obj_season_year)
        self.assertEquals(season.season_type, obj_season_type.lower())


class GameScheduleParserTest(AbstractTest):
    """
    tests sports.nfl.parser.GameSchedule -- the parser for sports.nfl.models.Game objects

    effectively tests the TeamHierarchy parser too
    """

    def setUp(self):
        super().setUp()
        self.sport = 'nflo'

    # def setUp(self):
    #     self.sport = 'nfl'
    #     self.season_str = """{'season': 2015.0, 'xmlns': 'http://feed.elasticstats.com/schema/nfl/schedule-v1.0.xsd', 'id': 'http://api.sportsdatallc.org/nfl-rt1/2015/PRE/schedule.xml', 'weeks': [{'week': {'week': 0.0, 'game': 'b5b6dcbf-3e3b-4e0c-9eaf-ba978545dcaf'}}, {'week': {'week': 1.0, 'games': [{'game': 'e0b0b391-8d15-4b81-b0fc-aa148b8713fc'}, {'game': '0ed4c4ee-f594-4e10-b156-0799062a94c8'}, {'game': 'e237815c-78eb-4960-a1cf-0dbf98908255'}, {'game': '346b5340-e0a8-42de-a2c7-13b83041b9d3'}, {'game': '4a66009c-c873-47a7-af96-2b28b75ff6da'}, {'game': '7875bd80-22ae-44b1-bd6b-6672de6359a9'}, {'game': '63b4d374-9c7c-416e-8aa9-456e22a36af6'}, {'game': '45bafeba-5f30-4d56-a504-02fa3ede6b5d'}, {'game': '19f6b700-3c8f-4783-899e-e348d572bfbe'}, {'game': 'b4dda772-c8cf-4a0d-8b1a-8cee09ebc0d7'}, {'game': 'f0c8a8ec-3c8f-484c-be72-28029a885c80'}, {'game': 'acdd07a4-a86b-4a86-8e3e-7cc26321b936'}, {'game': '8a215abc-52bc-439f-9718-f8b6810e5fe4'}, {'game': '28deac36-f997-4774-a820-83f85627bce1'}, {'game': 'b35b0d8d-b77c-4503-8339-8f48fb9239a4'}, {'game': '5bd30dc8-35b2-4c2b-9ba6-8cb1e9eecec5'}]}}, {'week': {'week': 2.0, 'games': []}}], 'type': 'PRE', 'dd_updated__id': 1456974034293, 'parent_api__id': 'schedule', '_id': 'cGFyZW50X2FwaV9faWRzY2hlZHVsZWlkaHR0cDovL2FwaS5zcG9ydHNkYXRhbGxjLm9yZy9uZmwtcnQxLzIwMTUvUFJFL3NjaGVkdWxlLnhtbA=='}"""
    #     self.away_team_str = """{'parent_api__id': 'hierarchy', 'market': 'Pittsburgh', 'league__id': 'NFL', 'conference__id': 'AFC', 'venue': '7349a2e6-0ac9-410b-8bd2-ca58c9f7aa34', 'division__id': 'AFC_NORTH', 'id': 'PIT', 'dd_updated__id': 1456973389372, 'name': 'Steelers', '_id': 'cGFyZW50X2FwaV9faWRoaWVyYXJjaHlsZWFndWVfX2lkTkZMY29uZmVyZW5jZV9faWRBRkNkaXZpc2lvbl9faWRBRkNfTk9SVEhpZFBJVA=='}"""
    #     self.home_team_str = """{'parent_api__id': 'hierarchy', 'market': 'Jacksonville', 'league__id': 'NFL', 'conference__id': 'AFC', 'venue': '4c5c036d-dd3d-4183-b595-71a43a97560f', 'division__id': 'AFC_SOUTH', 'id': 'JAC', 'dd_updated__id': 1456973389372, 'name': 'Jaguars', '_id': 'cGFyZW50X2FwaV9faWRoaWVyYXJjaHlsZWFndWVfX2lkTkZMY29uZmVyZW5jZV9faWRBRkNkaXZpc2lvbl9faWRBRkNfU09VVEhpZEpBQw=='}"""
    #     self.game_str = """{'parent_api__id': 'schedule', 'season__id': 'http://api.sportsdatallc.org/nfl-rt1/2015/PRE/schedule.xml', 'away': 'PIT', 'scheduled': '2015-08-14T23:30:00+00:00', 'home_rotation': '', 'away_rotation': '', 'dd_updated__id': 1456974034293, '_id': 'cGFyZW50X2FwaV9faWRzY2hlZHVsZXNlYXNvbl9faWRodHRwOi8vYXBpLnNwb3J0c2RhdGFsbGMub3JnL25mbC1ydDEvMjAxNS9QUkUvc2NoZWR1bGUueG1saWQxOWY2YjcwMC0zYzhmLTQ3ODMtODk5ZS1lMzQ4ZDU3MmJmYmU=', 'id': '19f6b700-3c8f-4783-899e-e348d572bfbe', 'weather__list': {'humidity': 49.0, 'wind__list': {'direction': 'NE', 'speed': 14.0}, 'condition': 'Partly Cloudy ', 'temperature': 90.0}, 'status': 'closed', 'broadcast__list': {'network': '', 'satellite': '', 'cable': '', 'internet': ''}, 'home': 'JAC', 'links__list': [{'link': {'rel': 'statistics', 'href': '/2015/PRE/1/PIT/JAC/statistics.xml', 'type': 'application/xml'}}, {'link': {'rel': 'summary', 'href': '/2015/PRE/1/PIT/JAC/summary.xml', 'type': 'application/xml'}}, {'link': {'rel': 'pbp', 'href': '/2015/PRE/1/PIT/JAC/pbp.xml', 'type': 'application/xml'}}, {'link': {'rel': 'boxscore', 'href': '/2015/PRE/1/PIT/JAC/boxscore.xml', 'type': 'application/xml'}}, {'link': {'rel': 'roster', 'href': '/2015/PRE/1/PIT/JAC/roster.xml', 'type': 'application/xml'}}, {'link': {'rel': 'injuries', 'href': '/2015/PRE/1/PIT/JAC/injuries.xml', 'type': 'application/xml'}}, {'link': {'rel': 'depthchart', 'href': '/2015/PRE/1/PIT/JAC/depthchart.xml', 'type': 'application/xml'}}], 'venue': '4c5c036d-dd3d-4183-b595-71a43a97560f'}"""
    #
    #     self.season_parser = SeasonSchedule()
    #     self.away_team_parser = TeamHierarchy()
    #     self.home_team_parser = TeamHierarchy()
    #     self.game_parser = GameSchedule()
    #
    # def test_game_schedule_parse(self):
    #     """
    #     as a prerequisite, parse the seasonschedule, and both home & away teams
    #     """
    #     # parse the season_schedule obj
    #     season_oplog_obj = OpLogObjWrapper(self.sport,'season',literal_eval(self.season_str))
    #     self.season_parser.parse( season_oplog_obj )
    #     self.assertEquals( 1, sports.nfl.models.Season.objects.filter(season_year=2015,season_type='pre').count() ) # should have parsed 1 thing
    #
    #     away_team_oplog_obj = OpLogObjWrapper(self.sport,'team',literal_eval(self.away_team_str))
    #     self.away_team_parser.parse( away_team_oplog_obj )
    #     self.assertEquals( 1, sports.nfl.models.Team.objects.all().count() ) # should be 1 team in there now
    #
    #     home_team_oplog_obj = OpLogObjWrapper(self.sport,'team',literal_eval(self.home_team_str))
    #     self.home_team_parser.parse( home_team_oplog_obj )
    #     self.assertEquals( 2, sports.nfl.models.Team.objects.all().count() ) # should be 2 teams in there now
    #
    #     # now attempt to parse the game
    #     game_oplog_obj = OpLogObjWrapper(self.sport,'game',literal_eval(self.game_str))
    #     self.game_parser.parse( game_oplog_obj )
    #     self.assertEquals( 1, sports.nfl.models.Game.objects.all().count() )

    def __parse_obj(self, db, coll, data):
        """
        calls DataDenNfl().parse( data ) using the 'db' and 'coll' to create the namespace
        and creates the target using the namespace, and the 'parent_api__id' field from the mongo obj data

        :param db:
        :param coll:
        :param data:
        :return: data passed in
        """
        oplog_obj = OpLogObjWrapper(db, coll, data)
        parser = DataDenNfl()
        parser.parse(oplog_obj)
        return data

    def __parse_obj_str(self, db, coll, obj_str):
        """
        calls DataDenNfl().parse( obj ) after converting 'obj_str' param into a proper object

        db -> the sport, ie: 'nflo'
        coll -> the collection name, ie: 'team', or 'game', etc...
        parent_api -> the feed, ie: 'hierarchy', 'pbp', etc...

        :param obj_str: the unwrapped mongo object

        returns the dict of the original data so we can assert on anything we want to
        """

        data = literal_eval(obj_str)
        # oplog_obj = OpLogObjWrapper(db, coll, data)
        # parser = DataDenNfl()
        # parser.parse(oplog_obj)
        # return data
        return self.__parse_obj(db, coll, data)

    def test_status_change(self):
        """
        parse in a game, and then change the stats from scheduled to inprogress
        and make sure it gets updated.
        """

        # parse a season object (Game objects will require it)
        season_str = """{'_id': 'cGFyZW50X2FwaV9faWRzY2hlZHVsZWlkNjU5ZDJiZDAtYzQzZS00YmIwLTg1MDMtOWQ1NzY5MTFkMDI5',
          'dd_updated__id': 1471578967708,
          'id': '659d2bd0-c43e-4bb0-8503-9d576911d029',
          'name': 'PRE',
          'parent_api__id': 'schedule',
          'type': 'PRE',
          'weeks': [{'week': '60bfeef5-51db-4e2f-bb85-377a6386ac6d'},
           {'week': '1d810a06-3f3b-4865-a0ba-f28091dd8d6f'},
           {'week': '79300bc5-2fc5-489a-9d4f-ef641e6f5885'},
           {'week': '051e133e-75ef-4818-835a-87e84fdc53b2'},
           {'week': 'acd0b2ac-8d64-4eac-8f34-365b807e996d'}],
          'xmlns': 'http://feed.elasticstats.com/schema/nfl/premium/schedule-v2.0.xsd',
          'year': 2016.0}"""
        data = self.__parse_obj_str(self.sport, 'season', season_str)
        qs = sports.nfl.models.Season.objects.filter(srid=data.get('id'))
        self.assertTrue(
            1 <= qs.count())  # should be at least 1, more tests will confirm its the one we expect
        season = qs[0]
        self.assertEquals(data.get('year'), season.season_year)  # the year matches
        self.assertTrue(
            season.season_type in SeasonSchedule.season_types)  # the season type is correct

        # parse a team
        away_team_str = """{'_id': 'cGFyZW50X2FwaV9faWRoaWVyYXJjaHlsZWFndWVfX2lkM2M2ZDMxOGEtNjE2NC00MjkwLTliYmMtYmY5YmIyMWNjNGI4Y29uZmVyZW5jZV9faWRiMTgwOGU1Zi1kNDBiLTQ3YzAtOGFmOC01MTc1YzBmZGNkMjZkaXZpc2lvbl9faWQ2ZGMxOTMzZi1jYTkwLTQ2ZTYtYWFmNy05Yjk1Y2M0NDMwNmFpZGEyMDQ3MWI0LWE4ZDktNDBjNy05NWFkLTkwY2MzMGU0NjkzMg==',
         'alias': 'GB',
         'conference__id': 'b1808e5f-d40b-47c0-8af8-5175c0fdcd26',
         'dd_updated__id': 1471601765520,
         'division__id': '6dc1933f-ca90-46e6-aaf7-9b95cc44306a',
         'id': 'a20471b4-a8d9-40c7-95ad-90cc30e46932',
         'league__id': '3c6d318a-6164-4290-9bbc-bf9bb21cc4b8',
         'market': 'Green Bay',
         'name': 'Packers',
         'parent_api__id': 'hierarchy',
         'references__list': {'reference': 'GB'},
         'venue': '5a60dd3a-302c-41c6-ab0f-dd335c1103c2'}"""
        data = self.__parse_obj_str(self.sport, 'team', away_team_str)
        qs = sports.nfl.models.Team.objects.filter(srid=data.get('id'))
        self.assertTrue(
            1 == qs.count())  # should be at least 1, more tests will confirm its the one we expect
        team = qs[0]
        self.assertEquals(data.get('name'), team.name)
        self.assertEquals(data.get('alias'), team.alias)

        # parse the other team
        home_team_str = """{'_id': 'cGFyZW50X2FwaV9faWRoaWVyYXJjaHlsZWFndWVfX2lkM2M2ZDMxOGEtNjE2NC00MjkwLTliYmMtYmY5YmIyMWNjNGI4Y29uZmVyZW5jZV9faWQxYmRlZmUxMi02Y2IyLTRkNmEtYjIwOC1iMDQ2MDJhZTc5YzNkaXZpc2lvbl9faWRlNDQ3ZTdjMC01OTk3LTRiYjctYmVhMy1hYWFlNDhhZWRjYjhpZDgyY2Y5NTY1LTZlYjktNGYwMS1iZGJkLTVhYTBkNDcyZmNkOQ==',
         'alias': 'IND',
         'conference__id': '1bdefe12-6cb2-4d6a-b208-b04602ae79c3',
         'dd_updated__id': 1471601765520,
         'division__id': 'e447e7c0-5997-4bb7-bea3-aaae48aedcb8',
         'id': '82cf9565-6eb9-4f01-bdbd-5aa0d472fcd9',
         'league__id': '3c6d318a-6164-4290-9bbc-bf9bb21cc4b8',
         'market': 'Indianapolis',
         'name': 'Colts',
         'parent_api__id': 'hierarchy',
         'references__list': {'reference': 'IND'},
         'venue': '6ed18563-53e0-46c2-a91d-12d73a16456d'}"""
        data = self.__parse_obj_str(self.sport, 'team', home_team_str)
        qs = sports.nfl.models.Team.objects.filter(srid=data.get('id'))
        self.assertTrue(
            1 == qs.count())  # should be at least 1, more tests will confirm its the one we expect
        team = qs[0]
        self.assertEquals(data.get('name'), team.name)
        self.assertEquals(data.get('alias'), team.alias)

        # parse the game (requires Season, and both the home and away Team objects to exist)
        # note: for this test we actually need to delete it if it exists, so the test can run properly
        scheduled_game_str = """{
            '_id': 'cGFyZW50X2FwaV9faWRzY2hlZHVsZXNlYXNvbl9faWQ2NTlkMmJkMC1jNDNlLTRiYjAtODUwMy05ZDU3NjkxMWQwMjl3ZWVrX19pZDYwYmZlZWY1LTUxZGItNGUyZi1iYjg1LTM3N2E2Mzg2YWM2ZGlkYTFhMzQzYjctMDYzMS00YzA0LWJkODgtZGFkNWM4OWY1MWJj',
            'attendance': 0.0,
            'away': 'a20471b4-a8d9-40c7-95ad-90cc30e46932',
            'broadcast__list': {'internet': 'WatchESPN',
            'network': 'ESPN',
            'satellite': 206.0},
            'dd_updated__id': 1471578967708,
            'entry_mode': 'INGEST',
            'home': '82cf9565-6eb9-4f01-bdbd-5aa0d472fcd9',
            'id': 'a1a343b7-0631-4c04-bd88-dad5c89f51bc',
            'number': 1.0,
            'parent_api__id': 'schedule',
            'reference': 56836.0,
            'scheduled': '2016-08-08T00:00:00+00:00',
            'season__id': '659d2bd0-c43e-4bb0-8503-9d576911d029',
            'status': 'scheduled',
            'utc_offset': -5.0,
            'venue': 'de94507b-cb7b-4684-a0ff-fad0131847e5',
            'weather': 'Temp:  F, Wind:   mph',
            'week__id': '60bfeef5-51db-4e2f-bb85-377a6386ac6d'
        }"""
        # delete existing Game objects with matching srid to ensure the following tests are valid
        data = literal_eval(scheduled_game_str)
        srid_game = data.get('id')
        sports.nfl.models.Game.objects.filter(srid=srid_game).delete()
        qs = sports.nfl.models.Game.objects.filter(srid=srid_game)
        self.assertEquals(0, qs.count())

        # make sure this game was created properly
        data = self.__parse_obj_str(self.sport, 'game', scheduled_game_str)
        qs = sports.nfl.models.Game.objects.filter(srid=srid_game)
        # should be at least 1, more tests will confirm its the one we expect
        self.assertEquals(1, qs.count())
        game = qs[0]
        self.assertEquals('scheduled', game.status)

        # now parse the game in the inprogress state (its 'status' field is only change to make
        # sure it changes
        inprogress = 'inprogress'
        data['status'] = inprogress
        data = self.__parse_obj(self.sport, 'game', data)
        qs = sports.nfl.models.Game.objects.filter(srid=srid_game)
        self.assertEquals(1, qs.count())  # there should still only be 1
        game = qs[0]
        self.assertEquals(inprogress, game.status)

        # change the status again
        complete = 'complete'
        data['status'] = complete
        data = self.__parse_obj(self.sport, 'game', data)
        qs = sports.nfl.models.Game.objects.filter(srid=srid_game)
        self.assertEquals(1, qs.count())  # there should still only be 1
        game = qs[0]
        self.assertEquals(complete, game.status)

        # change the status again - to the final state it should ever be in if it successfully
        # finished
        verify = 'verify'
        closed = 'closed'
        data['status'] = closed
        data = self.__parse_obj(self.sport, 'game', data)
        qs = sports.nfl.models.Game.objects.filter(srid=srid_game)
        self.assertEquals(1, qs.count())  # there should still only be 1
        game = qs[0]
        # First it goes into manual verificatons state
        self.assertEquals(verify, game.status)
        # Now if we manually change it to closed, it should go to that.
        game.status=closed
        game.save()
        self.assertEquals(closed, game.status)

        #
        # now we shoudnt be able to change it from the 'closed' status
        inprogress = 'inprogress'
        data['status'] = inprogress
        data = self.__parse_obj(self.sport, 'game', data)
        qs = sports.nfl.models.Game.objects.filter(srid=srid_game)
        self.assertEquals(1, qs.count())  # there should still only be 1
        game = qs[0]
        self.assertNotEquals(inprogress, game.status)


class GameScheduleParserStatusTest(AbstractTest):
    game_event = {
        "attendance": 64779,
        "_id": "cGFyZW50X2FwaV9faWRzY2hlZHVsZXNlY",
        "scheduled": "2017-08-31T23:00:00+00:00",
        "home": "82cf9565-6eb9-4f01-bdbd-5aa0d472fcd9",
        "away": "ad4ae08f-d808-42d5-a1e6-e9bc4e34d123",
        "id": "c806dc05-84cf-4fc5-84c0-6c469978f725",
        "week__id": "4974b8dd-e86b-49f0-be39-06c6797428b6",
        "dd_updated__id": 1504880958814,
        "parent_api__id": "schedule",
        "utc_offset": -5,
        "number": 58,
        "status": "closed",
        "reference": 57226,
        "weather": "Cloudy Temp: 78 F, Humidity: 53%, Wind: NNE 15 mph",
        "season__id": "3d6abb6b-9c91-40a9-9441-bbadc8a56f0e",
        "venue": "6ed18563-53e0-46c2-a91d-12d73a16456d",
        "entry_mode": "INGEST"
    }

    def setUp(self):
        cache.clear()
        super().setUp()
        self.parser = GameSchedule()

        # Make the stuff we need to parse this.
        mommy.make(
            Season,
            srid=self.game_event['season__id']
        )

        home_team = mommy.make(
            sports.nfl.models.Team,
            alias="DEN",
            srid=self.game_event['home']
        )

        away_team = mommy.make(
            sports.nfl.models.Team,
            alias="OKC",
            srid=self.game_event['away']
        )

        # Create a Game model so this boxcore can be parsed.
        self.game = mommy.make(
            Game,
            srid=self.game_event['id'],
            away=away_team,
            srid_away=away_team.srid,
            home=home_team,
            srid_home=home_team.srid,
            status='scheduled'
        )

    def __parse_and_send(self, unwrapped_obj, target, tag=None):
        parts = target[0].split('.')
        oplog_obj = OpLogObjWrapper(parts[0], parts[1], unwrapped_obj)
        self.parser.parse(oplog_obj, target=target)
        return self.parser

    # Test GameSchedule parser
    def test_completed_game_set_to_verify(self):
        sport_db = 'nflo'
        parent_api = 'schedule'

        self.assertEqual(self.game.status, 'scheduled')
        logger.info('Setting game to `%s`' % Game.STATUS_INPROGRESS)
        # Set the game event to 'inprogress' and ensure the game is still in 'inprogress' mode.
        self.game_event['status'] = Game.STATUS_INPROGRESS
        self.__parse_and_send(self.game_event, (sport_db + '.' + 'team', parent_api))
        self.game.refresh_from_db()
        self.assertEqual(self.game.status, Game.STATUS_INPROGRESS)

        logger.info('Setting game to `%s`' % Game.STATUS_COMPLETE)
        # Set the game event to 'complete' and ensure the game is in 'closed' mode.
        self.game_event['status'] = Game.STATUS_COMPLETE
        self.__parse_and_send(self.game_event, (sport_db + '.' + 'team', parent_api))
        self.game.refresh_from_db()
        self.assertEqual(self.game.status, Game.STATUS_COMPLETE)

        logger.info('Setting game to `%s`' % Game.STATUS_CLOSED)
        # Now set it to 'closed' and check the status is moved to 'verify'
        self.game_event['status'] = Game.STATUS_CLOSED
        self.__parse_and_send(self.game_event, (sport_db + '.' + 'team', parent_api))
        self.game.refresh_from_db()
        self.assertEqual(self.game.status, Game.STATUS_NEEDS_VERIFICATION)

        # Game was already closed, and gets re-parsed, with a 'closed' status.
        logger.info('Setting game to `%s`' % Game.STATUS_CLOSED)
        self.game.status = Game.STATUS_CLOSED
        self.game.save()
        # Now set the object 'closed' and make sure it doesn't go back to 'verify'
        self.game_event['status'] = Game.STATUS_CLOSED
        self.__parse_and_send(self.game_event, (sport_db + '.' + 'team', parent_api))
        self.game.refresh_from_db()
        self.assertEqual(self.game.status, Game.STATUS_CLOSED)


