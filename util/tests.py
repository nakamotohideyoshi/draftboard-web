from ast import literal_eval
from logging import getLogger
from unittest import TestCase

from util.dicts import (
    Reducer,
    Shrinker,
    Manager,
)
from contest.classes import (
    FairMatch,
)

logger = getLogger('util.tests')


class TestFairMatch(TestCase):
    """
    example of weird (error?) situation. #27 doesnt get back into the selection pool in Round 3.

        #contests_forced : [[25, 18, 5, 31, 33, 29, 24, 23, 30, 22]]
        #unused_entries  : [5, 18, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]

        contests_forced : [[, , , , , , , 23, , 22]]
        unused_entries  : [, , , , 26, 27, 28, , , , 32, ]

        from util.fairmatch import FairMatchNoCancel
        entry_pool = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,21,22,22,23,23,24,24,25,26,26,26,27,27,28,28,28,29,29,29,30,30,30,31,31,31,32,32,32,33,33,33]
        contest_size = 10
        fmnc = FairMatchNoCancel(entry_pool, contest_size)
        fmnc.run()
        fmnc.print_debug_info()

        ++++ beginning of round 1 ++++
        (pre-round) entry pool: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 21, 22, 22, 23, 23, 24, 24, 25, 26, 26, 26, 27, 27, 28, 28, 28, 29, 29, 29, 30, 30, 30, 31, 31, 31, 32, 32, 32, 33, 33, 33]
        excluded(for fairness): []
        round uniques         : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]
        remaining entries     : [21, 22, 23, 24, 26, 26, 27, 28, 28, 29, 29, 30, 30, 31, 31, 32, 32, 33, 33] including any entries in exclude (debug)
        remaining uniques     : [32, 33, 21, 22, 23, 24, 26, 27, 28, 29, 30, 31] not including excludes. potential additional entries this round
            making contest: [18, 8, 11, 32, 9, 15, 21, 28, 26, 5] force: False
            making contest: [12, 30, 1, 17, 33, 6, 27, 24, 20, 19] force: False
            making contest: [14, 13, 23, 3, 10, 16, 29, 7, 25, 2] force: False
                -> [4, 22, 31] didnt get filled.
                -> randomly chose: [29, 33, 28, 32, 21, 23, 24] from [29, 33, 28, 32, 21, 23, 24, 26, 30, 27] (avoiding these obviously: [4, 22, 31] )
            making contest: [4, 22, 31, 29, 33, 28, 32, 21, 23, 24] force: True ** = superlay is possible here.
            (exclude [29, 33, 28, 32, 21, 23, 24] in round 2)

        ++++ beginning of round 2 ++++
        (pre-round) entry pool: [22, 26, 26, 27, 28, 29, 30, 30, 31, 31, 32, 33]
        excluded(for fairness): [29, 33, 28, 32, 21, 23, 24]
        round uniques         : [31, 26, 27, 22, 30]
        remaining entries     : [26, 28, 29, 30, 31, 32, 33] including any entries in exclude (debug)
        remaining uniques     : [26, 30, 31] not including excludes. potential additional entries this round
                -> [27, 22, 30, 31, 26] didnt get filled.
                -> randomly chose: [] from [] (avoiding these obviously: [27, 22, 30, 31, 26] )
            (exclude [] in round 3)

        ++++ beginning of round 3 ++++
        (pre-round) entry pool: [26, 28, 29, 30, 31, 32, 33]
        excluded(for fairness): []
        round uniques         : [32, 33, 26, 28, 29, 30, 31]
        remaining entries     : [] including any entries in exclude (debug)
        remaining uniques     : [] not including excludes. potential additional entries this round
                -> [31, 32, 28, 30, 33, 26, 29] didnt get filled.
                -> randomly chose: [] from [] (avoiding these obviously: [31, 32, 28, 30, 33, 26, 29] )
            (exclude [] in round 4)
        done!
                get 10x entry from [32, 33, 22, 26, 27, 28, 29, 30, 31] ignoring entries in []
                get 10x entry from [26, 30, 31] ignoring entries in []

    make sure we properly exclude entries in the final 1st entry step
    where we potentially use additional 2nd entries to fill a contest.
    """

    def setUp(self):
        self.fm = FairMatch([1, 2, 3, 4], 3)


# class TestFairMatchNoCancel(TestCase):
#     """
#     the "no cancel" version of fairmatch runs FairMatch,
#     and as a final step it will place all unused entries
#     into contests which may result in overlay.
#     """
#
#     def setUp(self):
#         self.entry_pool = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
#                            21, 21, 22, 22, 23, 23, 24,
#                            24, 25, 26, 26, 26, 27, 27, 28, 28, 28, 29, 29, 29, 30, 30, 30, 31, 31,
#                            31, 32, 32, 32, 33, 33, 33]
#         self.contest_size = 10
#         self.fmnc = FairMatchNoCancel([1, 2, 3, 4], 3)
#

class ReducerTest(TestCase):
    def setUp(self):
        pass  # TODO

    def test_exception_remove_fields_not_set(self):
        """
        exception should be thrown if child class
        does not set 'remove_fields' list
        """

        class TestReducer(Reducer):
            pass

        data = {}  # for this test, doesnt need any key values
        self.assertRaises(
            Reducer.RemoveFieldsNotSetException,
            lambda: TestReducer(data)
        )

    def test_exception_invalid_init_args(self):
        """
        should raise exception when an instance
        is created with an invalid object (ie: not a dict)
        """

        class TestReducer(Reducer):
            remove_fields = []

        data = 1  # purposely invalid for this test

        self.assertRaises(
            Reducer.InvalidDataType,
            lambda: TestReducer(data)
        )

    def test_boolean_conversion(self):
        """
        Reducer has the ability to convert string values
        equal to: "true", "false" into booleans.

        this tests that. (it is not applied to all fields by default
         and must be selectively used in your own implementation though!)

        values other than the strings "true" and "false" are returned unchanged.
        """

        class TestReducer(Reducer):
            remove_fields = []

        tr = TestReducer({})  # data doesnt matter for this test
        # test if assertTrue returns true for things that arent booleans

        ######################################################################
        # in python 3.x, the following asserts have comments that are valid! #
        ######################################################################
        # self.assertFalse(0) # passes
        # self.assertTrue(1)  # passes
        # self.assertFalse(2) # fails!   assertFalse() implemented with if statement, and
        #                     #             >>> if 2: <code>, will enter the if-guard!

        # test Reducer's str2bool() method
        self.assertTrue(tr.str2bool(Reducer.str_true))
        self.assertFalse(tr.str2bool(Reducer.str_false))

        # test on things not cast to bool
        d = {}  # str2bool should return a dict
        self.assertTrue(isinstance(tr.str2bool(d), dict))
        l = []  # str2bool should return a list
        self.assertTrue(isinstance(tr.str2bool(l), list))

    def test_removes_specified_fields(self):
        """
        a simple test to make sure its working as intended

        this test also ensures the original data is not modified
        """
        data = {
            'key1': 'val1',
            'key2': 'val2',
        }
        orig = data.copy()

        class TestReducer(Reducer):
            remove_fields = ['key1']

        tr = TestReducer(data)
        reduced = tr.reduce()

        # ensure the keys left do not match the remove_fields
        # the set() <= set() will evaluate True if there any remove_fields
        # still in the keys of the reduced data. so assert that it is False
        self.assertFalse(set(TestReducer.remove_fields) <= set(reduced.keys()))

        # and just check to make sure the original data is intact
        self.assertTrue(tr.data == orig)

    def test_pre_reduce_implemention(self):
        """
        test that overriding the method pre_reduce() actually
        executes prior to reduce happening.

        this test implementation overrides pre_reduce() and reduce()
        to each set a class variable which flags they have been called,
        but it will only set the flag for reduce() if pre_reduce has
        previously been set to True. thus, if the 'reduce_called'
        variable is True after the reduce() method has been invoked
        we can infer that pre_reduce() indeed happened before it, as expected.
        """
        data = {}

        class TestReducer(Reducer):
            remove_fields = ['key1']

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.pre_reduce_called = False
                self.reduce_called = False

            def pre_reduce(self):
                super().pre_reduce()
                self.pre_reduce_called = True

            def reduce(self):
                reduced = super().reduce()
                self.reduce_called = self.pre_reduce_called and True
                return reduced

        #
        tr = TestReducer(data)
        reduced = tr.reduce()

        self.assertTrue(tr.pre_reduce_called and tr.reduce_called)


