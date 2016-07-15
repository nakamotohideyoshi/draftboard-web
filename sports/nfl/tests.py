#
# sports/nfl/test.py

from django.utils import timezone
from ast import literal_eval
from test.classes import AbstractTest
import sports.nfl.models
from sports.nfl.models import (
    Team,
    Player,
    Season,
    Game,
    PlayerStats,
)
from dataden.watcher import OpLogObj, OpLogObjWrapper
from sports.nfl.parser import (
    SeasonSchedule,
    GameSchedule,
    GameBoxscoreParser,
    TeamBoxscoreParser,
    TeamHierarchy,
    PlayParser,

    # reducers, shrinkers, managers
    PlayReducer,
    PlayShrinker,
    PlayManager,
)
import re

class TestPlayManagerRegexScraping(AbstractTest):
    """
    the nfl play will have some datapoints extracted from the text description.

    lets make sure were doing it right.
    """

    def setUp(self):
        self.data = {} # TODO

    def test_1(self):
        pass # TODO

class TestPlayManager(AbstractTest):
    """ parse some information out of the human readable text description """

    def setUp(self):
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
        additional_data = {'special_field_1' : 'special_value_1'}
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
        self.parser = TeamBoxscoreParser()

    def __parse_and_send(self, unwrapped_obj, target):
        # oplog_obj = OpLogObjWrapper('nflo', 'play', unwrapped_obj)
        # self.parser.parse(oplog_obj, target=('nflo.play', 'pbp'))
        parts = target[0].split('.')
        oplog_obj = OpLogObjWrapper(parts[0], parts[1], unwrapped_obj)
        self.parser.parse(oplog_obj, target=target)
        self.parser.send()

    def test_1(self):
        sport_db = 'nflo'
        parent_api = 'boxscores'

        data = {
            "_id": "cGFyZW50X2FwaV9faWRib3hzY29yZXNnYW1lX19pZDFjYTlhMGMxLWQxNDUtNGFjYi1hY2EyLWNiMmI1ZmU1MjliOXBhcmVudF9saXN0X19pZHN1bW1hcnlfX2xpc3RpZDQyNTRkMzE5LTFiYzctNGY4MS1iNGFiLWI1ZTZmMzQwMmI2OQ==",
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

        self.__parse_and_send(data, (sport_db + '.' + 'team', parent_api))

class TestGameBoxscoreParser(AbstractTest):
    """ tests the send() part only """

    def setUp(self):
        self.parser = GameBoxscoreParser()

    def __parse_and_send(self, unwrapped_obj, target):
        # oplog_obj = OpLogObjWrapper('nflo', 'play', unwrapped_obj)
        # self.parser.parse(oplog_obj, target=('nflo.play', 'pbp'))
        parts = target[0].split('.')
        oplog_obj = OpLogObjWrapper(parts[0], parts[1], unwrapped_obj)
        self.parser.parse(oplog_obj, target=target)
        self.parser.send()

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

        self.__parse_and_send(data, (sport_db + '.' + 'game', parent_api))

class TestPlayParser(AbstractTest):
    """
    parsers and sends PBP objects from the official feed

    NOTE: because the test database does parse the stats previously,
    we will NOT HAVE the PlayerStats objects.
    """

    def setUp(self):
        self.parser = PlayParser()

    def __parse_and_send(self, unwrapped_obj, target):

        # oplog_obj = OpLogObjWrapper('nflo', 'play', unwrapped_obj)
        # self.parser.parse(oplog_obj, target=('nflo.play', 'pbp'))
        parts = target[0].split('.')
        oplog_obj = OpLogObjWrapper(parts[0], parts[1], unwrapped_obj)
        self.parser.parse(oplog_obj, target=target)

        # #
        # # get the 'player' srids
        # player_srids = self.parser.get_srids_for_field('player')
        # print('"player" field srids:', str(player_srids))
        #
        # # get the game srid from the 'game__id' field
        # #game_srid = self.parser.get_srids_for_field('game__id')
        # game_srid = self.parser.get_srid_game('game__id')
        # print('"game" field srid:', str(game_srid))
        #
        # #
        # # look up the player stats (TODO get the game srid as well)
        # player_stats_found = self.parser.find_player_stats()
        # print('player_stats_found:', str(player_stats_found), ' BECAUSE THERE ARE NONE IN THE TEST DB!')

        #print('get_send_data:', self.parser.get_send_data())

        # print('SL', self.parser.StartLocationCache().fetch(self.parser.ts, self.parser.play_srid))
        # print('SP', self.parser.StartPossessionCache().fetch(self.parser.ts, self.parser.play_srid))
        # print('EL', self.parser.EndLocationCache().fetch(self.parser.ts, self.parser.play_srid))
        # print('EP', self.parser.EndPossessionCache().fetch(self.parser.ts, self.parser.play_srid))

        # test sending with pusher. we cant do this with codeship though! (so remove it when done)
        #self.parser.send()#force=True)

    def test_1(self):
        """ kickoff (touchback) """
        unwrapped_obj = {
            'start_situation__list': {'yfd': 0.0, 'location': '4809ecb0-abd3-451d-9c4a-92a90b83ca06', 'clock': '15:00',
                                      'possession': '4809ecb0-abd3-451d-9c4a-92a90b83ca06', 'down': 0.0},
            'away_points': 0.0, 'reference': 63.0,
            'end_situation__list': {'yfd': 10.0, 'location': '22052ff7-c065-42ee-bc8f-c4691c50e624', 'clock': '15:00',
                                    'possession': '22052ff7-c065-42ee-bc8f-c4691c50e624', 'down': 1.0},
            'alt_description': 'A.Franks kicks 65 yards from MIA 35 to end zone, Touchback.',
            'game__id': '0141a0a5-13e5-4b28-b19f-0c3923aaef6e', 'parent_api__id': 'pbp', 'clock': '15:00',
            'drive__id': 'a956d9cb-d8ab-408c-91fc-442f06e338ff', 'statistics__list': {
                'kick__list': {'gross_yards': 74.0, 'team': '4809ecb0-abd3-451d-9c4a-92a90b83ca06', 'yards': 65.0,
                               'attempt': 1.0, 'touchback': 1.0, 'player': '59da7aea-f21a-43c5-b0bf-2d1e8b19da80',
                               'confirmed': 'true'},
                'return__list': {'team': '22052ff7-c065-42ee-bc8f-c4691c50e624', 'touchback': 1.0, 'confirmed': 'true',
                                 'category': 'kick_return'}}, 'id': '9de4c5df-5e94-4fe2-b646-ba1dca0a1afd',
            'sequence': 63.0, 'parent_list__id': 'play_by_play__list', 'home_points': 0.0,
            'description': '3-A.Franks kicks 65 yards from MIA 35 to end zone, Touchback.',
            '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDAxNDFhMGE1LTEzZTUtNGIyOC1iMTlmLTBjMzkyM2FhZWY2ZXF1YXJ0ZXJfX2lkZmQzMTM2OGItYTE1OS00ZjU2LWEwMjItYWZjNjkxZTM0NzU1cGFyZW50X2xpc3RfX2lkcGxheV9ieV9wbGF5X19saXN0ZHJpdmVfX2lkYTk1NmQ5Y2ItZDhhYi00MDhjLTkxZmMtNDQyZjA2ZTMzOGZmaWQ5ZGU0YzVkZi01ZTk0LTRmZTItYjY0Ni1iYTFkY2EwYTFhZmQ=',
            'type': 'kickoff', 'play_clock': 12.0, 'quarter__id': 'fd31368b-a159-4f56-a022-afc691e34755',
            'dd_updated__id': 1464841517401, 'wall_clock': '2015-09-13T17:02:41+00:00'}

        self.__parse_and_send(unwrapped_obj)

    def test_2(self):
        """ rushing play """
        unwrapped_obj = {
            'start_situation__list': {'yfd': 10.0, 'location': '22052ff7-c065-42ee-bc8f-c4691c50e624', 'clock': '15:00',
                                      'possession': '22052ff7-c065-42ee-bc8f-c4691c50e624', 'down': 1.0},
            'away_points': 0.0, 'reference': 82.0,
            'end_situation__list': {'yfd': 5.0, 'location': '22052ff7-c065-42ee-bc8f-c4691c50e624', 'clock': '14:30',
                                    'possession': '22052ff7-c065-42ee-bc8f-c4691c50e624', 'down': 2.0},
            'alt_description': '(15:00) A.Morris left tackle to WAS 25 for 5 yards (K.Sheppard).',
            'game__id': '0141a0a5-13e5-4b28-b19f-0c3923aaef6e', 'parent_api__id': 'pbp', 'clock': '15:00',
            'drive__id': 'a956d9cb-d8ab-408c-91fc-442f06e338ff', 'statistics__list': {
                'rush__list': {'team': '22052ff7-c065-42ee-bc8f-c4691c50e624', 'yards': 5.0, 'goaltogo': 0.0,
                               'attempt': 1.0, 'player': 'bd10efdf-d8e7-4e23-ab1a-1e42fb65131b', 'inside_20': 0.0,
                               'confirmed': 'true'},
                'defense__list': {'team': '4809ecb0-abd3-451d-9c4a-92a90b83ca06', 'tackle': 1.0,
                                  'player': '7190fb71-0916-4f9d-88a0-8c1a8c1c9d0d', 'confirmed': 'true'}},
            'id': '3a2e9bb4-6b79-473a-b86a-522b92e88c71', 'sequence': 82.0, 'parent_list__id': 'play_by_play__list',
            'home_points': 0.0, 'description': '(15:00) 46-A.Morris left tackle to WAS 25 for 5 yards (52-K.Sheppard).',
            '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDAxNDFhMGE1LTEzZTUtNGIyOC1iMTlmLTBjMzkyM2FhZWY2ZXF1YXJ0ZXJfX2lkZmQzMTM2OGItYTE1OS00ZjU2LWEwMjItYWZjNjkxZTM0NzU1cGFyZW50X2xpc3RfX2lkcGxheV9ieV9wbGF5X19saXN0ZHJpdmVfX2lkYTk1NmQ5Y2ItZDhhYi00MDhjLTkxZmMtNDQyZjA2ZTMzOGZmaWQzYTJlOWJiNC02Yjc5LTQ3M2EtYjg2YS01MjJiOTJlODhjNzE=',
            'type': 'rush', 'play_clock': 12.0, 'quarter__id': 'fd31368b-a159-4f56-a022-afc691e34755',
            'dd_updated__id': 1464841517401, 'wall_clock': '2015-09-13T17:03:26+00:00'}

        self.__parse_and_send(unwrapped_obj)

    def test_3(self):
        """ passing play """
        sport_db = 'nflo'
        parent_api = 'pbp'

        start_possession = {'alias': 'WAS', 'quarter__id': 'fd31368b-a159-4f56-a022-afc691e34755', 'parent_api__id': 'pbp',
            'play__id': '7e49db54-68d0-444d-b244-690f3930b77b', 'reference': 4971.0, 'market': 'Washington',
            '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDAxNDFhMGE1LTEzZTUtNGIyOC1iMTlmLTBjMzkyM2FhZWY2ZXF1YXJ0ZXJfX2lkZmQzMTM2OGItYTE1OS00ZjU2LWEwMjItYWZjNjkxZTM0NzU1cGFyZW50X2xpc3RfX2lkc3RhcnRfc2l0dWF0aW9uX19saXN0ZHJpdmVfX2lkYTk1NmQ5Y2ItZDhhYi00MDhjLTkxZmMtNDQyZjA2ZTMzOGZmcGxheV9faWQ3ZTQ5ZGI1NC02OGQwLTQ0NGQtYjI0NC02OTBmMzkzMGI3N2JpZDIyMDUyZmY3LWMwNjUtNDJlZS1iYzhmLWM0NjkxYzUwZTYyNA==',
            'drive__id': 'a956d9cb-d8ab-408c-91fc-442f06e338ff', 'name': 'Redskins', 'dd_updated__id': 1464841517401,
            'game__id': '0141a0a5-13e5-4b28-b19f-0c3923aaef6e', 'id': '22052ff7-c065-42ee-bc8f-c4691c50e624',
            'parent_list__id': 'start_situation__list'}
        self.__parse_and_send(start_possession, (sport_db + '.' + 'possession', parent_api))
        # required_parts = self.parser.update_required_parts(self.parser.ts, self.parser.play_srid)
        # self.assertTrue(None in required_parts)

        end_possession = {'alias': 'WAS', 'quarter__id': 'fd31368b-a159-4f56-a022-afc691e34755', 'parent_api__id': 'pbp',
             'play__id': '7e49db54-68d0-444d-b244-690f3930b77b', 'reference': 4971.0, 'market': 'Washington',
             '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDAxNDFhMGE1LTEzZTUtNGIyOC1iMTlmLTBjMzkyM2FhZWY2ZXF1YXJ0ZXJfX2lkZmQzMTM2OGItYTE1OS00ZjU2LWEwMjItYWZjNjkxZTM0NzU1cGFyZW50X2xpc3RfX2lkZW5kX3NpdHVhdGlvbl9fbGlzdGRyaXZlX19pZGE5NTZkOWNiLWQ4YWItNDA4Yy05MWZjLTQ0MmYwNmUzMzhmZnBsYXlfX2lkN2U0OWRiNTQtNjhkMC00NDRkLWIyNDQtNjkwZjM5MzBiNzdiaWQyMjA1MmZmNy1jMDY1LTQyZWUtYmM4Zi1jNDY5MWM1MGU2MjQ=',
             'drive__id': 'a956d9cb-d8ab-408c-91fc-442f06e338ff', 'name': 'Redskins', 'dd_updated__id': 1464841517401,
             'game__id': '0141a0a5-13e5-4b28-b19f-0c3923aaef6e', 'id': '22052ff7-c065-42ee-bc8f-c4691c50e624',
             'parent_list__id': 'end_situation__list'}
        self.__parse_and_send(end_possession, (sport_db + '.' + 'possession', parent_api))
        # required_parts = self.parser.update_required_parts(self.parser.ts, self.parser.play_srid)
        # self.assertTrue(None in required_parts)

        start_location = {'play__id': '7e49db54-68d0-444d-b244-690f3930b77b', 'alias': 'WAS',
             'quarter__id': 'fd31368b-a159-4f56-a022-afc691e34755', 'parent_api__id': 'pbp', 'yardline': 25.0,
             'reference': 4971.0, 'market': 'Washington',
             '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDAxNDFhMGE1LTEzZTUtNGIyOC1iMTlmLTBjMzkyM2FhZWY2ZXF1YXJ0ZXJfX2lkZmQzMTM2OGItYTE1OS00ZjU2LWEwMjItYWZjNjkxZTM0NzU1cGFyZW50X2xpc3RfX2lkc3RhcnRfc2l0dWF0aW9uX19saXN0ZHJpdmVfX2lkYTk1NmQ5Y2ItZDhhYi00MDhjLTkxZmMtNDQyZjA2ZTMzOGZmcGxheV9faWQ3ZTQ5ZGI1NC02OGQwLTQ0NGQtYjI0NC02OTBmMzkzMGI3N2JpZDIyMDUyZmY3LWMwNjUtNDJlZS1iYzhmLWM0NjkxYzUwZTYyNA==',
             'drive__id': 'a956d9cb-d8ab-408c-91fc-442f06e338ff', 'name': 'Redskins', 'dd_updated__id': 1464841517401,
             'game__id': '0141a0a5-13e5-4b28-b19f-0c3923aaef6e', 'id': '22052ff7-c065-42ee-bc8f-c4691c50e624',
             'parent_list__id': 'start_situation__list'}
        self.__parse_and_send(start_location, (sport_db + '.' + 'location', parent_api))
        # required_parts = self.parser.update_required_parts(self.parser.ts, self.parser.play_srid)
        # self.assertTrue(None in required_parts)

        end_location = {'play__id': '7e49db54-68d0-444d-b244-690f3930b77b', 'alias': 'WAS',
             'quarter__id': 'fd31368b-a159-4f56-a022-afc691e34755', 'parent_api__id': 'pbp', 'yardline': 29.0,
             'reference': 4971.0, 'market': 'Washington',
             '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDAxNDFhMGE1LTEzZTUtNGIyOC1iMTlmLTBjMzkyM2FhZWY2ZXF1YXJ0ZXJfX2lkZmQzMTM2OGItYTE1OS00ZjU2LWEwMjItYWZjNjkxZTM0NzU1cGFyZW50X2xpc3RfX2lkZW5kX3NpdHVhdGlvbl9fbGlzdGRyaXZlX19pZGE5NTZkOWNiLWQ4YWItNDA4Yy05MWZjLTQ0MmYwNmUzMzhmZnBsYXlfX2lkN2U0OWRiNTQtNjhkMC00NDRkLWIyNDQtNjkwZjM5MzBiNzdiaWQyMjA1MmZmNy1jMDY1LTQyZWUtYmM4Zi1jNDY5MWM1MGU2MjQ=',
             'drive__id': 'a956d9cb-d8ab-408c-91fc-442f06e338ff', 'name': 'Redskins', 'dd_updated__id': 1464841517401,
             'game__id': '0141a0a5-13e5-4b28-b19f-0c3923aaef6e', 'id': '22052ff7-c065-42ee-bc8f-c4691c50e624',
             'parent_list__id': 'end_situation__list'}
        self.__parse_and_send(end_location, (sport_db + '.' + 'location', parent_api))
        # required_parts = self.parser.update_required_parts(self.parser.ts, self.parser.play_srid)
        # self.assertTrue(None in required_parts)

        play = {
            'start_situation__list': {'yfd': 5.0, 'location': '22052ff7-c065-42ee-bc8f-c4691c50e624', 'clock': '14:30',
                                      'possession': '22052ff7-c065-42ee-bc8f-c4691c50e624', 'down': 2.0},
            'away_points': 0.0, 'reference': 103.0,
            'end_situation__list': {'yfd': 1.0, 'location': '22052ff7-c065-42ee-bc8f-c4691c50e624', 'clock': '13:56',
                                    'possession': '22052ff7-c065-42ee-bc8f-c4691c50e624', 'down': 3.0},
            'alt_description': '(14:30) (Shotgun) K.Cousins pass short right to A.Roberts to WAS 29 for 4 yards (B.Grimes).',
            'game__id': '0141a0a5-13e5-4b28-b19f-0c3923aaef6e', 'parent_api__id': 'pbp', 'clock': '14:30',
            'drive__id': 'a956d9cb-d8ab-408c-91fc-442f06e338ff', 'id': '7e49db54-68d0-444d-b244-690f3930b77b',
            'sequence': 103.0, 'parent_list__id': 'play_by_play__list', 'home_points': 0.0,
            'description': '(14:30) (Shotgun) 8-K.Cousins pass short right to 12-A.Roberts to WAS 29 for 4 yards (21-B.Grimes).',
            '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDAxNDFhMGE1LTEzZTUtNGIyOC1iMTlmLTBjMzkyM2FhZWY2ZXF1YXJ0ZXJfX2lkZmQzMTM2OGItYTE1OS00ZjU2LWEwMjItYWZjNjkxZTM0NzU1cGFyZW50X2xpc3RfX2lkcGxheV9ieV9wbGF5X19saXN0ZHJpdmVfX2lkYTk1NmQ5Y2ItZDhhYi00MDhjLTkxZmMtNDQyZjA2ZTMzOGZmaWQ3ZTQ5ZGI1NC02OGQwLTQ0NGQtYjI0NC02OTBmMzkzMGI3N2I=',
            'type': 'pass', 'statistics__list': {
                'receive__list': {'team': '22052ff7-c065-42ee-bc8f-c4691c50e624', 'yards': 4.0, 'goaltogo': 0.0,
                                  'player': '9691f874-be36-4529-a7eb-dde22ee4a848', 'confirmed': 'true',
                                  'reception': 1.0, 'yards_after_catch': 2.0, 'inside_20': 0.0, 'target': 1.0},
                'pass__list': {'team': '22052ff7-c065-42ee-bc8f-c4691c50e624', 'yards': 4.0, 'goaltogo': 0.0,
                               'att_yards': 2.0, 'attempt': 1.0, 'player': 'bbd0942c-6f77-4f83-a6d0-66ec6548019e',
                               'complete': 1.0, 'inside_20': 0.0, 'confirmed': 'true'},
                'defense__list': {'team': '4809ecb0-abd3-451d-9c4a-92a90b83ca06', 'tackle': 1.0,
                                  'player': '7979b613-6dbf-4534-8166-6430433c1ec3', 'confirmed': 'true'}},
            'quarter__id': 'fd31368b-a159-4f56-a022-afc691e34755', 'dd_updated__id': 1464841517401,
            'wall_clock': '2015-09-13T17:03:57+00:00'}
        self.__parse_and_send(play, (sport_db + '.' + 'play', parent_api))

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

        self.game.season, created = Season.objects.get_or_create(srid='nflsrid',season_year=2015,season_type='reg')
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

class TestSeasonScheduleParser(AbstractTest):
    """
    tests sports.nfl.parser.SeasonSchedule
    """

    def setUp(self):
        self.obj_str = """{'_id': 'cGFyZW50X2FwaV9faWRzY2hlZHVsZWlkaHR0cDovL2FwaS5zcG9ydHNkYXRhbGxjLm9yZy9uZmwtcnQxLzIwMTUvUkVHL3NjaGVkdWxlLnhtbA==', 'parent_api__id': 'schedule', 'weeks': [{'week': {'games': [{'game': 'acbb3001-6bb6-41ce-9e91-942abd284e4c'}, {'game': '9920f2a3-720f-4973-998a-eae9b965b8d2'}, {'game': '95091eb4-5bb9-445d-b3f8-023df4dd8d33'}, {'game': '8c65a3c5-9e23-419d-be18-a7663eb53550'}, {'game': '51689a76-5dce-46a1-aa90-c2c04f806340'}, {'game': '83b72efe-7955-4fa4-9149-9eaccbbf0f20'}, {'game': '0141a0a5-13e5-4b28-b19f-0c3923aaef6e'}, {'game': 'eeda7ddd-91df-4993-9cd0-0e8be266f930'}, {'game': 'f2a0bd05-7dff-47b9-97b8-4e5d1a2aceca'}, {'game': 'f32eedba-9552-4200-8e82-4e591bbfcbf5'}, {'game': '56d3f529-89a1-40a8-a323-4811aacc0044'}, {'game': '1ca9a0c1-d145-4acb-aca2-cb2b5fe529b9'}, {'game': 'fee3509f-34b8-461c-946e-a945b73c2bc1'}, {'game': 'c8ca977e-77ad-42fc-a80b-0d4a78e73b87'}, {'game': '2b75bc2a-a0ee-40c7-8a74-e8b1a6e9c256'}, {'game': '718a4f52-c6af-4080-b955-95e8769b68a7'}], 'week': 1.0}}, {'week': {'games': [{'game': '554aac47-088a-42fc-9888-366c3cec5968'}, {'game': 'beaa013f-71cf-463a-8ff4-3b589d69a21e'}, {'game': '9a4d58be-7c83-4b6c-9be7-be686fa945a1'}, {'game': 'd3c8897f-a676-4c0e-beea-5ad1ad7b2cd7'}, {'game': '270b3161-ab73-488e-a25b-8dfbfb752590'}, {'game': '150b2028-7122-4a8d-a015-4b6b1631f290'}, {'game': '28e73389-51ff-4220-91aa-47de855f910b'}, {'game': 'a334f89b-48ed-4e26-a9c1-3d695765e3bd'}, {'game': '83fab116-f034-4f9a-b769-c4e461466a72'}, {'game': '39c307b6-0f85-4124-acb4-7a3a6de07c8f'}, {'game': '55ec637d-4ca8-402c-96ee-840777f87b68'}, {'game': 'c7c45e93-5d60-4389-84e1-971c8ce8807e'}, {'game': 'cc799f7f-542d-43c4-84d0-d4c7d72d7702'}, {'game': '597ee855-a149-49a6-8a35-013fa088449a'}, {'game': 'f325594a-cd1d-43b3-b091-035cfa4d32b1'}, {'game': '8e72ff56-7740-4fe4-b818-78344716abe0'}], 'week': 2.0}}], 'id': 'http://api.sportsdatallc.org/nfl-rt1/2015/REG/schedule.xml', 'dd_updated__id': 1456974079451, 'xmlns': 'http://feed.elasticstats.com/schema/nfl/schedule-v1.0.xsd', 'season': 2015.0, 'type': 'REG'}"""
        self.season_parser = SeasonSchedule()

    def __validate_season(self, season_model, expected_season_year, expected_season_type):
        self.assertEquals(season_model.season_year, expected_season_year)
        self.assertEquals(season_model.season_type, expected_season_type)

    def test_pst_season(self):
        obj = literal_eval(self.obj_str)
        srid = obj.get('id') # the srid will be found in the 'id' field
        oplog_obj = OpLogObjWrapper('nfl','season', obj)
        self.season_parser.parse( oplog_obj )
        season = sports.nfl.models.Season.objects.get(srid=srid)
        self.__validate_season( season, 2015, 'reg' )

class TestGameScheduleParser(AbstractTest):
    """
    tests sports.nfl.parser.GameSchedule -- the parser for sports.nfl.models.Game objects

    effectively tests the TeamHierarchy parser too
    """

    def setUp(self):
        self.sport = 'nfl'
        self.season_str = """{'season': 2015.0, 'xmlns': 'http://feed.elasticstats.com/schema/nfl/schedule-v1.0.xsd', 'id': 'http://api.sportsdatallc.org/nfl-rt1/2015/PRE/schedule.xml', 'weeks': [{'week': {'week': 0.0, 'game': 'b5b6dcbf-3e3b-4e0c-9eaf-ba978545dcaf'}}, {'week': {'week': 1.0, 'games': [{'game': 'e0b0b391-8d15-4b81-b0fc-aa148b8713fc'}, {'game': '0ed4c4ee-f594-4e10-b156-0799062a94c8'}, {'game': 'e237815c-78eb-4960-a1cf-0dbf98908255'}, {'game': '346b5340-e0a8-42de-a2c7-13b83041b9d3'}, {'game': '4a66009c-c873-47a7-af96-2b28b75ff6da'}, {'game': '7875bd80-22ae-44b1-bd6b-6672de6359a9'}, {'game': '63b4d374-9c7c-416e-8aa9-456e22a36af6'}, {'game': '45bafeba-5f30-4d56-a504-02fa3ede6b5d'}, {'game': '19f6b700-3c8f-4783-899e-e348d572bfbe'}, {'game': 'b4dda772-c8cf-4a0d-8b1a-8cee09ebc0d7'}, {'game': 'f0c8a8ec-3c8f-484c-be72-28029a885c80'}, {'game': 'acdd07a4-a86b-4a86-8e3e-7cc26321b936'}, {'game': '8a215abc-52bc-439f-9718-f8b6810e5fe4'}, {'game': '28deac36-f997-4774-a820-83f85627bce1'}, {'game': 'b35b0d8d-b77c-4503-8339-8f48fb9239a4'}, {'game': '5bd30dc8-35b2-4c2b-9ba6-8cb1e9eecec5'}]}}, {'week': {'week': 2.0, 'games': []}}], 'type': 'PRE', 'dd_updated__id': 1456974034293, 'parent_api__id': 'schedule', '_id': 'cGFyZW50X2FwaV9faWRzY2hlZHVsZWlkaHR0cDovL2FwaS5zcG9ydHNkYXRhbGxjLm9yZy9uZmwtcnQxLzIwMTUvUFJFL3NjaGVkdWxlLnhtbA=='}"""
        self.away_team_str = """{'parent_api__id': 'hierarchy', 'market': 'Pittsburgh', 'league__id': 'NFL', 'conference__id': 'AFC', 'venue': '7349a2e6-0ac9-410b-8bd2-ca58c9f7aa34', 'division__id': 'AFC_NORTH', 'id': 'PIT', 'dd_updated__id': 1456973389372, 'name': 'Steelers', '_id': 'cGFyZW50X2FwaV9faWRoaWVyYXJjaHlsZWFndWVfX2lkTkZMY29uZmVyZW5jZV9faWRBRkNkaXZpc2lvbl9faWRBRkNfTk9SVEhpZFBJVA=='}"""
        self.home_team_str = """{'parent_api__id': 'hierarchy', 'market': 'Jacksonville', 'league__id': 'NFL', 'conference__id': 'AFC', 'venue': '4c5c036d-dd3d-4183-b595-71a43a97560f', 'division__id': 'AFC_SOUTH', 'id': 'JAC', 'dd_updated__id': 1456973389372, 'name': 'Jaguars', '_id': 'cGFyZW50X2FwaV9faWRoaWVyYXJjaHlsZWFndWVfX2lkTkZMY29uZmVyZW5jZV9faWRBRkNkaXZpc2lvbl9faWRBRkNfU09VVEhpZEpBQw=='}"""
        self.game_str = """{'parent_api__id': 'schedule', 'season__id': 'http://api.sportsdatallc.org/nfl-rt1/2015/PRE/schedule.xml', 'away': 'PIT', 'scheduled': '2015-08-14T23:30:00+00:00', 'home_rotation': '', 'away_rotation': '', 'dd_updated__id': 1456974034293, '_id': 'cGFyZW50X2FwaV9faWRzY2hlZHVsZXNlYXNvbl9faWRodHRwOi8vYXBpLnNwb3J0c2RhdGFsbGMub3JnL25mbC1ydDEvMjAxNS9QUkUvc2NoZWR1bGUueG1saWQxOWY2YjcwMC0zYzhmLTQ3ODMtODk5ZS1lMzQ4ZDU3MmJmYmU=', 'id': '19f6b700-3c8f-4783-899e-e348d572bfbe', 'weather__list': {'humidity': 49.0, 'wind__list': {'direction': 'NE', 'speed': 14.0}, 'condition': 'Partly Cloudy ', 'temperature': 90.0}, 'status': 'closed', 'broadcast__list': {'network': '', 'satellite': '', 'cable': '', 'internet': ''}, 'home': 'JAC', 'links__list': [{'link': {'rel': 'statistics', 'href': '/2015/PRE/1/PIT/JAC/statistics.xml', 'type': 'application/xml'}}, {'link': {'rel': 'summary', 'href': '/2015/PRE/1/PIT/JAC/summary.xml', 'type': 'application/xml'}}, {'link': {'rel': 'pbp', 'href': '/2015/PRE/1/PIT/JAC/pbp.xml', 'type': 'application/xml'}}, {'link': {'rel': 'boxscore', 'href': '/2015/PRE/1/PIT/JAC/boxscore.xml', 'type': 'application/xml'}}, {'link': {'rel': 'roster', 'href': '/2015/PRE/1/PIT/JAC/roster.xml', 'type': 'application/xml'}}, {'link': {'rel': 'injuries', 'href': '/2015/PRE/1/PIT/JAC/injuries.xml', 'type': 'application/xml'}}, {'link': {'rel': 'depthchart', 'href': '/2015/PRE/1/PIT/JAC/depthchart.xml', 'type': 'application/xml'}}], 'venue': '4c5c036d-dd3d-4183-b595-71a43a97560f'}"""

        self.season_parser = SeasonSchedule()
        self.away_team_parser = TeamHierarchy()
        self.home_team_parser = TeamHierarchy()
        self.game_parser = GameSchedule()

    def test_game_schedule_parse(self):
        """
        as a prerequisite, parse the seasonschedule, and both home & away teams
        """
        # parse the season_schedule obj
        season_oplog_obj = OpLogObjWrapper(self.sport,'season',literal_eval(self.season_str))
        self.season_parser.parse( season_oplog_obj )
        self.assertEquals( 1, sports.nfl.models.Season.objects.filter(season_year=2015,season_type='pre').count() ) # should have parsed 1 thing

        away_team_oplog_obj = OpLogObjWrapper(self.sport,'team',literal_eval(self.away_team_str))
        self.away_team_parser.parse( away_team_oplog_obj )
        self.assertEquals( 1, sports.nfl.models.Team.objects.all().count() ) # should be 1 team in there now

        home_team_oplog_obj = OpLogObjWrapper(self.sport,'team',literal_eval(self.home_team_str))
        self.home_team_parser.parse( home_team_oplog_obj )
        self.assertEquals( 2, sports.nfl.models.Team.objects.all().count() ) # should be 2 teams in there now

        # now attempt to parse the game
        game_oplog_obj = OpLogObjWrapper(self.sport,'game',literal_eval(self.game_str))
        self.game_parser.parse( game_oplog_obj )
        self.assertEquals( 1, sports.nfl.models.Game.objects.all().count() )

# class TestPlayPbp(AbstractTest):
#     """
#     test parse an actual object which once came from dataden. (sanity check)
#
#     there is a more generic test in sports.sport.tests
#     """
#
#     def setUp(self):
#         # passing play has some player srids we might care about
#         self.obj_str = """{'o': {'yfd': 10.0, 'distance': 'Short', 'yard_line': 31.0, 'direction': 'Left', 'formation': 'Shotgun', 'summary': '12-A.Rodgers incomplete. Intended for 17-D.Adams.', 'updated': '2015-09-29T00:32:01+00:00', 'type': 'pass', 'side': 'GB', 'down': 1.0, 'participants__list': [{'player': '0ce48193-e2fa-466e-a986-33f751add206'}, {'player': 'e7d6ae25-bf15-4660-8b37-c37716551de3'}], 'game__id': 'af51f745-7e7d-4762-864c-bac67c2db7e4', 'clock': '14:53', '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZGFmNTFmNzQ1LTdlN2QtNDc2Mi04NjRjLWJhYzY3YzJkYjdlNHBhcmVudF9saXN0X19pZGRyaXZlX19saXN0aWQwM2ZmZDlkOC05NGQ2LTQ2NzUtOWE1MC00ZGNjMWY5NDFhODE=', 'id': '03ffd9d8-94d6-4675-9a50-4dcc1f941a81', 'dd_updated__id': 1443486878736, 'parent_list__id': 'drive__list', 'sequence': 3.0, 'links__list': {'link__list': {'href': '/2015/REG/3/KC/GB/plays/03ffd9d8-94d6-4675-9a50-4dcc1f941a81.xml', 'type': 'application/xml', 'rel': 'summary'}}, 'parent_api__id': 'pbp'}, 'ns': 'nfl.play', 'ts': 1454659978}"""
#         # kick play may not have player srdis we care about
#         # self.data = literal_eval(self.obj_str) # convert to dict
#         # self.oplog_obj = OpLogObj(self.data)
#
#         # the field we will try to get a game srid from
#         self.game_srid_field        = 'game__id'
#         # a list of the game_srids we expect to get back (only 1 for this test)
#         self.target_game_srids      = ['af51f745-7e7d-4762-864c-bac67c2db7e4']
#
#         # the field name we will search for player srid(s)
#         self.player_srid_field      = 'player'
#         # the list of player srids we expect to find in this object
#         self.target_player_srids    = ['0ce48193-e2fa-466e-a986-33f751add206']
#
#         self.player_stats_class     = PlayerStats
#
#     def __play_pbp_parse(self, str_oplog_obj):
#         data        = literal_eval( str_oplog_obj )
#         oplog_obj   = OpLogObj( data )
#         play_pbp    = PlayPbp()
#         play_pbp.parse( oplog_obj )
#         return play_pbp
#
#     def test_play_pbp_parse(self):
#         """
#         """
#         play_pbp = self.__play_pbp_parse(self.obj_str)
#
#         game_srids = play_pbp.get_srids_for_field(self.game_srid_field)
#         self.assertIsInstance( game_srids, list )
#         self.assertEquals( set(game_srids), set(self.target_game_srids) )
#         self.assertEquals( len(set(game_srids)), 1 )
#
#         # we are going to use the game_srid for a PlayerStats filter()
#         game_srid = list(set(game_srids))[0]
#         self.assertIsInstance( game_srid, str ) # the srid should be a string
#
#         # we are going to use the list of player srids for the PlayerStats filter()
#         player_srids = play_pbp.get_srids_for_field(self.player_srid_field)
#         self.assertTrue( set(self.target_player_srids) <= set(player_srids) )
#
#     def test_play_pbp_for_kick_play(self):
#         """
#         we dont really care about kick plays for scoring, so lets
#         just see how the PlayPbp / pbp+stats linker handles this object
#         """
#         obj_str2 = """{'o': {'yfd': 10.0, 'yard_line': 35.0, 'id': '85345fbd-d2f1-43e7-885f-925370a9828e', 'summary': '5-C.Santos kicks 70 yards from KC 35. 88-T.Montgomery to GB 31 for 36 yards (30-J.Fleming).', 'updated': '2015-09-29T00:32:06+00:00', 'type': 'kick', 'side': 'KC', 'down': 1.0, 'participants__list': [{'player': 'd96ff17c-841a-4768-8e08-3a4cfcb7f717'}, {'player': '0c39e276-7a5b-448f-a696-532506f1035a'}, {'player': '349a994b-4b6d-42e6-a2fe-bdb3359b0a31'}], 'game__id': 'af51f745-7e7d-4762-864c-bac67c2db7e4', 'clock': '15:00', '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZGFmNTFmNzQ1LTdlN2QtNDc2Mi04NjRjLWJhYzY3YzJkYjdlNHBhcmVudF9saXN0X19pZGRyaXZlX19saXN0aWQ4NTM0NWZiZC1kMmYxLTQzZTctODg1Zi05MjUzNzBhOTgyOGU=', 'parent_api__id': 'pbp', 'dd_updated__id': 1443486878736, 'parent_list__id': 'drive__list', 'sequence': 2.0, 'links__list': {'link__list': {'href': '/2015/REG/3/KC/GB/plays/85345fbd-d2f1-43e7-885f-925370a9828e.xml', 'type': 'application/xml', 'rel': 'summary'}}}, 'ns': 'nfl.play', 'ts': 1454659978}"""
#
#         play_pbp = self.__play_pbp_parse(obj_str2)

