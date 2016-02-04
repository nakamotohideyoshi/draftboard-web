#
# dataden/cache/caches.py

from django.core.cache import caches
from django.utils import timezone
from queue import Queue, Full, Empty
from mysite.exceptions import IncorrectVariableTypeException
from keyprefix.classes import UsesCacheKeyPrefix
from dataden.util.hsh import Hashable
from random import Random
from dataden.models import (
    LiveStatsCacheConfig,
    Trigger,
)
import random

# >>> cache1 = caches['myalias']
# >>> cache  = caches['default'] # ie: settings.CACHES = { 'default' : THIS }

#
# cache methods
# set( key, val, duration )                  # always adds
# add( key, val, duration )                  # only adds if doesnt exist
# get( key, default )                   # get, if not exists, return default
# set_many({'a': 1, 'b': 2, 'c': 3})    # more efficient for multiple key:value pairs
# get_many(['a', 'b', 'c'])             # more efficient get() for multiple key:value pairs
# delete( key )                         # remove key from cache
# delete_many( ['a','b'] )              # more efficient delete() for multiple key:value pairs
# clear()                               # blow away entire cache - apocalypse
# cache.close()                         # close our conenction to the cache

#
# The default is a wrapper around redis, but if you
# were using straight redis, here are a couple methods to know about:
#  r = redis.Redis()
#  set( key, value )            # default ttl
#  set( key, value, ttl )       # specify the ttl

class LiveStatsCache( UsesCacheKeyPrefix ):
    """
    LiveStatsCache is responsible for handling a large volume of stat updates,
    the primary of which are coming from triggers.

    This cache modifies the timeout for each item that is added to the cache
    by adding +/- 25% of the timeout. Due to the nature of how the stats
    will be parsed, it will spread out db model save()'s.
    This timeout modifier can be adjusted with the 'timeout_modifier' variable.
    """

    sent_pbp_table_key = 'SentPbp_LiveStatsCache_table'

    class Config(object):

        def __init__(self):
            try:
                self.conf = LiveStatsCacheConfig.objects.get( pk=1 )
            except LiveStatsCacheConfig.DoesNotExist:
                self.conf = LiveStatsCacheConfig()

                # the expiration (seconds) for objects added to the cache, before any modifiers.
                self.conf.key_timeout = 30 * 60

                # randomly vary the cache expiration of added objects by this percentage.
                self.conf.timeout_mod = 25      # for example: 33 indicates 33%

                self.conf.save()

        def get_key_timeout(self):
            return self.conf.key_timeout

        def set_key_timeout(self, seconds):
            self.conf.key_timeout = seconds
            self.conf.save()

        def get_timeout_mod(self):
            return self.conf.timeout_mod

        def set_timeout_mod(self, percent_as_int):
            self.conf.timeout_mod = percent_as_int
            self.conf.save()

    def __init__(self, name='default', key_version=1, to=1800,
                        to_mod=25, clear=False, use_admin_conf=True):
        """
        'to' is the timeout when setting an object in the cache
        'to_mod' is an integer value from 0 to anything that specifies the percentage
         to adjust the timeout. ex: to_mod=25 indicates we should randomize the
         timeout by 25%. negative values will be absolute valued.

         this class will attempt to use the config in the database by default,
         you can force you own values to be used if you use: use_admin_conf=False

        :param name:
        :param key_version:
        :param to:
        :param to_mod:
        :param clear:
        :param use_admin_conf:
        :return:
        """
        super().__init__()

        self.c = caches[ name ]             # 'default' is the settings.CACHES['default'] !
        if clear == True:
            self.c.clear() # REMOVE THE WORLD from the cache. everything. is. gone.

        self.key_version    = key_version

        if use_admin_conf:
            self.config = self.Config()
            self.to             = self.config.get_key_timeout()
            self.to_mod         = self.config.get_timeout_mod()
        else:
            self.to             = abs(to)       # seconds until expires from cache
            self.to_mod         = abs(to_mod)   # +/- percentage to randomly adjust timeout

        self.r = Random()

    def __validate_livestat(self, livestat):
        """
        validates livestat parameter

        :param livestat:
        :raises IncorrectVariableTypeException: when 'livestat' param is not the expected type
        :return:
        """
        if not issubclass(type(livestat), Hashable):
            raise IncorrectVariableTypeException(type(self).__name__, 'livestat' )

    def update(self, livestat):
        """
        returns True if the item was added to the cache, otherwise returns false.
        returns False if the item was ALREADY in the cache.

        The argument should be an instance of Hashable.
        Check if it exists in the cache, then decide
        whether or not to save it to the database.

        throws IncorrectVariableTypeException if livestat is not a dataden.util.hsh.Hashable

        :param livestat:
        :return:
        """

        self.__validate_livestat(livestat)

        #
        # the return value, a boolean, is True if it was added, otherwise False
        was_added = self.c.add( self.get_key(livestat.hsh()), livestat.get_id(),
                              self.get_to(), version=self.key_version )
        return was_added

    def update_pbp(self, livestat):
        """
        return a boolean indicating whether a livestat object with an
        '_id' field matching livestat.get_id() was just added.
        """

        self.__validate_livestat( livestat )

        sent_pbp = self.c.get( self.sent_pbp_table_key, {} )
        if sent_pbp.get(livestat.get_id(), None) is not None:
            # it exists
            was_added = False
        else:
            # it did not exist !
            sent_pbp[livestat.get_id()] = 'x' # set to anything
            was_added = True
            # add the dict back into the cache
            self.c.add( self.sent_pbp_table_key, sent_pbp, self.to, version=self.key_version )

        return was_added    # if was_added is True, that means we just added it

    def get_to(self):
        # int( float(797) * ( float(r.randint( -1 * 13, 13 )) / 100.0 ) )
        rand = self.r.randint( -1 * self.to_mod, self.to_mod )
        modifier = int( float(self.to) * (float(rand) / 100.0) )
        return self.to + modifier

