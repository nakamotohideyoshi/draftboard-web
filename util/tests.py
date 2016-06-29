#
# util/tests.py

from unittest import TestCase
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
