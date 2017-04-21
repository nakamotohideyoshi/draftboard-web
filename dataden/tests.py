#
# dataden/tests.py

from django.test import TestCase
from django.utils.crypto import get_random_string

from dataden.cache.caches import (
    LiveStatsCache,
)
from dataden.util.hsh import (
    Hashable,
    InvalidArgumentException,
    ObjectNotHashableException,
    InvalidCryptoException,
)
from dataden.util.simpletimer import SimpleTimer
from dataden.watcher import OpLogObjWrapper


class TestHashable(TestCase):
    """
    tests for the Hashable class
    """

    def test_none_raises_invalid_argument_exception(self):
        obj = None
        self.assertRaises(InvalidArgumentException, lambda: Hashable(obj))

    def test_object_not_hashable_exception(self):
        obj = object  # the base python object class is not serializable
        self.assertRaises(ObjectNotHashableException, lambda: Hashable(obj))

    def test_invalid_crypto_exception(self):
        obj = 'strings are hashable'
        crypto = 'mycryptoxxx'
        self.assertRaises(InvalidCryptoException, lambda: Hashable(obj, crypto=crypto))

    def test_compare_to_known_value(self):
        dct = {'caleb': 'bob'}
        h = Hashable(dct)
        should_be_this_for_sha256 = '1ec96f13a69526d681aa92494d62d1d6f478e514e5202b8701526e0241ae73c6'
        self.assertEquals(h.hsh(), should_be_this_for_sha256)


class TestSimpleTimer(TestCase):
    """
    tests for the SimpleTimer class
    """

    def test_start_and_stop(self):
        t = SimpleTimer()
        t.start()
        t.stop()


class TestStatsCache(TestCase):
    """
    general tests for the StatsCache class
    """

    def test_instantiate(self):
        stats = LiveStatsCache()


class TestLiveStatsCache(TestCase):
    def setUp(self):
        #
        # WARNING: entirely clearing the cache will break other tests!
        # self.live_stats_cache = LiveStatsCache(clear=True) # totally wipe out the cache

        #
        # use a very short timeout so that the next time we run tests
        # redis is clean from things added from this test
        self.cache_timeout = 30
        self.cache_timeout_mod = 1  # 1 % variability
        self.live_stats_cache = LiveStatsCache(to=self.cache_timeout, to_mod=self.cache_timeout_mod)

    def test_update_pbp_object(self):
        # pbp_dataden_obj_id          = 'LiveStatsCache_abcdefghijklmnopqrstuvwxz'
        pbp_dataden_obj_id = get_random_string(32)
        spoofed_dataden_pbp_object = {'_id': pbp_dataden_obj_id, 'parent_api__id': 'any_parent_api'}
        oplog_obj = OpLogObjWrapper('any_db', 'any_coll', spoofed_dataden_pbp_object)

        # the first time we call update_pbp() it should return true,
        # indicating we just added it
        self.assertTrue(self.live_stats_cache.update_pbp(oplog_obj))
        # the following time we call update_pbp() with the same object,
        # it should return false, indicating it already exists in the cache
        self.assertFalse(self.live_stats_cache.update_pbp(oplog_obj))