class TriggerCache( UsesCacheKeyPrefix ):
    """
    loads enabled triggers from redis

    Store all of the site DataDen Triggers in cache, because without
    this cache there could be a polling effect on the actual db and we dont want that.
    """

    KEY = "enabled_triggers"
    TIMEOUT = 1 # 100 # seconds - turned down to 1 second for debugging

    def __init__(self, name='default', clear=False, key_version=1):
        """
        get the cache from django.core.caches with the 'name', by default its 'default'

        if clear=True, wipes out any existing cached triggers

        :param name:
        :param clear:
        :param key_version:
        :return:
        """
        super().__init__()
        self.c = caches[ name ]     # 'default' is the settings.CACHES['default'] !
        if clear == True:
            self.clear()
        self.key_version    = key_version
        self.triggers       = self.get_triggers()

        print('TriggerCache...')
        for t in self.triggers:
            print( '  ', t )

    def __key(self):
        """
        helper/wrapper function for getting the key
        :return:
        """
        return self.get_key(self.KEY)

    def clear(self):
        self.c.delete( self.__key() ) # removes the item at the key
        self.triggers = []

    def add_triggers(self, triggers):
        was_added = self.c.add( self.__key(), self.triggers,
                                self.TIMEOUT, version=self.key_version )
        return was_added

    def get_triggers(self):
        """
        tries to get the enabled triggers from the cache. If it cant find them there
        it defaults to getting them from the regular database.

        :return:
        """
        self.triggers = self.c.get( self.__key(), None )
        if not self.triggers:
            #
            # retrieve them from the regular database
            self.triggers = Trigger.objects.filter( enabled=True )
            self.add_triggers( triggers=self.triggers )

        return self.triggers

