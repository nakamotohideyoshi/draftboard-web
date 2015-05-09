#
# dataden/watcher.py

from mysite.settings import local

from dataden.util.hsh import Hashable
from dataden.util.simpletimer import SimpleTimer
from dataden.cache.caches import LiveStatsCache

from pymongo import MongoClient
from pymongo.cursor import _QUERY_OPTIONS, CursorType
import re, time
from dataden.signals import Update

class UnimplementedTriggerCallbackException(Exception):
    def __init__(self, class_name, variable_name):
        super().__init__( "The trigger() callback is unimplemented.")

class ParentApis(object):

    def __init__(self, mongo_client=None):
        self.client = mongo_client
        if not self.client:
            self.client = local.get_mongo_client() # cheese

    def all(self):
        pass # TODO

class OpLogObj( Hashable ):

    exclude_field_names = ['dd_updated__id']

    def __init__(self, obj):
        self.ts     = obj.get('ts')
        self.ns     = obj.get('ns')
        self.o      = obj.get('o')

        #
        # certain fields we want to remove because
        # they arent relevant, or serializable and
        # will break the hash mechanism
        for field_name in self.exclude_field_names:
            self.o.pop(field_name, None)

        super().__init__( self.o )

    def get_o(self):
        """
        retrieve the dataden object - extracting it from its oplog wrapper
        """
        return self.o

    def get_id(self):
        return self.o.get('_id')  ######### IF EVERYTHING BREAK ITS BEAUSE THIS WAS LACKING THE 'return'

    def get_ts(self):
        return self.ts

class Trigger(object):
    """
    uses local.oplog.rs to implement mongo triggers
    """

    DB_LOCAL    = 'local'
    OPLOG       = 'oplog.rs'

    PARENT_API__ID = 'parent_api__id'

    def __init__(self, db, coll, parent_api=None, cache='default', clear=False, init=False):
        """
        clear=True  does a world wipe of the cache.
        all=True    parses the oplog from the begining, instead of from "now"

        :param db:
        :param coll:
        :param cache:
        :param clear:
        :param all:
        :return:
        """
        self.init         = init            # default: False, if True, parse entire log
        self.client       = MongoClient()   # defaults to localhost:27017
        self.last_ts      = None
        self.db_name      = db              # ie: 'nba', 'nfl'
        self.coll_name    = coll            # ie: 'player', 'standings'
        self.parent_api   = parent_api      # dataden's name for the feed to look in

        self.timer      = SimpleTimer()

        self.db_local   = self.client.get_database( self.DB_LOCAL )
        self.oplog      = self.db_local.get_collection( self.OPLOG )

        self.live_stats_cache = LiveStatsCache( cache, clear=clear )

    def run(self, last_ts=None):
        """
        run the watcher, and start triggering on relevant db_name/coll_name.
        if last_ts is set, start from as far back as (but not guaranteed to be) last_ts.

        :return:
        """
        self.display()

        if last_ts:
            self.last_ts = last_ts # user wants to start from at least this specific ts
        else:
            self.last_ts = self.get_last_ts() # get most recent ts, (by default, dont reparse the world)

        while True:
            self.timer.start()
            cur = self.get_cursor( self.oplog, self.query() )
            #self.timer.stop(msg='get_cursor()')

            count = 0
            added = 0
            for obj in cur:
                self.timer.start()

                hashable_object = OpLogObj(obj)
                self.last_ts = hashable_object.get_ts()

                if self.live_stats_cache.update( hashable_object ):
                    #
                    # send the 'o' object (a stat update) out as a
                    # signal because its been updated!!
                    Update( hashable_object ).send()
                    added += 1

                count += 1
                self.timer.stop(print_now=False, sum=True)

            msg = '(%s of %s) total objects are new in <<< %s >>>' % \
                                (str(added), str(count), self.get_ns())
            self.timer.stop(msg='%s | loop time [avg time per object %s]' % \
                                            (msg, str(self.timer.get_sum())) )
            self.timer.start(clear_sum=True) # and then the next start() will correct

    def get_ns(self):
        return '%s.%s' % (self.db_name, self.coll_name)

    def get_last_ts(self):
        """
        sets the last_ts internally, and then returns the same value.
        must be called before query() is generated

        :return:
        """
        self.timer.start()
        cur = self.oplog.find().sort([('$natural', -1)])
        for obj in cur:
            self.last_ts = OpLogObj( obj ).get_ts()
            self.timer.stop(msg='get_last_ts()')
            return self.last_ts

    def query(self):
        q = {
            'ts' : {'$gt' : self.last_ts},
            'ns' : '%s.%s' % (self.db_name, self.coll_name),

            # specific parent_api__id - will be removed if parent_api__id is None
            'o.%s' % self.PARENT_API__ID : self.parent_api
        }

        if not self.parent_api:
            q.pop('o.%s' % self.PARENT_API__ID, None)

        if self.init == True:  # explicity showing if its == True, because this will be rare
            self.init = False  # toggle it off after the first run though !
            q.pop('ts', None)

        return q

    def get_cursor(self, collection, query, cursor_type=None, hint=[('$natural', 1)]):
        """
        Gets a Cursor for the given collection and target query.
        If cursor_type is None it defaults to CursorType.TAILABLE_AWAIT.
        hint tells Mongo the proper index to use for the query

        :param collection:
        :param query:
        :param cursor_type:
        :param hint:
        :return:
        """
        if cursor_type is None:
            cursor_type = CursorType.TAILABLE_AWAIT

        cur = collection.find(query, cursor_type=cursor_type)
        cur = cur.hint(hint)
        return cur

    def display(self):
        print('%s [ trigger running on <<< %s.%s %s >>' % (self.__class__.__name__,
                                    self.db_name, self.coll_name, 'parent_api: %s' % self.parent_api) )

    def trigger_debug(self, object):
        print( object )

    def trigger(self):
        raise UnimplementedTriggerCallbackException(
            self.__class__.__name__ + 'must implement trigger() method')

class NbaPlayerStats(Trigger):

    #
    # may want to specify the parent api id as well

    DB_NBA      = 'nba'
    COLL_PLAYER = 'player'
    PARENT_API  = 'stats'

    def __init__(self):
        super().__init__(db=self.DB_NBA, coll=self.COLL_PLAYER, parent_api=self.PARENT_API)

class NbaPbpEvent(Trigger):

    #
    # may want to specify the parent api id as well

    DB          = 'nba'
    COLL        = 'event'
    PARENT_API  = 'pbp'

    def __init__(self):
        super().__init__(db=self.DB, coll=self.COLL, parent_api=self.PARENT_API)