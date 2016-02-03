#
# dataden/tests.py

from django.test import TestCase
import random
from testfixtures import Replacer,test_datetime
from test.classes import AbstractTest
from dataden.util.hsh import (
    Hashable,
    InvalidArgumentException,
    ObjectNotHashableException,
    InvalidCryptoException,
)
from dataden.watcher import OpLogObjWrapper
from dataden.util.simpletimer import SimpleTimer
from dataden.cache.caches import (
    LiveStatsCache,
    RandomId,
    QueueTable,
    NonBlockingQueue,
    LinkedExpiringObjectQueueTable,
)

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

class TestStatsCache(TestCase):
    """
    general tests for the StatsCache class
    """

    def test_instantiate(self):
        stats = LiveStatsCache()

class TestLiveStatsCache(TestCase):

    def setUp(self):
        self.live_stats_cache = LiveStatsCache(clear=True) # totally wipe out the cache

    def test_update_pbp_object(self):
        pbp_dataden_obj_id          = 'thisisarandomlygenerateduniquevalue'
        spoofed_dataden_pbp_object  = {'_id':pbp_dataden_obj_id, 'parent_api__id':'any_parent_api'}
        oplog_obj = OpLogObjWrapper('any_db','any_coll', spoofed_dataden_pbp_object)

        # the first time we call update_pbp() it shoudl return true,
        # indicating we just added it
        self.assertTrue( self.live_stats_cache.update_pbp( oplog_obj ) )
        # the following time we call update_pbp() with the same object,
        # it should return false, indicating it already exists in the cache
        self.assertFalse( self.live_stats_cache.update_pbp( oplog_obj ) )

class TestLinkedExpiringObjectQueueTable(TestCase):

    def setUp(self):
        #
        #
        self.queue_names                = ['playbyplay123','stats123']
        self.object_id_field            = '_id'
        self.object_common_id_field     = 'common_id'
        self.common_ids                 = ['a', 'b', 'c']
        self.obj_idx                    = 0

    def __get_random_common_id(self):
        return self.common_ids[ random.randint(0, len(self.common_ids) - 1)]

    def __next_obj_id(self):
        self.obj_idx += 1
        return str(self.obj_idx)

    def __next_test_obj(self):
        """
        using an incrementing unique object id mapped to '_id'
        and a random common linking id from self.common_ids,
        get the next test object to add

        :return:
        """
        obj = {
            self.object_id_field        : self.__next_obj_id(),
            self.object_common_id_field : self.__get_random_common_id(),

            # different every run, easier to discern differences when obj debug printed
            'data'                      : RandomId().get_random_id(),
        }
        return obj

    def test_non_blocking_queue(self):
        """
        test the fundamental NonBlockingQueue
        """
        size = 3
        q = NonBlockingQueue( size )
        self.assertIsNone( q.get() )
        q.put( 'one' )
        self.assertIsNotNone( q.get() )     # getting the only item returns non-None
        self.assertIsNone( q.get() )        # it should be empty again, and return None

        # fill it up with duplicates so we can add 1 different thing after,
        # and make sure it ejects an existing thing
        duplicate_obj = 'duplicate'
        different_obj = 'different'
        for x in range(size):
            ejected_obj = q.put( duplicate_obj )
            self.assertIsNone( ejected_obj )
        # add a different object, which should eject the most recently added obj
        for x in range(size):
            # the return of the put() should match 'duplicate_obj' because it gets ejected
            self.assertEquals( q.put( different_obj ), duplicate_obj )
        # now we should be left with a queue full of the 'different_obj'
        for x in range(size):
            self.assertEquals( q.get(), different_obj )
        # and now there should be nothing in queue, so get() should return None
        self.assertIsNone( q.get() )

    def test_queue_table(self):
        """
        test the QueueTable object for basic functionality
        """
        qt = QueueTable(self.queue_names)

        # ensure all queues empty, and return None
        for i in range(len(self.queue_names)):
            self.assertIsNone( qt.get( self.queue_names[i] ) )
            self.assertIsNone( qt.get( self.queue_names[i] ) )
        # add something to each named queue
        for i in range(len(self.queue_names)):
            qt.add( self.queue_names[i], self.__next_test_obj() )
            qt.add( self.queue_names[i], self.__next_test_obj() )
        # simply make sure each queue returns something thats not None
        for i in range(len(self.queue_names)):
            self.assertIsNotNone( qt.get( self.queue_names[i] ) )
            self.assertIsNotNone( qt.get( self.queue_names[i] ) )

    def test_linked_expiring_object_queue_table(self):
        """
        TODO - what is this test for?
        """
        pass # TODO
        #linked_queue = LinkedExpiringObjectQueueTable(self.queue_names)