class PlayByPlayCache( UsesCacheKeyPrefix ):
    """
    For the trailing history of pbp objects available.

    Stores a short, trailing history, of a particular sports play by play objects,
    so the front end can get a list of these objects to display. Does not contain
    all of the pbp objects for entire games or days by design -- this is meant only
    to keep track of a small window in time behind the actual time.
    """

    KEY         = "PlayByPlayCache_"
    TIMEOUT     = 60*60*48                 #  before this cache data expires. (add() refreshes countdown)
    MAX         = 100

    def __init__(self, sport, name='default', clear=False, key_version=1, max=0):
        """
        get the cache from django.core.caches with the 'name', by default its 'default'

        if clear=True, wipes out any existing cached triggers

        :param name:
        :param clear:
        :param key_version:
        :return:
        """
        super().__init__()

        self.sport  = sport

        self.c = caches[ name ]     # 'default' is the settings.CACHES['default'] !

        if clear == True:
            self.clear()

        self.key_version    = key_version

        self.max = self.MAX # default value
        if max > 0:
            self.max = max

    def __key(self):
        """
        return the key for which we can retrieve the pbp objects

        :return:
        """
        return self.get_key(self.KEY) + self.sport

    def clear(self):
        self.c.delete( self.__key() ) # removes the item at the key

    def add(self, pbp):
        """
        add a pbp object to the capped list of pbp objects for this sport

        :param pbp:
        :return:
        """
        current = self.get_pbps()
        new = [ pbp ] + current[0:self.max - 1]     # get the first MAX pbp objects, and push on the new one
        self.c.set( self.__key(), new, self.TIMEOUT, version=self.key_version )

    def get_pbps(self):
        """
        tries to get the play by play objects from the cache.

        returns an empty list if there are no objects in the cache

        :return:
        """
        return self.c.get( self.__key(), [] )

class NonBlockingQueue( Queue ):
    """
    queue that discards the oldest items.
    instead of blocking on put() if its Full, put simply returns
    the oldest item in the queue, and adds the obj
    """

    def __init__(self, size=10):
        super().__init__(size)

    def put(self, obj):
        """
        Put an obj into the queue.
        Discards the oldest item if the queue is full.

        :param obj:
        :return:
        """
        ejected_obj = None
        try:
            super().put(obj, False)
        except Full:
            ejected_obj = super().get( False )
            super().put(obj, False )

        # return the item that is being ejected -- otherwise return None
        return ejected_obj

    def get(self):
        """

        :return: tuple of (<datetime object>, <obj>). if nothing in the queue, returns None
        """
        try:
            return super().get(False)
        except Empty:
            return None

class CommonId(object):

    def __init__(self, common_id, obj):
        self.common_id = common_id
        self.obj = obj

    def get_common_id(self):
        return self.common_id

    def get_obj(self):
        return self.obj

class RandomId(object):

    def get_random_id(self):
        """
        returns random values using random.getrandbits(128)
        kind of like in this code example:

        >>> hash = random.getrandbits(128)
        >>> '%032x' % hash
        >>> 'ddc16ae5ad655f088d71fd30fe03497f'
        """
        return '%032x' % random.getrandbits(128)

class RandomIdMixin(RandomId):
    """ classes wanting use of the method get_random_id() """
    pass

# class AbstractLinkableObject(object):
#
#     def __init__(self, obj):
#         self.obj = obj
#
#     def get_linking_id(self):
#         raise Exception('AbstractLinkableObject.get_linking_id() must be overridden!')
#
# class PbpLinkableObject(AbstractLinkableObject):
#
#     def get_linking_id(self):
#         return self.obj.get('id')
#
# class StatsLinkableObject(AbstractLinkableObject):
#
#     def get_linking_id(self):
#         return self.obj.get('id')

