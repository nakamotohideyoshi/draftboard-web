#
# dataden/tests.py

from django.test import TestCase

from testfixtures import Replacer,test_datetime
from test.classes import AbstractTest
from dataden.util.hsh import Hashable, InvalidArgumentException, \
                             ObjectNotHashableException, InvalidCryptoException

from dataden.util.simpletimer import SimpleTimer
from dataden.classes import DataDen

import datetime
import django
import time
import psycopg2 # for IntegrityError exception

class TestHashable(TestCase):
    """
    tests for the Hashable class
    """

    def test_none_raises_invalid_argument_exception(self):
        obj = None
        self.assertRaises(InvalidArgumentException, lambda: Hashable( obj ) )

    def test_object_not_hashable_exception(self):
        obj = object   # the base python object class is not serializable
        self.assertRaises(ObjectNotHashableException, lambda: Hashable( obj ) )

    def test_invalid_crypto_exception(self):
        obj = 'strings are hashable'
        crypto = 'mycryptoxxx'
        self.assertRaises(InvalidCryptoException, lambda: Hashable( obj, crypto=crypto ) )

    def test_compare_to_known_value(self):
        dct = {'caleb':'bob'}
        h = Hashable( dct )
        should_be_this_for_sha256 = '1ec96f13a69526d681aa92494d62d1d6f478e514e5202b8701526e0241ae73c6'
        self.assertEquals( h.hsh(), should_be_this_for_sha256 )

class TestSimpleTimer(TestCase):
    """
    tests for the SimpleTimer class
    """

    def test_start_and_stop(self):
        t = SimpleTimer()
        t.start()
        t.stop()

class StatsCache(TestCase):
    """
    general tests for the StatsCache class
    """

    def test_instantiate(self):
        stats = StatsCache()