class ShrinkerTest(TestCase):
    def setUp(self):
        pass  # TODO

    def test_exception_fields_not_set(self):
        """
        creating an instance of a subclass that has not
        set the fields property raises exception
        """

        class TestFieldsNotSetShrinker(Shrinker):
            pass

        data = {}  # for this test, doesnt need any key values
        self.assertRaises(
            Shrinker.FieldsNotSetException,
            lambda: TestFieldsNotSetShrinker(data)
        )

    def test_does_not_rename_to_existing_field(self):
        """
        shrinker should not rename a field to an existing key name
        """
        data = {
            'key99': 'val99',
            'key1': 'val1'
        }

        class TestShrinker(Shrinker):
            fields = {'key99': 'key1'}

        ts = TestShrinker(data)
        shrunk = ts.shrink()

        # make sure 'key1' is still the key for 'val1'
        # which is effectively how we know we didnt overwrite
        # the existing 'key1' value!
        self.assertTrue(shrunk.get('key1') == 'val1')

    def test_shrink_does_not_modify_original_data(self):
        """
        shrinker should not rename a field to an existing key name
        """
        data = {
            'key99': 'val99',
            'key1': 'val1'
        }
        orig = data.copy()

        class TestShrinker(Shrinker):
            fields = {
                'key99': 'key9999',
                'key1': 'key1111'
            }

        ts = TestShrinker(data)
        shrunk = ts.shrink()

        # make sure 'key1' is still the key for 'val1'
        # which is effectively how we know we didnt overwrite
        # the existing 'key1' value!
        self.assertTrue(ts.data == orig)


class ManagerTest(TestCase):
    def setUp(self):
        class MyReducer(Reducer):
            remove_fields = []

        class MyShrinker(Shrinker):
            fields = {}

        class MyManager(Manager):
            reducer_class = MyReducer
            shrinker_class = MyShrinker

        # test methods can get their own instance
        self.manager_instance = MyManager({})

    def test_0(self):
        """ test int2bool """
        val = 0
        self.assertEqual(False, self.manager_instance.int2bool(val))

    def test_1(self):
        """ test int2bool """
        val = 1
        self.assertEqual(True, self.manager_instance.int2bool(val))

    def test_2(self):
        """ test int2bool """
        val = 0.0
        self.assertEqual(False, self.manager_instance.int2bool(val))

    def test_3(self):
        """ test int2bool """
        val = 1.0
        self.assertEqual(True, self.manager_instance.int2bool(val))

    def test_4(self):
        """ test str2bool """
        val = 'false'
        self.assertEqual(False, self.manager_instance.str2bool(val))

    def test_5(self):
        """ test str2bool """
        val = 'true'
        self.assertEqual(True, self.manager_instance.str2bool(val))


#
##################################################################################################
# tests below here are not really for the system so much as they are for quick examples
##################################################################################################


