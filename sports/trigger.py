from logging import getLogger
from django.core.cache import cache
from dataden.cache.caches import LiveStatsCache
from dataden.watcher import (
    OpLogObj,
    Trigger,
)
import sports.parser

logger = getLogger('sports.trigger')


class SportTrigger(Trigger):
    def __init__(self, sport, *args, **kwargs):
        self.sport = sport

        # update the triggers! basically we always forget to manually add
        # new triggers if we change sport specific code that needs new ones.
        # the next few lines uses sports.parser.DataDenParser.setup_triggers()
        # update the current triggers in the database automatically.
        # TODO ... circular imports are awesome
        parser = sports.parser.DataDenParser()
        parser.setup_triggers(self.sport)

        # call super method
        super().__init__(*args, **kwargs)

        # internal debug field to help us print out the triggers the first time only
        self.showed_triggers = False

    def reload_triggers(self):
        """
        override parent method, so we can set only the triggers for this sport
        """

        # sets self.triggers with ALL triggers.
        super().reload_triggers()

        # get only specific triggers models for this sport
        self.triggers = self.triggers.filter(db=self.sport)

        if self.showed_triggers == False:
            self.showed_triggers = True

            # print them to the screen so we know exactly which are about to be used
            for t in self.triggers:
                logger.info('  Reloaded trigger: %s' % t)


class MlbOpLogObj(OpLogObj):
    object_namespace = 'mlb.at_bat'

    def override_new(self):
        """
        always pretend its the first time we've seen an object
        from this namespace (ie: 'ns') if it doesnt yet
        have a description value (we need it to pass the trigger filter for pbp stuff)
        """
        if self.get_ns() == self.object_namespace and self.get_o().get('description') is None:
            my_ns = self.get_ns()
            logger.debug('(override!) my_ns: %s' % my_ns)
            return True
        return False


class TriggerMlb(SportTrigger):
    """
    nearly identical to the default Trigger, but sets
    a special OpLogObj subclass that will allow for
    at_bat objects to always be sent out if their
    description field is not yet set for pbp purposes.
    """

    oplogobj_class = MlbOpLogObj


class CacheList(object):
    """
    a list implementation. the list is stored in cache using a combination
    of the unique_name __init__() param as well as the key in the add() method
    """

    class UniqueNameException(Exception):
        pass

    # unique_name cannot include this because its used
    # to index into the cache used by CacheList
    key_separator = ':'

    # default timeout (seconds)
    default_timeout = 300

    def __init__(self, cache, unique_name=None, timeout=None):
        """
        create this list in the specified cache, with the timeout (seconds)

        :param cache: any cache implementation, ie: django.core.cache.cache
        :param unique_name: a string, unique prefix to the key that indexes to the list
        :param timeout: the cache expiration, in seconds
        :return:
        """

        #
        self.cache = cache

        #
        self.unique_name = unique_name
        if unique_name is None:
            self.unique_name = self.__class__.__name__
        elif self.key_separator in unique_name:
            err_msg = 'unique_name cannot include character "%s"' % self.key_separator
            raise self.UniqueNameException(err_msg)

        #
        self.timeout = timeout
        if self.timeout is None:
            self.timeout = self.default_timeout

    def add(self, key, val):
        """
        key is the lookup to a list(). add val to it.

        :param key: string (or we will use str() to cast it to a string)
        :param val: any object the cache will let us add
        :return:
        """
        l = self.get(key)
        l.append(val)
        # set it in the cache, with the specified timeout
        k = self.__get_key(key)
        # print('k[%s] cache[%s] set timeout[%s] zonepitch [%s]' % (k, str(self.cache), str(self.timeout), str(val)))
        self.cache.set(k, l, self.timeout)

    def __get_key(self, key):
        return '%s%s%s' % (self.unique_name, self.key_separator, str(key))

    def get(self, key):
        """
        returns a list of the vals added (unless it has expired),
        in which case it returns an empty list

        :param key: the key of the list to retrieve
        :return:
        """
        return self.cache.get(self.__get_key(key), [])


class DjangoCacheList(CacheList):
    """
    for testing, uses the default django cache
    """

    def __init__(self):
        super().__init__(cache)


class MlbCache(LiveStatsCache):
    """
    extend the default trigger's LiveStatsCache to provide
    mlb the mechanism for saving the lists of ZonePitch objects
    along with the ability to retrieve them using an at-bat srid.
    """

    def update(self, oplog_obj):
        """
        override update() method to add this livestat to the
        list of zonepitches if it is actually a zonepitch
        """

        # we must call super, and we must return
        # its return value at end of this method!
        was_added = super().update(oplog_obj)

        #
        # logic for zonepitches moved into the ZonePitch parser class!
        # # if the object was _just_ added, then we should also
        # # add it to our list of zonepitches for the atbat (in the cache).
        # if was_added == True:
        #     ns = oplog_obj.get_ns()
        #     parent_api = oplog_obj.get_parent_api()
        #     if ns == 'mlb.pitcher' and parent_api == 'pbp':
        #         #
        #         # its a zone pitch, add it to its cached list
        #         # using the MlbTrigger's cache (self.c)
        #         zonepitch = oplog_obj.get_o()
        #         zpid = zonepitch.pop('_id') # remove it. its a lot of unnecessary characters
        #         at_bat_id = zonepitch.get('at_bat__id')
        #         #print('adding to cache_list, at_bat_id:', str(at_bat_id))
        #         cache_list = CacheList(self.c)
        #         cache_list.add(at_bat_id, zonepitch)
        #         #print('cache_list is now:', str(cache_list.get(at_bat_id)))

        return was_added


class MlbTrigger(SportTrigger):
    live_stats_cache_class = MlbCache

    def __init__(self):
        super().__init__('mlb')
