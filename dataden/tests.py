#
# dataden/tests.py

from django.test import TestCase
import random
from django.utils.crypto import get_random_string
import mysite.exceptions
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
    LinkableObject,
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
        #
        # WARNING: entirely clearing the cache will break other tests!
        #self.live_stats_cache = LiveStatsCache(clear=True) # totally wipe out the cache

        #
        # use a very short timeout so that the next time we run tests
        # redis is clean from things added from this test
        self.cache_timeout      = 30
        self.cache_timeout_mod  = 1  # 1 % variability
        self.live_stats_cache   = LiveStatsCache(to=self.cache_timeout, to_mod=self.cache_timeout_mod)

    def test_update_pbp_object(self):
        #pbp_dataden_obj_id          = 'LiveStatsCache_abcdefghijklmnopqrstuvwxz'
        pbp_dataden_obj_id  = get_random_string(32)
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

    def __next_test_linkable_obj(self):
        """
        wrap the test objs with a LinkableObject for use
        with the LinkedExpiringObjectQueueTable
        """
        return LinkableObject( self.__next_test_obj(), field=self.object_common_id_field )

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

        self.assertEquals( set(self.queue_names), set(qt.get_queue_names()) )

        # empty queues should return None when get() is called on them.
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
        # and now both queues should return None again...
        for i in range(len(self.queue_names)):
            self.assertIsNone( qt.get( self.queue_names[i] ) )
            self.assertIsNone( qt.get( self.queue_names[i] ) )

    def test_linkable_object(self):
        """
        make sure LinkedObject extracts the right id
        """
        id = 'abc'
        linkable_object = LinkableObject({'id':id})
        self.assertEquals( linkable_object.get_linking_id(), id )

        custom_id_field = 'custom_id'
        id2             = 'the_custom_id'
        linkable_object2 = LinkableObject({custom_id_field:id2}, field=custom_id_field)
        self.assertEquals( linkable_object2.get_linking_id(), id2 )

    def test_linked_expiring_object_queue_table(self):
        """
        test the LinkedExpiringObjectQueueTable implementation
        """

        # test instance exceptions when creating a new queue
        self.assertRaises( LinkedExpiringObjectQueueTable.QueueNamesNotSetException,
                           lambda: LinkedExpiringObjectQueueTable(names=[]) )
        self.assertRaises( LinkedExpiringObjectQueueTable.UniqueQueueNameConstraintException,
                           lambda: LinkedExpiringObjectQueueTable(names=['dupe','dupe']) )

        class InvalidObject(object):
            def __init__(self):
                pass

        # created with a list of names (a unique name per queue)
        test_qt = LinkedExpiringObjectQueueTable(self.queue_names)

        # test exceptions
        self.assertRaises( LinkedExpiringObjectQueueTable.QueueNotFoundException,
                            lambda: test_qt.add( 'invalid queue', LinkableObject({'id':'test'}) ) )
        self.assertRaises( LinkedExpiringObjectQueueTable.IllegalMethodException,
                            lambda: test_qt.put() )
        self.assertRaises( mysite.exceptions.IncorrectVariableTypeException,
                            lambda: test_qt.add( self.queue_names[0], InvalidObject() ) )

        #
        qt = LinkedExpiringObjectQueueTable(self.queue_names)

        # add the same object to each queue to see if it would link and send !
        linkable_object = self.__next_test_linkable_obj()
        for i in range(len(self.queue_names)):
            qt.add( self.queue_names[i], linkable_object )

        # qt.add( self.queue_names[0], self.__next_test_linkable_obj() )

        # # intiially, all the queues should be empty
        # for i in range(len(self.queue_names)):
        #     self.assertIsNone( qt.get( self.queue_names[i] ) )
        #     self.assertIsNone( qt.get( self.queue_names[i] ) )