class TestRawRequirements(TestCase):
    def setUp(self):
        #
        raw_requirements_str = """{'at_bat_stats': None, 'runners': [{'last_name': 'Prado', 'starting_base': 1.0, 'parent_api__id': 'pbp', 'id': '933a0bc9-26c0-478e-982c-01fd8ffe0614', 'ending_base': 1.0, 'out': 'false', 'at_bat__id': 'b9f80da8-d881-43b5-89f8-af0ebd9c4ac5', 'jersey_number': 14.0, 'dd_updated__id': 1467229174873, 'preferred_name': 'Martin', '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDc1OGJjOTg1LTQxNzEtNGM4Yi1iZWUzLWM3YzJhYjY3ODBmZGF0X2JhdF9faWRiOWY4MGRhOC1kODgxLTQzYjUtODlmOC1hZjBlYmQ5YzRhYzVwaXRjaF9faWRmZDkzODc0Yi0xMmI1LTQyZGEtOWY2ZS1kYWM4MTQzNmRmYWZwYXJlbnRfbGlzdF9faWRydW5uZXJzX19saXN0aWQ5MzNhMGJjOS0yNmMwLTQ3OGUtOTgyYy0wMWZkOGZmZTA2MTQ=', 'parent_list__id': 'runners__list', 'game__id': '758bc985-4171-4c8b-bee3-c7c2ab6780fd', 'first_name': 'Martin', 'pitch__id': 'fd93874b-12b5-42da-9f6e-dac81436dfaf'}], 'at_bat': {'id': 'b9f80da8-d881-43b5-89f8-af0ebd9c4ac5', 'dd_updated__id': 1467229174873, 'pitchs': [{'pitch': '9e27aede-76e2-410e-aff2-0be26834a443'}, {'pitch': 'de3fefa7-90c6-4524-bdd2-e75b75538e1c'}, {'pitch': '1f3909cb-fd36-4193-8b87-9c67cd8aabc4'}, {'pitch': 'fd93874b-12b5-42da-9f6e-dac81436dfaf'}], '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDc1OGJjOTg1LTQxNzEtNGM4Yi1iZWUzLWM3YzJhYjY3ODBmZGlkYjlmODBkYTgtZDg4MS00M2I1LTg5ZjgtYWYwZWJkOWM0YWM1', 'hitter_id': '42cb5171-ffa3-4600-9c41-dbc3805206ea', 'game__id': '758bc985-4171-4c8b-bee3-c7c2ab6780fd', 'parent_api__id': 'pbp'}, 'pitch': {'outcome_id': 'bB', 'at_bat__id': 'b9f80da8-d881-43b5-89f8-af0ebd9c4ac5', 'parent_api__id': 'pbp', 'id': 'fd93874b-12b5-42da-9f6e-dac81436dfaf', 'updated_at': '2016-06-29T19:39:29Z', 'status': 'official', 'pitcher': '97fb113f-b852-4bc1-91bf-79dd11e14992', 'dd_updated__id': 1467229174873, '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDc1OGJjOTg1LTQxNzEtNGM4Yi1iZWUzLWM3YzJhYjY3ODBmZGF0X2JhdF9faWRiOWY4MGRhOC1kODgxLTQzYjUtODlmOC1hZjBlYmQ5YzRhYzVpZGZkOTM4NzRiLTEyYjUtNDJkYS05ZjZlLWRhYzgxNDM2ZGZhZg==', 'game__id': '758bc985-4171-4c8b-bee3-c7c2ab6780fd', 'created_at': '2016-06-29T19:39:27Z', 'count__list': {'outs': 0.0, 'balls': 2.0, 'pitch_count': 4.0, 'strikes': 2.0}, 'flags__list': {'is_ab': 'false', 'is_on_base': 'false', 'is_bunt': 'false', 'is_passed_ball': 'false', 'is_ab_over': 'false', 'is_wild_pitch': 'false', 'is_double_play': 'false', 'is_hit': 'false', 'is_bunt_shown': 'false', 'is_triple_play': 'false'}, 'runners__list': {'runner': '933a0bc9-26c0-478e-982c-01fd8ffe0614'}}, 'zone_pitches': [{'id': '97fb113f-b852-4bc1-91bf-79dd11e14992', 'pitch_speed': 92.0, 'parent_api__id': 'pbp', 'pitch_type': 'FA', 'pitch_count': 20.0, 'pitch_zone': 8.0, 'dd_updated__id': 1467229093256, 'hitter_hand': 'L', 'pitcher_hand': 'R', '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDc1OGJjOTg1LTQxNzEtNGM4Yi1iZWUzLWM3YzJhYjY3ODBmZGF0X2JhdF9faWRiOWY4MGRhOC1kODgxLTQzYjUtODlmOC1hZjBlYmQ5YzRhYzVwaXRjaF9faWQ5ZTI3YWVkZS03NmUyLTQxMGUtYWZmMi0wYmUyNjgzNGE0NDNpZDk3ZmIxMTNmLWI4NTItNGJjMS05MWJmLTc5ZGQxMWUxNDk5Mg==', 'game__id': '758bc985-4171-4c8b-bee3-c7c2ab6780fd', 'at_bat__id': 'b9f80da8-d881-43b5-89f8-af0ebd9c4ac5', 'pitch__id': '9e27aede-76e2-410e-aff2-0be26834a443'}, {'id': '97fb113f-b852-4bc1-91bf-79dd11e14992', 'pitch_speed': 86.0, 'parent_api__id': 'pbp', 'pitch_type': 'SL', 'pitch_count': 21.0, 'pitch_zone': 1.0, 'dd_updated__id': 1467229147682, 'hitter_hand': 'L', 'pitcher_hand': 'R', '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDc1OGJjOTg1LTQxNzEtNGM4Yi1iZWUzLWM3YzJhYjY3ODBmZGF0X2JhdF9faWRiOWY4MGRhOC1kODgxLTQzYjUtODlmOC1hZjBlYmQ5YzRhYzVwaXRjaF9faWRkZTNmZWZhNy05MGM2LTQ1MjQtYmRkMi1lNzViNzU1MzhlMWNpZDk3ZmIxMTNmLWI4NTItNGJjMS05MWJmLTc5ZGQxMWUxNDk5Mg==', 'game__id': '758bc985-4171-4c8b-bee3-c7c2ab6780fd', 'at_bat__id': 'b9f80da8-d881-43b5-89f8-af0ebd9c4ac5', 'pitch__id': 'de3fefa7-90c6-4524-bdd2-e75b75538e1c'}, {'id': '97fb113f-b852-4bc1-91bf-79dd11e14992', 'pitch_speed': 87.0, 'parent_api__id': 'pbp', 'pitch_type': 'SL', 'pitch_count': 22.0, 'pitch_zone': 13.0, 'dd_updated__id': 1467229156775, 'hitter_hand': 'L', 'pitcher_hand': 'R', '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDc1OGJjOTg1LTQxNzEtNGM4Yi1iZWUzLWM3YzJhYjY3ODBmZGF0X2JhdF9faWRiOWY4MGRhOC1kODgxLTQzYjUtODlmOC1hZjBlYmQ5YzRhYzVwaXRjaF9faWQxZjM5MDljYi1mZDM2LTQxOTMtOGI4Ny05YzY3Y2Q4YWFiYzRpZDk3ZmIxMTNmLWI4NTItNGJjMS05MWJmLTc5ZGQxMWUxNDk5Mg==', 'game__id': '758bc985-4171-4c8b-bee3-c7c2ab6780fd', 'at_bat__id': 'b9f80da8-d881-43b5-89f8-af0ebd9c4ac5', 'pitch__id': '1f3909cb-fd36-4193-8b87-9c67cd8aabc4'}, {'id': '97fb113f-b852-4bc1-91bf-79dd11e14992', 'pitch_speed': 92.0, 'parent_api__id': 'pbp', 'pitch_type': 'FA', 'pitch_count': 23.0, 'pitch_zone': 13.0, 'dd_updated__id': 1467229174873, 'hitter_hand': 'L', 'pitcher_hand': 'R', '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDc1OGJjOTg1LTQxNzEtNGM4Yi1iZWUzLWM3YzJhYjY3ODBmZGF0X2JhdF9faWRiOWY4MGRhOC1kODgxLTQzYjUtODlmOC1hZjBlYmQ5YzRhYzVwaXRjaF9faWRmZDkzODc0Yi0xMmI1LTQyZGEtOWY2ZS1kYWM4MTQzNmRmYWZpZDk3ZmIxMTNmLWI4NTItNGJjMS05MWJmLTc5ZGQxMWUxNDk5Mg==', 'game__id': '758bc985-4171-4c8b-bee3-c7c2ab6780fd', 'at_bat__id': 'b9f80da8-d881-43b5-89f8-af0ebd9c4ac5', 'pitch__id': 'fd93874b-12b5-42da-9f6e-dac81436dfaf'}], 'stats': None}"""
        self.raw = literal_eval(raw_requirements_str)
        #
        self.pitch = self.raw.get('pitch')
        self.at_bat = self.raw.get('at_bat')
        self.zone_pitches = self.raw.get('zone_pitches')
        self.runners = self.raw.get('runners')