class QueueTable(RandomIdMixin):
    """
    an object that has 0 or more named queues, named by strings
    """

    class QueueNotFoundException(Exception): pass

    class QueueNamesNotSetException(Exception): pass

    class UniqueQueueNameConstraintException(Exception): pass

    class IllegalMethodException(Exception): pass

    queue_size = 10

    def __init__(self, names=[]):
        """
        initialize a QueueTable with an internal queue for every string in 'names' param

        :param names: list of string names of queues
        """
        if names == []:
            err_msg = 'the argument "names" must be a non-empty list of unique names"'
            raise self.QueueNamesNotSetException(err_msg)

        #
        # set( list ) returns the set of unique names, so if everything in 'names'
        # is unique the size of the set should match size of the names list!
        if len(set(names)) != len(names):
            err_msg = 'names does not contain unique values: %s' % str(names)
            raise self.UniqueQueueNameConstraintException(err_msg)

        #
        # build the internal queues
        self.queues = {}
        for name in names:
            self.queues[name] = NonBlockingQueue(self.queue_size)

    def put(self):
        """
        :raises IllegalMethodException: you should be using add(name, obj) instead!
        """
        raise self.IllegalMethodException('do not use put(). use add(name, obj) instead!')

    def get_queue(self, name):
        """
        get a queue by name

        :param name:
        :return:
        """
        if name in self.queues.keys():
            return self.queues[ name ]
        # else raise exception with the name of the queue
        raise self.QueueNotFoundException(name)

    def get(self, name):
        """
        get the first thing in the named queue
        """
        return self.get_queue(name).get()

    def get_obj(self, queue_name, obj):
        """
        TODO - what does this do?

        i think it grabs a specific obj from the named queue, removes it, and returns it...

        perhaps remove() should do that !
        """
        raise Exception('unimplemented')

    def remove(self, name, obj):
        """
        remove the object from the queue equal to 'obj' parameter
        """
        q = self.get_queue(name)
        q.queue.remove( obj )
        # TODO - perhaps going to need to loop to find the obj with identifier...

    def add(self, name, obj, identifier=None):
        """
        adds the object to the named queue as a tuple of the form:
            (<identifier>, timezone.now(), obj)

        if the indentifier is not None, it is used instead of a random one.
        """

        if identifier:
            uid = identifier
        else:
            uid = RandomId().get_random_id()
        now = timezone.now()
        q   = self.get_queue(name)
        tup = (uid, now, obj)
        q.put( tup )

class LinkedExpiringObjectQueueTable(QueueTable):
    """
    an object with access to multiple named queues.

    objects placed into any of the queues will be able
    to be retrieved from the queue until they expire.

    the identifier can be used to retrieve objects
    from cache, but if they have expired will return None.
    """

    default_timeout         = 5
    default_django_cache    = 'default'

    def __init__(self, names, timeout=None, cache=None):
        """
        create a new instance of LinkedExpiringObjectQueueTable

        :param names: list of string names of the queues to create
        :param timeout: integer seconds of countdown until queued objects expire from cache
        :param cache: if None, uses caches["default"] django cache. if None, uses
        """
        super().__init__(names)

        if timeout is None:
            self.timeout = self.default_timeout
        else:
            self.timeout = timeout

        if cache is None:
            self.cache = caches[self.default_django_cache]
        else:
            self.cache = cache

    def add(self, name, obj):
        """
        create a random id and puts it in the global cache with the timeout

        super().add( name, obj ) is called after we add the identifier to the cache,
        but _before_ we fire the countdown task that will try to do the future linking.

        :param name:
        :param obj:
        :return:
        """

        #
        # cache the identifier as both the key and the value as a
        # way of flagging this object as being in its countdown!
        # the identifier is automatically removed the cache when it expires.
        identifier = self.get_random_id()
        self.cache.add( identifier, identifier, self.timeout )

        #
        # TODO - for the item we are about to add, we should check
        # TODO   if there is already a linkable object in the queue!
        linked_object = self.remove( )

        #
        # call super().add() to add it to the queue, using our own identifier
        super().add( name, obj, identifier=identifier )

        # fire the task to do the linking in the near future, allowing some time
        # for a linkable stat to come in the queue


    def get_linked_object(self, original_queue, identifier):
        """
        TODO - what does this do?
        """
        pass # TODO

    # TODO      everytime something is added to the LinkedExpiringObjectQueueTable
    # TODO      fire a task with countdownSeconds to try to link objects!
