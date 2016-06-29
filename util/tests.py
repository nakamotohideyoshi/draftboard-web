#
# util/tests.py

from unittest import TestCase
from ast import literal_eval
from util.dicts import (
    Reducer,
    Shrinker,
)

class ReducerTest(TestCase):

    def setUp(self):
        pass # TODO

    def test_exception_remove_fields_not_set(self):
        """
        exception should be thrown if child class
        does not set 'remove_fields' list
        """
        class TestReducer(Reducer): pass
        data = {} # for this test, doesnt need any key values
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
        data = 1 # purposely invalid for this test

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
        tr = TestReducer({}) # data doesnt matter for this test
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
        d = {} # str2bool should return a dict
        self.assertTrue(isinstance(tr.str2bool(d), dict))
        l = [] # str2bool should return a list
        self.assertTrue(isinstance(tr.str2bool(l), list))

    def test_removes_specified_fields(self):
        """
        a simple test to make sure its working as intended

        this test also ensures the original data is not modified
        """
        data = {
            'key1' : 'val1',
            'key2' : 'val2',
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
        pass # TODO

    def test_exception_fields_not_set(self):
        """
        creating an instance of a subclass that has not
        set the fields property raises exception
        """
        class TestFieldsNotSetShrinker(Shrinker): pass
        data = {} # for this test, doesnt need any key values
        self.assertRaises(
            Shrinker.FieldsNotSetException,
            lambda: TestFieldsNotSetShrinker(data)
        )

    def test_does_not_rename_to_existing_field(self):
        """
        shrinker should not rename a field to an existing key name
        """
        data = {
            'key99':'val99',
            'key1':'val1'
        }
        class TestShrinker(Shrinker):
            fields = {'key99':'key1'}

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
            'key99':'val99',
            'key1':'val1'
        }
        orig = data.copy()
        class TestShrinker(Shrinker):
            fields = {
                'key99':'key9999',
                'key1':'key1111'
            }

        ts = TestShrinker(data)
        shrunk = ts.shrink()

        # make sure 'key1' is still the key for 'val1'
        # which is effectively how we know we didnt overwrite
        # the existing 'key1' value!
        self.assertTrue(ts.data == orig)

#
##################################################################################################
# tests below here are not really for the system so much as they are for quick examples
##################################################################################################