class TestRawRequirements2(TestCase):
    def setUp(self):
        #
        raw_requirements_str = """{'at_bat': {'dd_updated__id': 1467229093423, 'description': 'Matt Szczur walks.', 'game__id': '08981bd8-d1d7-48e1-8668-9098b8f7fe90', '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDA4OTgxYmQ4LWQxZDctNDhlMS04NjY4LTkwOThiOGY3ZmU5MGlkMGEwNGUyNDMtMDA4YS00ODhjLWFjZjMtYTFkNDMzNmI2ZTEy', 'parent_api__id': 'pbp', 'id': '0a04e243-008a-488c-acf3-a1d4336b6e12', 'pitchs': [{'pitch': 'ad9e77a5-59ff-4182-89c5-873a97ce6b02'}, {'pitch': '77619054-127a-4180-b4b6-998b3b9e6ab8'}, {'pitch': '76bbe755-8128-453b-bd43-6f2ae10f85f5'}, {'pitch': '57fda296-4ce6-4430-ab81-78d0da39f5a7'}, {'pitch': 'bfa4c342-1dee-4119-b0e1-fa814b46ec70'}], 'hitter_id': 'ea8fad1f-1c47-4f61-b7c7-9c725f02d9a2'}, 'runners': [{'dd_updated__id': 1467229093423, 'at_bat__id': '0a04e243-008a-488c-acf3-a1d4336b6e12', 'first_name': 'Matthew', 'ending_base': 1.0, '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDA4OTgxYmQ4LWQxZDctNDhlMS04NjY4LTkwOThiOGY3ZmU5MGF0X2JhdF9faWQwYTA0ZTI0My0wMDhhLTQ4OGMtYWNmMy1hMWQ0MzM2YjZlMTJwaXRjaF9faWRiZmE0YzM0Mi0xZGVlLTQxMTktYjBlMS1mYTgxNGI0NmVjNzBwYXJlbnRfbGlzdF9faWRydW5uZXJzX19saXN0aWRlYThmYWQxZi0xYzQ3LTRmNjEtYjdjNy05YzcyNWYwMmQ5YTI=', 'preferred_name': 'Matt', 'out': 'false', 'game__id': '08981bd8-d1d7-48e1-8668-9098b8f7fe90', 'outcome_id': 'AD1', 'pitch__id': 'bfa4c342-1dee-4119-b0e1-fa814b46ec70', 'last_name': 'Szczur', 'parent_api__id': 'pbp', 'starting_base': 0.0, 'jersey_number': 20.0, 'id': 'ea8fad1f-1c47-4f61-b7c7-9c725f02d9a2', 'parent_list__id': 'runners__list'}], 'stats': None, 'at_bat_stats': None, 'zone_pitches': [{'dd_updated__id': 1467229029937, 'game__id': '08981bd8-d1d7-48e1-8668-9098b8f7fe90', 'pitch_count': 5.0, 'hitter_hand': 'R', 'pitcher_hand': 'R', 'at_bat__id': '0a04e243-008a-488c-acf3-a1d4336b6e12', 'pitch_type': 'FA', 'pitch__id': 'ad9e77a5-59ff-4182-89c5-873a97ce6b02', 'parent_api__id': 'pbp', 'pitch_zone': 13.0, 'pitch_speed': 95.0, 'id': 'e7f69d9c-f311-466b-8f28-591255b49489', '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDA4OTgxYmQ4LWQxZDctNDhlMS04NjY4LTkwOThiOGY3ZmU5MGF0X2JhdF9faWQwYTA0ZTI0My0wMDhhLTQ4OGMtYWNmMy1hMWQ0MzM2YjZlMTJwaXRjaF9faWRhZDllNzdhNS01OWZmLTQxODItODljNS04NzNhOTdjZTZiMDJpZGU3ZjY5ZDljLWYzMTEtNDY2Yi04ZjI4LTU5MTI1NWI0OTQ4OQ=='}, {'dd_updated__id': 1467229048032, 'game__id': '08981bd8-d1d7-48e1-8668-9098b8f7fe90', 'pitch_count': 6.0, 'hitter_hand': 'R', 'pitcher_hand': 'R', 'at_bat__id': '0a04e243-008a-488c-acf3-a1d4336b6e12', 'pitch_type': 'FA', 'pitch__id': '77619054-127a-4180-b4b6-998b3b9e6ab8', 'parent_api__id': 'pbp', 'pitch_zone': 4.0, 'pitch_speed': 95.0, 'id': 'e7f69d9c-f311-466b-8f28-591255b49489', '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDA4OTgxYmQ4LWQxZDctNDhlMS04NjY4LTkwOThiOGY3ZmU5MGF0X2JhdF9faWQwYTA0ZTI0My0wMDhhLTQ4OGMtYWNmMy1hMWQ0MzM2YjZlMTJwaXRjaF9faWQ3NzYxOTA1NC0xMjdhLTQxODAtYjRiNi05OThiM2I5ZTZhYjhpZGU3ZjY5ZDljLWYzMTEtNDY2Yi04ZjI4LTU5MTI1NWI0OTQ4OQ=='}, {'dd_updated__id': 1467229084251, 'game__id': '08981bd8-d1d7-48e1-8668-9098b8f7fe90', 'pitch_count': 7.0, 'hitter_hand': 'R', 'pitcher_hand': 'R', 'at_bat__id': '0a04e243-008a-488c-acf3-a1d4336b6e12', 'pitch_type': 'SL', 'pitch__id': '76bbe755-8128-453b-bd43-6f2ae10f85f5', 'parent_api__id': 'pbp', 'pitch_zone': 13.0, 'pitch_speed': 82.0, 'id': 'e7f69d9c-f311-466b-8f28-591255b49489', '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDA4OTgxYmQ4LWQxZDctNDhlMS04NjY4LTkwOThiOGY3ZmU5MGF0X2JhdF9faWQwYTA0ZTI0My0wMDhhLTQ4OGMtYWNmMy1hMWQ0MzM2YjZlMTJwaXRjaF9faWQ3NmJiZTc1NS04MTI4LTQ1M2ItYmQ0My02ZjJhZTEwZjg1ZjVpZGU3ZjY5ZDljLWYzMTEtNDY2Yi04ZjI4LTU5MTI1NWI0OTQ4OQ=='}, {'dd_updated__id': 1467229084251, 'game__id': '08981bd8-d1d7-48e1-8668-9098b8f7fe90', 'pitch_count': 8.0, 'hitter_hand': 'R', 'pitcher_hand': 'R', 'at_bat__id': '0a04e243-008a-488c-acf3-a1d4336b6e12', 'pitch_type': 'FA', 'pitch__id': '57fda296-4ce6-4430-ab81-78d0da39f5a7', 'parent_api__id': 'pbp', 'pitch_zone': 13.0, 'pitch_speed': 95.0, 'id': 'e7f69d9c-f311-466b-8f28-591255b49489', '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDA4OTgxYmQ4LWQxZDctNDhlMS04NjY4LTkwOThiOGY3ZmU5MGF0X2JhdF9faWQwYTA0ZTI0My0wMDhhLTQ4OGMtYWNmMy1hMWQ0MzM2YjZlMTJwaXRjaF9faWQ1N2ZkYTI5Ni00Y2U2LTQ0MzAtYWI4MS03OGQwZGEzOWY1YTdpZGU3ZjY5ZDljLWYzMTEtNDY2Yi04ZjI4LTU5MTI1NWI0OTQ4OQ=='}, {'dd_updated__id': 1467229093423, 'game__id': '08981bd8-d1d7-48e1-8668-9098b8f7fe90', 'pitch_count': 9.0, 'hitter_hand': 'R', 'pitcher_hand': 'R', 'at_bat__id': '0a04e243-008a-488c-acf3-a1d4336b6e12', 'pitch_type': 'FA', 'pitch__id': 'bfa4c342-1dee-4119-b0e1-fa814b46ec70', 'parent_api__id': 'pbp', 'pitch_zone': 10.0, 'pitch_speed': 95.0, 'id': 'e7f69d9c-f311-466b-8f28-591255b49489', '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDA4OTgxYmQ4LWQxZDctNDhlMS04NjY4LTkwOThiOGY3ZmU5MGF0X2JhdF9faWQwYTA0ZTI0My0wMDhhLTQ4OGMtYWNmMy1hMWQ0MzM2YjZlMTJwaXRjaF9faWRiZmE0YzM0Mi0xZGVlLTQxMTktYjBlMS1mYTgxNGI0NmVjNzBpZGU3ZjY5ZDljLWYzMTEtNDY2Yi04ZjI4LTU5MTI1NWI0OTQ4OQ=='}], 'pitch': {'dd_updated__id': 1467229093423, 'status': 'official', 'runners__list': {'runner': 'ea8fad1f-1c47-4f61-b7c7-9c725f02d9a2'}, 'updated_at': '2016-06-29T19:38:08Z', 'at_bat__id': '0a04e243-008a-488c-acf3-a1d4336b6e12', 'pitcher': 'e7f69d9c-f311-466b-8f28-591255b49489', 'count__list': {'balls': 4.0, 'strikes': 1.0, 'pitch_count': 5.0, 'outs': 1.0}, 'created_at': '2016-06-29T19:38:04Z', 'flags__list': {'is_bunt': 'false', 'is_hit': 'false', 'is_on_base': 'true', 'is_triple_play': 'false', 'is_bunt_shown': 'false', 'is_double_play': 'false', 'is_ab_over': 'true', 'is_wild_pitch': 'false', 'is_ab': 'false', 'is_passed_ball': 'false'}, 'outcome_id': 'bB', 'parent_api__id': 'pbp', '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDA4OTgxYmQ4LWQxZDctNDhlMS04NjY4LTkwOThiOGY3ZmU5MGF0X2JhdF9faWQwYTA0ZTI0My0wMDhhLTQ4OGMtYWNmMy1hMWQ0MzM2YjZlMTJpZGJmYTRjMzQyLTFkZWUtNDExOS1iMGUxLWZhODE0YjQ2ZWM3MA==', 'game__id': '08981bd8-d1d7-48e1-8668-9098b8f7fe90', 'id': 'bfa4c342-1dee-4119-b0e1-fa814b46ec70'}}"""
        self.raw = literal_eval(raw_requirements_str)
        #
        self.pitch = self.raw.get('pitch')
        self.at_bat = self.raw.get('at_bat')
        self.zone_pitches = self.raw.get('zone_pitches')
        self.runners = self.raw.get('runners')

    def test_at_bat_has_description(self):
        logger.info(self.at_bat)
        description = self.at_bat.get('description')
        logger.info('description[%s]' % description)
        self.assertIsNotNone(description)

        class AtBatReducer(Reducer):
            remove_fields = [
                '_id',
                'errors__list',
                'parent_api__id',
                'pitchs',
                'game__id',
                'id',
                'created_at',
                'updated_at',
                'runners__list',
                'count__list',
                'flags__list',
                'fielders__list',
                'status',
                'pitcher',
                'hit_location',
                'hit_type',
            ]

        class AtBatShrinker(Shrinker):
            fields = {
                'at_bat__id': 'srid',
                'dd_updated__id': 'ts',
                'hitter_id': 'srid_hitter',
                'outcome_id': 'oid',
                'description': 'oid_description',
            }

        r = AtBatReducer(self.at_bat)
        reduced = r.reduce()
        logger.info('reduced: %s' % reduced)

        s = AtBatShrinker(reduced)
        shrunk = s.shrink()
        logger.info('shrunk: %s' % shrunk)


