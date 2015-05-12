#
# dataden/cache/caches.py

from django.core.cache import caches

from mysite.exceptions import IncorrectVariableTypeException

from keyprefix.classes import UsesCacheKeyPrefix
from dataden.util.hsh import Hashable

from random import Random

from dataden.models import LiveStatsCacheConfig, Trigger

# >>> cache1 = caches['myalias']
# >>> cache  = caches['default'] # ie: settings.CACHES = { 'default' : THIS }

#
# cache methods
# set( key, duration )                  # always adds
# add( key, duration )                  # only adds if doesnt exist
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

    class Config(object):

        def __init__(self):
            try:
                self.conf = LiveStatsCacheConfig.objects.get( pk=1 )
            except LiveStatsCacheConfig.DoesNotExist:
                self.conf = LiveStatsCacheConfig()
                self.conf.key_timeout = 1800
                self.conf.timeout_mod = 25
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

    def update_many(self, livestats):
        pass # TODO ?

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

        if not issubclass(type(livestat), Hashable):
            raise IncorrectVariableTypeException(type(self).__name__, 'livestat' )

        #
        # the return value, a boolean, is True if it was added, otherwise False
        was_added = self.c.add( self.get_key(livestat.hsh()), livestat.get_id(),
                              self.get_to(), version=self.key_version )
        return was_added

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
    TIMEOUT = 100 # seconds

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