class TestRawRequirements(TestCase):

    def setUp(self):
        #
        raw_requirements_str = """{'at_bat_stats': None, 'runners': [{'last_name': 'Prado', 'starting_base': 1.0, 'parent_api__id': 'pbp', 'id': '933a0bc9-26c0-478e-982c-01fd8ffe0614', 'ending_base': 1.0, 'out': 'false', 'at_bat__id': 'b9f80da8-d881-43b5-89f8-af0ebd9c4ac5', 'jersey_number': 14.0, 'dd_updated__id': 1467229174873, 'preferred_name': 'Martin', '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDc1OGJjOTg1LTQxNzEtNGM4Yi1iZWUzLWM3YzJhYjY3ODBmZGF0X2JhdF9faWRiOWY4MGRhOC1kODgxLTQzYjUtODlmOC1hZjBlYmQ5YzRhYzVwaXRjaF9faWRmZDkzODc0Yi0xMmI1LTQyZGEtOWY2ZS1kYWM4MTQzNmRmYWZwYXJlbnRfbGlzdF9faWRydW5uZXJzX19saXN0aWQ5MzNhMGJjOS0yNmMwLTQ3OGUtOTgyYy0wMWZkOGZmZTA2MTQ=', 'parent_list__id': 'runners__list', 'game__id': '758bc985-4171-4c8b-bee3-c7c2ab6780fd', 'first_name': 'Martin', 'pitch__id': 'fd93874b-12b5-42da-9f6e-dac81436dfaf'}], 'at_bat': {'id': 'b9f80da8-d881-43b5-89f8-af0ebd9c4ac5', 'dd_updated__id': 1467229174873, 'pitchs': [{'pitch': '9e27aede-76e2-410e-aff2-0be26834a443'}, {'pitch': 'de3fefa7-90c6-4524-bdd2-e75b75538e1c'}, {'pitch': '1f3909cb-fd36-4193-8b87-9c67cd8aabc4'}, {'pitch': 'fd93874b-12b5-42da-9f6e-dac81436dfaf'}], '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDc1OGJjOTg1LTQxNzEtNGM4Yi1iZWUzLWM3YzJhYjY3ODBmZGlkYjlmODBkYTgtZDg4MS00M2I1LTg5ZjgtYWYwZWJkOWM0YWM1', 'hitter_id': '42cb5171-ffa3-4600-9c41-dbc3805206ea', 'game__id': '758bc985-4171-4c8b-bee3-c7c2ab6780fd', 'parent_api__id': 'pbp'}, 'pitch': {'outcome_id': 'bB', 'at_bat__id': 'b9f80da8-d881-43b5-89f8-af0ebd9c4ac5', 'parent_api__id': 'pbp', 'id': 'fd93874b-12b5-42da-9f6e-dac81436dfaf', 'updated_at': '2016-06-29T19:39:29Z', 'status': 'official', 'pitcher': '97fb113f-b852-4bc1-91bf-79dd11e14992', 'dd_updated__id': 1467229174873, '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDc1OGJjOTg1LTQxNzEtNGM4Yi1iZWUzLWM3YzJhYjY3ODBmZGF0X2JhdF9faWRiOWY4MGRhOC1kODgxLTQzYjUtODlmOC1hZjBlYmQ5YzRhYzVpZGZkOTM4NzRiLTEyYjUtNDJkYS05ZjZlLWRhYzgxNDM2ZGZhZg==', 'game__id': '758bc985-4171-4c8b-bee3-c7c2ab6780fd', 'created_at': '2016-06-29T19:39:27Z', 'count__list': {'outs': 0.0, 'balls': 2.0, 'pitch_count': 4.0, 'strikes': 2.0}, 'flags__list': {'is_ab': 'false', 'is_on_base': 'false', 'is_bunt': 'false', 'is_passed_ball': 'false', 'is_ab_over': 'false', 'is_wild_pitch': 'false', 'is_double_play': 'false', 'is_hit': 'false', 'is_bunt_shown': 'false', 'is_triple_play': 'false'}, 'runners__list': {'runner': '933a0bc9-26c0-478e-982c-01fd8ffe0614'}}, 'zone_pitches': [{'id': '97fb113f-b852-4bc1-91bf-79dd11e14992', 'pitch_speed': 92.0, 'parent_api__id': 'pbp', 'pitch_type': 'FA', 'pitch_count': 20.0, 'pitch_zone': 8.0, 'dd_updated__id': 1467229093256, 'hitter_hand': 'L', 'pitcher_hand': 'R', '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDc1OGJjOTg1LTQxNzEtNGM4Yi1iZWUzLWM3YzJhYjY3ODBmZGF0X2JhdF9faWRiOWY4MGRhOC1kODgxLTQzYjUtODlmOC1hZjBlYmQ5YzRhYzVwaXRjaF9faWQ5ZTI3YWVkZS03NmUyLTQxMGUtYWZmMi0wYmUyNjgzNGE0NDNpZDk3ZmIxMTNmLWI4NTItNGJjMS05MWJmLTc5ZGQxMWUxNDk5Mg==', 'game__id': '758bc985-4171-4c8b-bee3-c7c2ab6780fd', 'at_bat__id': 'b9f80da8-d881-43b5-89f8-af0ebd9c4ac5', 'pitch__id': '9e27aede-76e2-410e-aff2-0be26834a443'}, {'id': '97fb113f-b852-4bc1-91bf-79dd11e14992', 'pitch_speed': 86.0, 'parent_api__id': 'pbp', 'pitch_type': 'SL', 'pitch_count': 21.0, 'pitch_zone': 1.0, 'dd_updated__id': 1467229147682, 'hitter_hand': 'L', 'pitcher_hand': 'R', '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDc1OGJjOTg1LTQxNzEtNGM4Yi1iZWUzLWM3YzJhYjY3ODBmZGF0X2JhdF9faWRiOWY4MGRhOC1kODgxLTQzYjUtODlmOC1hZjBlYmQ5YzRhYzVwaXRjaF9faWRkZTNmZWZhNy05MGM2LTQ1MjQtYmRkMi1lNzViNzU1MzhlMWNpZDk3ZmIxMTNmLWI4NTItNGJjMS05MWJmLTc5ZGQxMWUxNDk5Mg==', 'game__id': '758bc985-4171-4c8b-bee3-c7c2ab6780fd', 'at_bat__id': 'b9f80da8-d881-43b5-89f8-af0ebd9c4ac5', 'pitch__id': 'de3fefa7-90c6-4524-bdd2-e75b75538e1c'}, {'id': '97fb113f-b852-4bc1-91bf-79dd11e14992', 'pitch_speed': 87.0, 'parent_api__id': 'pbp', 'pitch_type': 'SL', 'pitch_count': 22.0, 'pitch_zone': 13.0, 'dd_updated__id': 1467229156775, 'hitter_hand': 'L', 'pitcher_hand': 'R', '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDc1OGJjOTg1LTQxNzEtNGM4Yi1iZWUzLWM3YzJhYjY3ODBmZGF0X2JhdF9faWRiOWY4MGRhOC1kODgxLTQzYjUtODlmOC1hZjBlYmQ5YzRhYzVwaXRjaF9faWQxZjM5MDljYi1mZDM2LTQxOTMtOGI4Ny05YzY3Y2Q4YWFiYzRpZDk3ZmIxMTNmLWI4NTItNGJjMS05MWJmLTc5ZGQxMWUxNDk5Mg==', 'game__id': '758bc985-4171-4c8b-bee3-c7c2ab6780fd', 'at_bat__id': 'b9f80da8-d881-43b5-89f8-af0ebd9c4ac5', 'pitch__id': '1f3909cb-fd36-4193-8b87-9c67cd8aabc4'}, {'id': '97fb113f-b852-4bc1-91bf-79dd11e14992', 'pitch_speed': 92.0, 'parent_api__id': 'pbp', 'pitch_type': 'FA', 'pitch_count': 23.0, 'pitch_zone': 13.0, 'dd_updated__id': 1467229174873, 'hitter_hand': 'L', 'pitcher_hand': 'R', '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDc1OGJjOTg1LTQxNzEtNGM4Yi1iZWUzLWM3YzJhYjY3ODBmZGF0X2JhdF9faWRiOWY4MGRhOC1kODgxLTQzYjUtODlmOC1hZjBlYmQ5YzRhYzVwaXRjaF9faWRmZDkzODc0Yi0xMmI1LTQyZGEtOWY2ZS1kYWM4MTQzNmRmYWZpZDk3ZmIxMTNmLWI4NTItNGJjMS05MWJmLTc5ZGQxMWUxNDk5Mg==', 'game__id': '758bc985-4171-4c8b-bee3-c7c2ab6780fd', 'at_bat__id': 'b9f80da8-d881-43b5-89f8-af0ebd9c4ac5', 'pitch__id': 'fd93874b-12b5-42da-9f6e-dac81436dfaf'}], 'stats': None}"""
        self.raw = literal_eval(raw_requirements_str)
        self.pitch = self.raw.get('pitch')
        self.at_bat = self.raw.get('at_bat')
        self.zone_pitches = self.raw.get('zone_pitches')
        self.runners = self.raw.get('runners')