class TestLinkedParts(TestCase):
    def setUp(self):
        # get the updates ordered this way >>>   ./manage.py playupdate 5269090 5269094
        #
        # updates = Update.objects.filter(o__contains='1467237448660').order_by('ts')

        # print out updates the way they are formatted below
        #
        # for u in updates:
        #     print(u.pk, u.ts, u.ns, u.o)
        #     print( '' )

        # pk      ts                               ns          o
        # 5269090 2016-06-29 21:57:39.731651+00:00 mlb.pitcher {'dd_updated__id': 1467237448660, 'hitter_hand': 'R', 'game__id': '3e522dc1-0435-4556-b30a-58dc5565efe0', 'pitcher_hand': 'R', 'pitch__id': '4275e881-c745-41e4-a91c-abd12358be16', 'at_bat__id': 'e8678617-3a9b-44f1-b90d-68919b064c85', 'id': '48347189-837d-4453-9e54-d3be3b9fc639', 'pitch_type': 'SL', 'pitch_count': 15.0, 'parent_api__id': 'pbp', 'pitch_zone': 12.0, 'pitch_speed': 85.0, '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDNlNTIyZGMxLTA0MzUtNDU1Ni1iMzBhLTU4ZGM1NTY1ZWZlMGF0X2JhdF9faWRlODY3ODYxNy0zYTliLTQ0ZjEtYjkwZC02ODkxOWIwNjRjODVwaXRjaF9faWQ0Mjc1ZTg4MS1jNzQ1LTQxZTQtYTkxYy1hYmQxMjM1OGJlMTZpZDQ4MzQ3MTg5LTgzN2QtNDQ1My05ZTU0LWQzYmUzYjlmYzYzOQ=='}
        #
        # 5269091 2016-06-29 21:57:39.824714+00:00 mlb.runner {'_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDNlNTIyZGMxLTA0MzUtNDU1Ni1iMzBhLTU4ZGM1NTY1ZWZlMGF0X2JhdF9faWRlODY3ODYxNy0zYTliLTQ0ZjEtYjkwZC02ODkxOWIwNjRjODVwaXRjaF9faWQ0Mjc1ZTg4MS1jNzQ1LTQxZTQtYTkxYy1hYmQxMjM1OGJlMTZwYXJlbnRfbGlzdF9faWRydW5uZXJzX19saXN0aWRmYjA2MWM3Ny01MjUzLTQxODEtYWQ3Yi1jNjhlZjE4YWE1MTE=', 'last_name': 'Pujols', 'pitch__id': '4275e881-c745-41e4-a91c-abd12358be16', 'starting_base': 1.0, 'id': 'fb061c77-5253-4181-ad7b-c68ef18aa511', 'game__id': '3e522dc1-0435-4556-b30a-58dc5565efe0', 'parent_list__id': 'runners__list', 'parent_api__id': 'pbp', 'preferred_name': 'Albert', 'dd_updated__id': 1467237448660, 'ending_base': 1.0, 'jersey_number': 5.0, 'at_bat__id': 'e8678617-3a9b-44f1-b90d-68919b064c85', 'first_name': 'Jose', 'out': 'false'}
        #
        # 5269092 2016-06-29 21:57:39.829554+00:00 mlb.runner {'jersey_number': 27.0, 'first_name': 'Michael', 'starting_base': 2.0, 'out': 'false', 'game__id': '3e522dc1-0435-4556-b30a-58dc5565efe0', 'last_name': 'Trout', 'pitch__id': '4275e881-c745-41e4-a91c-abd12358be16', '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDNlNTIyZGMxLTA0MzUtNDU1Ni1iMzBhLTU4ZGM1NTY1ZWZlMGF0X2JhdF9faWRlODY3ODYxNy0zYTliLTQ0ZjEtYjkwZC02ODkxOWIwNjRjODVwaXRjaF9faWQ0Mjc1ZTg4MS1jNzQ1LTQxZTQtYTkxYy1hYmQxMjM1OGJlMTZwYXJlbnRfbGlzdF9faWRydW5uZXJzX19saXN0aWQ3ZjUxODYzMi0yZDVkLTQ4YzgtYjk5NC0yZDRkNDNhMWVmM2I=', 'ending_base': 2.0, 'at_bat__id': 'e8678617-3a9b-44f1-b90d-68919b064c85', 'preferred_name': 'Mike', 'parent_list__id': 'runners__list', 'id': '7f518632-2d5d-48c8-b994-2d4d43a1ef3b', 'parent_api__id': 'pbp', 'dd_updated__id': 1467237448660}
        #
        # 5269093 2016-06-29 21:57:39.860150+00:00 mlb.pitch {'dd_updated__id': 1467237448660, 'game__id': '3e522dc1-0435-4556-b30a-58dc5565efe0', 'outcome_id': 'bB', 'created_at': '2016-06-29T21:57:19Z', 'pitcher': '48347189-837d-4453-9e54-d3be3b9fc639', 'count__list': {'balls': 1.0, 'strikes': 0.0, 'outs': 1.0, 'pitch_count': 1.0}, 'at_bat__id': 'e8678617-3a9b-44f1-b90d-68919b064c85', 'runners__list': [{'runner': 'fb061c77-5253-4181-ad7b-c68ef18aa511'}, {'runner': '7f518632-2d5d-48c8-b994-2d4d43a1ef3b'}], 'flags__list': {'is_wild_pitch': 'false', 'is_bunt_shown': 'false', 'is_triple_play': 'false', 'is_hit': 'false', 'is_ab_over': 'false', 'is_passed_ball': 'false', 'is_on_base': 'false', 'is_double_play': 'false', 'is_bunt': 'false', 'is_ab': 'false'}, 'id': '4275e881-c745-41e4-a91c-abd12358be16', 'parent_api__id': 'pbp', 'updated_at': '2016-06-29T21:57:23Z', 'status': 'official', '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDNlNTIyZGMxLTA0MzUtNDU1Ni1iMzBhLTU4ZGM1NTY1ZWZlMGF0X2JhdF9faWRlODY3ODYxNy0zYTliLTQ0ZjEtYjkwZC02ODkxOWIwNjRjODVpZDQyNzVlODgxLWM3NDUtNDFlNC1hOTFjLWFiZDEyMzU4YmUxNg=='}
        #
        # 5269094 2016-06-29 21:57:39.989930+00:00 mlb.at_bat {'hitter_id':
        # 'd28626fe-94c6-4fdb-bcf3-ba7b1c5180e6', '_id':
        # 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDNlNTIyZGMxLTA0MzUtNDU1Ni1iMzBhLTU4ZGM1NTY1ZWZlMGlkZTg2Nzg2MTctM2E5Yi00NGYxLWI5MGQtNjg5MTliMDY0Yzg1',
        # 'dd_updated__id': 1467237448660, 'id':
        # 'e8678617-3a9b-44f1-b90d-68919b064c85', 'game__id':
        # '3e522dc1-0435-4556-b30a-58dc5565efe0', 'pitch':
        # '4275e881-c745-41e4-a91c-abd12358be16', 'parent_api__id': 'pbp'}

        self.zone_pitch = literal_eval(
            """{'dd_updated__id': 1467237448660, 'hitter_hand': 'R', 'game__id': '3e522dc1-0435-4556-b30a-58dc5565efe0', 'pitcher_hand': 'R', 'pitch__id': '4275e881-c745-41e4-a91c-abd12358be16', 'at_bat__id': 'e8678617-3a9b-44f1-b90d-68919b064c85', 'id': '48347189-837d-4453-9e54-d3be3b9fc639', 'pitch_type': 'SL', 'pitch_count': 15.0, 'parent_api__id': 'pbp', 'pitch_zone': 12.0, 'pitch_speed': 85.0, '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDNlNTIyZGMxLTA0MzUtNDU1Ni1iMzBhLTU4ZGM1NTY1ZWZlMGF0X2JhdF9faWRlODY3ODYxNy0zYTliLTQ0ZjEtYjkwZC02ODkxOWIwNjRjODVwaXRjaF9faWQ0Mjc1ZTg4MS1jNzQ1LTQxZTQtYTkxYy1hYmQxMjM1OGJlMTZpZDQ4MzQ3MTg5LTgzN2QtNDQ1My05ZTU0LWQzYmUzYjlmYzYzOQ=='}""")
        self.runner1 = literal_eval(
            """{'_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDNlNTIyZGMxLTA0MzUtNDU1Ni1iMzBhLTU4ZGM1NTY1ZWZlMGF0X2JhdF9faWRlODY3ODYxNy0zYTliLTQ0ZjEtYjkwZC02ODkxOWIwNjRjODVwaXRjaF9faWQ0Mjc1ZTg4MS1jNzQ1LTQxZTQtYTkxYy1hYmQxMjM1OGJlMTZwYXJlbnRfbGlzdF9faWRydW5uZXJzX19saXN0aWRmYjA2MWM3Ny01MjUzLTQxODEtYWQ3Yi1jNjhlZjE4YWE1MTE=', 'last_name': 'Pujols', 'pitch__id': '4275e881-c745-41e4-a91c-abd12358be16', 'starting_base': 1.0, 'id': 'fb061c77-5253-4181-ad7b-c68ef18aa511', 'game__id': '3e522dc1-0435-4556-b30a-58dc5565efe0', 'parent_list__id': 'runners__list', 'parent_api__id': 'pbp', 'preferred_name': 'Albert', 'dd_updated__id': 1467237448660, 'ending_base': 1.0, 'jersey_number': 5.0, 'at_bat__id': 'e8678617-3a9b-44f1-b90d-68919b064c85', 'first_name': 'Jose', 'out': 'false'}""")
        self.runner2 = literal_eval(
            """{'jersey_number': 27.0, 'first_name': 'Michael', 'starting_base': 2.0, 'out': 'false', 'game__id': '3e522dc1-0435-4556-b30a-58dc5565efe0', 'last_name': 'Trout', 'pitch__id': '4275e881-c745-41e4-a91c-abd12358be16', '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDNlNTIyZGMxLTA0MzUtNDU1Ni1iMzBhLTU4ZGM1NTY1ZWZlMGF0X2JhdF9faWRlODY3ODYxNy0zYTliLTQ0ZjEtYjkwZC02ODkxOWIwNjRjODVwaXRjaF9faWQ0Mjc1ZTg4MS1jNzQ1LTQxZTQtYTkxYy1hYmQxMjM1OGJlMTZwYXJlbnRfbGlzdF9faWRydW5uZXJzX19saXN0aWQ3ZjUxODYzMi0yZDVkLTQ4YzgtYjk5NC0yZDRkNDNhMWVmM2I=', 'ending_base': 2.0, 'at_bat__id': 'e8678617-3a9b-44f1-b90d-68919b064c85', 'preferred_name': 'Mike', 'parent_list__id': 'runners__list', 'id': '7f518632-2d5d-48c8-b994-2d4d43a1ef3b', 'parent_api__id': 'pbp', 'dd_updated__id': 1467237448660}""")
        self.runners = [self.runner1, self.runner2]
        self.pitch = literal_eval(
            """{'dd_updated__id': 1467237448660, 'game__id': '3e522dc1-0435-4556-b30a-58dc5565efe0', 'outcome_id': 'bB', 'created_at': '2016-06-29T21:57:19Z', 'pitcher': '48347189-837d-4453-9e54-d3be3b9fc639', 'count__list': {'balls': 1.0, 'strikes': 0.0, 'outs': 1.0, 'pitch_count': 1.0}, 'at_bat__id': 'e8678617-3a9b-44f1-b90d-68919b064c85', 'runners__list': [{'runner': 'fb061c77-5253-4181-ad7b-c68ef18aa511'}, {'runner': '7f518632-2d5d-48c8-b994-2d4d43a1ef3b'}], 'flags__list': {'is_wild_pitch': 'false', 'is_bunt_shown': 'false', 'is_triple_play': 'false', 'is_hit': 'false', 'is_ab_over': 'false', 'is_passed_ball': 'false', 'is_on_base': 'false', 'is_double_play': 'false', 'is_bunt': 'false', 'is_ab': 'false'}, 'id': '4275e881-c745-41e4-a91c-abd12358be16', 'parent_api__id': 'pbp', 'updated_at': '2016-06-29T21:57:23Z', 'status': 'official', '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDNlNTIyZGMxLTA0MzUtNDU1Ni1iMzBhLTU4ZGM1NTY1ZWZlMGF0X2JhdF9faWRlODY3ODYxNy0zYTliLTQ0ZjEtYjkwZC02ODkxOWIwNjRjODVpZDQyNzVlODgxLWM3NDUtNDFlNC1hOTFjLWFiZDEyMzU4YmUxNg=='}""")
        self.at_bat = literal_eval(
            """{'hitter_id': 'd28626fe-94c6-4fdb-bcf3-ba7b1c5180e6', '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDNlNTIyZGMxLTA0MzUtNDU1Ni1iMzBhLTU4ZGM1NTY1ZWZlMGlkZTg2Nzg2MTctM2E5Yi00NGYxLWI5MGQtNjg5MTliMDY0Yzg1', 'dd_updated__id': 1467237448660, 'id': 'e8678617-3a9b-44f1-b90d-68919b064c85', 'game__id': '3e522dc1-0435-4556-b30a-58dc5565efe0', 'pitch': '4275e881-c745-41e4-a91c-abd12358be16', 'parent_api__id': 'pbp'}""")

    def test_it(self):
        logger.info('')
        logger.info('zone_pitch: %s' % self.zone_pitch)
        logger.info('')
        logger.info('runners: %s' % self.runners)
        logger.info('')
        logger.info('pitch: %s' % self.pitch)
        logger.info('')
        logger.info('at_bat: %s' % self.at_bat)
        logger.info('')

    # class TestBuildLinkedPbpStatsData(TestCase):
    #
    #     def setUp(self):
    #         self.parser = PitchPbp()
    #         self.raw = literal_eval("""{'at_bat_stats': None, 'stats': None, 'pitch': {'outcome_id': 'aD', 'dd_updated__id': 1467237502982, 'parent_api__id': 'pbp', 'hit_location': 9.0, 'id': '6143553e-2d95-47a5-bc99-21fb5551d490', 'game__id': '9fd85ce8-c650-4cdb-8ff6-a5233e276b74', 'status': 'official', 'pitcher': '90aa4b7f-94b5-40e7-882f-5d2aa8fe2c95', 'hit_type': 'LD', 'updated_at': '2016-06-29T21:58:16Z', 'runners__list': [{'runner': '7c9c97fd-7a89-49e1-830b-0274a5c2209a'}, {'runner': 'd598fe0d-8402-4707-b05d-4663a1c3cbe7'}, {'runner': '468c82b9-425a-4986-a862-e1ae9de32a7c'}], 'count__list': {'balls': 1.0, 'pitch_count': 2.0, 'outs': 1.0, 'strikes': 0.0}, '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDlmZDg1Y2U4LWM2NTAtNGNkYi04ZmY2LWE1MjMzZTI3NmI3NGF0X2JhdF9faWQ2ZTIzYjEyYi1kZDU2LTRhYjctOGQzNy05ZGE1ZTM1YzdhZDRpZDYxNDM1NTNlLTJkOTUtNDdhNS1iYzk5LTIxZmI1NTUxZDQ5MA==', 'flags__list': {'is_triple_play': 'false', 'is_ab_over': 'true', 'is_passed_ball': 'false', 'is_bunt': 'false', 'is_wild_pitch': 'false', 'is_ab': 'true', 'is_bunt_shown': 'false', 'is_on_base': 'true', 'is_double_play': 'false', 'is_hit': 'true'}, 'created_at': '2016-06-29T21:58:12Z', 'at_bat__id': '6e23b12b-dd56-4ab7-8d37-9da5e35c7ad4'}, 'zone_pitches': [{'pitch_type': 'CU', 'dd_updated__id': 1467237484860, 'pitch_speed': 77.0, 'hitter_hand': 'R', 'parent_api__id': 'pbp', 'id': '90aa4b7f-94b5-40e7-882f-5d2aa8fe2c95', 'game__id': '9fd85ce8-c650-4cdb-8ff6-a5233e276b74', 'pitch__id': 'c580994b-d74e-4780-a694-ffdf1f08f0c3', 'at_bat__id': '6e23b12b-dd56-4ab7-8d37-9da5e35c7ad4', '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDlmZDg1Y2U4LWM2NTAtNGNkYi04ZmY2LWE1MjMzZTI3NmI3NGF0X2JhdF9faWQ2ZTIzYjEyYi1kZDU2LTRhYjctOGQzNy05ZGE1ZTM1YzdhZDRwaXRjaF9faWRjNTgwOTk0Yi1kNzRlLTQ3ODAtYTY5NC1mZmRmMWYwOGYwYzNpZDkwYWE0YjdmLTk0YjUtNDBlNy04ODJmLTVkMmFhOGZlMmM5NQ==', 'pitch_count': 10.0, 'pitcher_hand': 'R', 'pitch_zone': 13.0}, {'dd_updated__id': 1467237548314, 'pitch_speed': 93.0, 'hitter_hand': 'R', 'parent_api__id': 'pbp', 'id': '90aa4b7f-94b5-40e7-882f-5d2aa8fe2c95', 'game__id': '9fd85ce8-c650-4cdb-8ff6-a5233e276b74', 'at_bat__id': '6e23b12b-dd56-4ab7-8d37-9da5e35c7ad4', 'pitch_type': 'FA', 'pitch__id': '6143553e-2d95-47a5-bc99-21fb5551d490', '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDlmZDg1Y2U4LWM2NTAtNGNkYi04ZmY2LWE1MjMzZTI3NmI3NGF0X2JhdF9faWQ2ZTIzYjEyYi1kZDU2LTRhYjctOGQzNy05ZGE1ZTM1YzdhZDRwaXRjaF9faWQ2MTQzNTUzZS0yZDk1LTQ3YTUtYmM5OS0yMWZiNTU1MWQ0OTBpZDkwYWE0YjdmLTk0YjUtNDBlNy04ODJmLTVkMmFhOGZlMmM5NQ==', 'pitch_count': 11.0, 'pitcher_hand': 'R', 'pitch_zone': 4.0}], 'runners': [{'outcome_id': 'AD2', 'dd_updated__id': 1467237502982, 'preferred_name': 'Paul', 'parent_api__id': 'pbp', 'jersey_number': 44.0, 'game__id': '9fd85ce8-c650-4cdb-8ff6-a5233e276b74', 'starting_base': 0.0, 'pitch__id': '6143553e-2d95-47a5-bc99-21fb5551d490', 'first_name': 'Paul', 'last_name': 'Goldschmidt', 'out': 'false', 'id': '7c9c97fd-7a89-49e1-830b-0274a5c2209a', 'parent_list__id': 'runners__list', '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDlmZDg1Y2U4LWM2NTAtNGNkYi04ZmY2LWE1MjMzZTI3NmI3NGF0X2JhdF9faWQ2ZTIzYjEyYi1kZDU2LTRhYjctOGQzNy05ZGE1ZTM1YzdhZDRwaXRjaF9faWQ2MTQzNTUzZS0yZDk1LTQ3YTUtYmM5OS0yMWZiNTU1MWQ0OTBwYXJlbnRfbGlzdF9faWRydW5uZXJzX19saXN0aWQ3YzljOTdmZC03YTg5LTQ5ZTEtODMwYi0wMjc0YTVjMjIwOWE=', 'ending_base': 2.0, 'at_bat__id': '6e23b12b-dd56-4ab7-8d37-9da5e35c7ad4'}, {'outcome_id': 'ERN', 'dd_updated__id': 1467237502982, 'preferred_name': 'Philip', 'parent_api__id': 'pbp', 'jersey_number': 15.0, 'game__id': '9fd85ce8-c650-4cdb-8ff6-a5233e276b74', 'starting_base': 1.0, 'pitch__id': '6143553e-2d95-47a5-bc99-21fb5551d490', 'first_name': 'Philip', 'last_name': 'Gosselin', 'out': 'false', 'id': 'd598fe0d-8402-4707-b05d-4663a1c3cbe7', 'parent_list__id': 'runners__list', '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDlmZDg1Y2U4LWM2NTAtNGNkYi04ZmY2LWE1MjMzZTI3NmI3NGF0X2JhdF9faWQ2ZTIzYjEyYi1kZDU2LTRhYjctOGQzNy05ZGE1ZTM1YzdhZDRwaXRjaF9faWQ2MTQzNTUzZS0yZDk1LTQ3YTUtYmM5OS0yMWZiNTU1MWQ0OTBwYXJlbnRfbGlzdF9faWRydW5uZXJzX19saXN0aWRkNTk4ZmUwZC04NDAyLTQ3MDctYjA1ZC00NjYzYTFjM2NiZTc=', 'description': 'Philip Gosselin scores.', 'ending_base': 4.0, 'at_bat__id': '6e23b12b-dd56-4ab7-8d37-9da5e35c7ad4'}, {'outcome_id': 'ERN', 'dd_updated__id': 1467237502982, 'preferred_name': 'Michael', 'parent_api__id': 'pbp', 'id': '468c82b9-425a-4986-a862-e1ae9de32a7c', 'game__id': '9fd85ce8-c650-4cdb-8ff6-a5233e276b74', 'starting_base': 3.0, 'pitch__id': '6143553e-2d95-47a5-bc99-21fb5551d490', 'first_name': 'Michael', 'last_name': 'Bourn', 'at_bat__id': '6e23b12b-dd56-4ab7-8d37-9da5e35c7ad4', 'jersey_number': 1.0, 'parent_list__id': 'runners__list', '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDlmZDg1Y2U4LWM2NTAtNGNkYi04ZmY2LWE1MjMzZTI3NmI3NGF0X2JhdF9faWQ2ZTIzYjEyYi1kZDU2LTRhYjctOGQzNy05ZGE1ZTM1YzdhZDRwaXRjaF9faWQ2MTQzNTUzZS0yZDk1LTQ3YTUtYmM5OS0yMWZiNTU1MWQ0OTBwYXJlbnRfbGlzdF9faWRydW5uZXJzX19saXN0aWQ0NjhjODJiOS00MjVhLTQ5ODYtYTg2Mi1lMWFlOWRlMzJhN2M=', 'description': 'Michael Bourn scores.', 'ending_base': 4.0, 'out': 'false'}], 'at_bat': {'dd_updated__id': 1467237502982, 'hitter_id': '7c9c97fd-7a89-49e1-830b-0274a5c2209a', 'parent_api__id': 'pbp', 'id': '6e23b12b-dd56-4ab7-8d37-9da5e35c7ad4', '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDlmZDg1Y2U4LWM2NTAtNGNkYi04ZmY2LWE1MjMzZTI3NmI3NGlkNmUyM2IxMmItZGQ1Ni00YWI3LThkMzctOWRhNWUzNWM3YWQ0', 'game__id': '9fd85ce8-c650-4cdb-8ff6-a5233e276b74', 'description': 'Paul Goldschmidt doubles to deep right center field. Philip Gosselin scores. Michael Bourn scores.', 'pitchs': [{'pitch': 'c580994b-d74e-4780-a694-ffdf1f08f0c3'}, {'pitch': '6143553e-2d95-47a5-bc99-21fb5551d490'}]}}""")
    #
    #     def test_reconstruct_from_pitch(self):
    #         # set the pitch srid, and the ts so the class thinks they were set up normally
    #         # as they would have been during parse()
    #         # self.parser.srid_pitch  = self.raw.get('pitch').get('id')
    #         # self.parser.ts          = self.raw.get('pitch').get('dd_updated__id')
    #
    #         #
    #         data = self.parser.build_linked_pbp_stats_data(self.raw)
    #         print(str(data))

    def test_send_because_of_runner_with_steal(self):
        # runner object with 'SB2' outcome ... 2nd base was stolen
        runner = literal_eval(
            """{'game__id': '5293a648-c570-440a-8230-9dba92249e5d', 'parent_api__id': 'pbp', 'pitch__id': 'b1139c07-d64a-4e62-931a-f0dd20adecf1', '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDUyOTNhNjQ4LWM1NzAtNDQwYS04MjMwLTlkYmE5MjI0OWU1ZGF0X2JhdF9faWQ0ODk1ZWQxZS1jMTU1LTRlZmUtOWFkMi1mZWY2MzRhNTJlODJwaXRjaF9faWRiMTEzOWMwNy1kNjRhLTRlNjItOTMxYS1mMGRkMjBhZGVjZjFwYXJlbnRfbGlzdF9faWRydW5uZXJzX19saXN0aWRkODIwMTc1Mi1jNjcwLTQxMDQtYjhiYy0xZmI4YWE3Y2IyNmY=', 'last_name': 'Arcia', 'description': 'Oswaldo Arcia steals second.', 'outcome_id': 'SB2', 'ending_base': 2.0, 'first_name': 'Oswaldo', 'preferred_name': 'Oswaldo', 'jersey_number': 9.0, 'out': 'false', 'dd_updated__id': 1467338190681, 'id': 'd8201752-c670-4104-b8bc-1fb8aa7cb26f', 'at_bat__id': '4895ed1e-c155-4efe-9ad2-fef634a52e82', 'starting_base': 1.0, 'parent_list__id': 'runners__list'}""")
