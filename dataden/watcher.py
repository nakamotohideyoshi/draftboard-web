#
# dataden/watcher.py

#
# this setting can have a huge impact on the speed of stat updates
# because it will us celery tasks to do all the updates, but
# that can have the affect of hammering the disk - it works, but
# has not been battle tested on heroku yet. currently it will
# bring a vagrant VM to its knees.

from django.conf import settings
ASYNC_UPDATES = settings.DATADEN_ASYNC_UPDATES # False for dev

from dataden.util.hsh import Hashable
from dataden.util.simpletimer import SimpleTimer
from dataden.cache.caches import LiveStatsCache, TriggerCache

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
            #self.client = local.get_mongo_client() # cheese
            self.client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)

    def all(self):
        pass # TODO

class OpLogObj( Hashable ):

    exclude_field_names = ['dd_updated__id']

    def __init__(self, obj):
        self.original_obj           = obj # save the original object
        self.ts                     = obj.get('ts')
        self.ns                     = obj.get('ns')
        self.o                      = obj.get('o')

        #
        # certain fields we want to remove because
        # they arent relevant, or serializable and
        # will break the hash mechanism
        tmp = {}
        for field_name in self.exclude_field_names:
            val = self.o.pop(field_name, None)
            if val:
                tmp[ field_name ] = val

        #
        # the constructor for Hashable hashes the object once
        # so after this call, we can put the exclude fields back in
        super().__init__( self.o )

        for k,v in tmp.items():
            self.o[ k ] = v

    def __str__(self):
        return str(self.original_obj)

    def get_ns(self):
        """
        return the namespace. its a string like this: 'nba.player', ie: 'DB.COLLECTION'
        """
        return self.ns

    def get_o(self):
        """
        retrieve the dataden object - extracting it from its oplog wrapper
        """
        return self.o

    def get_parent_api(self):
        """
        try to get the 'parent_api__id' value from the 'o'
        """
        return self.o.get('parent_api__id', None)

    def get_id(self):
        """
        get the dataden mongo _id base64 encoded hash of the keys
        """
        return self.o.get('_id', None)

    def get_ts(self):
        """
        get the 'ts' property of the oplog object
        """
        return self.ts

class OpLogObjWrapper( OpLogObj ):
    """
    Use this class to construct "fake" oplog objects for the primary purpose
    of being able to send any object we want as a signal using Update().send().

    ie: if you used some class to get a cursor of mongo objects from
    a specific db & collection, you can send that object as a signal
    if you create an instance of this class with the mongo obj and
    send it with the Update() signal !

    usage: >>> Update( OpLogObjWrapper( obj_not_from_oplog ) ).send()

    Details of whats really happening: mongo objects that come from the oplog.rs
    collection can be sent via Update(obj).send() because they are essentially
    just regular mongo objects stuff in the 'o' field of a dictionary like this:
        oplogobj = {
            "ts" : Timestamp(1431580464, 163),
            "h" : NumberLong("-9089075734746773552"),
            "v" : 2,
            "op" : "u",
            "ns" : "nba.player",
            "o2" : {
                "_id" : "cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZGU4NGExNDI1LTY2NmEtNDEzZS04NDA4LThhZTBlZTZmNjMwM3F1YXJ0ZXJfX2lkN2Q0OTMzMWUtODIzMS00ZjMxLTllZWYtYjBiMjUxMWY5MmZmcGFyZW50X2xpc3RfX2lkZmllbGRnb2FsX19saXN0ZXZlbnRfX2lkN2M0NzBmNDQtM2JiMS00MTYzLWI0ZTEtZmUzOWQ3ZjYzOTkwaWQyNjczNDg1MS1kY2U2LTRlNWItODI5MS01OTRhN2ViZDY2NTg="
            },
            "o" : regular_mongo_obj (ie: {})
        }
    This class just wraps the object given to it with a fake oplog wrapper,
    putting theh fake mongo obj into the 'o' field!
    """
    OPLOG_WRAPPER = {
        "ts" : 0,   # currently, we dont care about this field
        "h" : 0,    # currently, we dont care about this field
        "v" : 2,    # currently, we dont care about this field
        "op" : "u", # currently, we dont care about this field

        "ns" : None, # ie: "nba.player",
        "o2" : {
            "_id" : None # mongo obj's "_id" field
        },
        "o" : None, #regular_mongo_obj (ie: {})
    }

    def __init__(self, db, coll, mongo_obj):
        #
        # copy OPLOG_WRAPPER, and create our new wrapped obj with the important fields
        wrapped_obj = {}
        for key, val in self.OPLOG_WRAPPER.items():
            if key == 'ns':
                new_val = '%s.%s' % (db,coll)   # create the 'ns' string!
            elif key == 'o':
                new_val = mongo_obj   # !
            else:
                # set with whatever is in OPLOG_WRAPPER
                new_val = val
            wrapped_obj[ key ] = new_val

        #
        # now create the OpLogObj with our spoofed obj
        super().__init__(wrapped_obj)

class Trigger(object):
    """
    uses local.oplog.rs to implement mongo triggers
    """

    DB_LOCAL    = 'local'
    OPLOG       = 'oplog.rs'

    PARENT_API__ID = 'parent_api__id'

    DEFAULT_CURSOR_TYPE = CursorType.TAILABLE_AWAIT

    live_stats_cache_class = LiveStatsCache

    def __init__(self, cache='default', clear=False, init=False,
                                db=None, coll=None, parent_api=None, cursor_type=None ):
        """
        by default, uses all the enabled Trigger(s), see /admin/dataden/trigger/

        clear=True  does a world wipe of the cache.
        all=True    parses the oplog from the begining, instead of from "now"

        if 'db', 'coll', and 'parent_api' all exist, just run
        the Trigger with a single trigger enabled, specified by those params

        :param db:
        :param coll:
        :param parent_api:
        :param cache:
        :param clear:
        :param init:
        :param triggers:
        :return:
        """
        self.init         = init            # default: False, if True, parse entire log
        self.client       = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
        self.last_ts      = None

        #
        # usually these are all set to None, and we use the admin configured triggers
        self.db_name      = db              # ie: 'nba', 'nfl'
        self.coll_name    = coll            # ie: 'player', 'standings'
        self.parent_api   = parent_api      # dataden's name for the feed to look in

        self.timer      = SimpleTimer()

        self.db_local   = self.client.get_database( self.DB_LOCAL )
        self.oplog      = self.db_local.get_collection( self.OPLOG )

        # self.live_stats_cache   = LiveStatsCache( cache, clear=clear )
        self.live_stats_cache   = self.live_stats_cache_class( cache, clear=clear )

        self.trigger_cache      = TriggerCache()

        self.cursor_type = cursor_type

    def single_trigger_override(self):
        """
        if this returns True, it will block the query() from
        building a query for all the enabled Triggers,
        and thus making Trigger capable of applying 1-off triggers
        even if there are others running. Should really only
        be used for dev/testing purposes because too many
        single Triggers will put a load on cpu/mongodb

        :return:
        """
        return self.db_name and self.coll_name and self.parent_api

    def run(self, last_ts=None):
        """
        if last_ts is not specified, we start parsing essentially any second now,
        but we do not get anything that happened a short while ago.

        run the watcher, and start triggering on relevant db_name/coll_name.
        if last_ts is set, start from as far back as (but not guaranteed to be) last_ts.

        :return:
        """
        #self.display()

        if last_ts:
            self.last_ts = last_ts # user wants to start from at least this specific ts
        else:
            self.last_ts = self.get_last_ts() # get most recent ts, (by default, dont reparse the world)

        #print('last_ts():', str(self.last_ts))
        self.timer.start()
        self.reload_triggers() # do this pre query() being called

        #
        # using a tailable cursor allows us to loop on it
        # and we will pick up new objects as they come into
        # the oplog based on whatever our query is!
        cur = self.get_cursor( self.oplog, self.query(), cursor_type=self.cursor_type )
        while cur.alive:
            try:
                obj = cur.next()
            except StopIteration:
                #print('waiting')
                continue

            hashable_object = OpLogObj(obj)
            self.last_ts = hashable_object.get_ts()

            #
            # the live stats cache will filter out objects
            # from being sent unless its the first time
            # they've been seen, or if there have been changes
            if self.live_stats_cache.update( hashable_object ):
                # primarily for sumo logic, log this object making
                # sure to include the 'ts' timestamp from the oplog
                self.log_for_sumo( hashable_object )

                # the object is new or has been updated.
                # send the update signal along with the object to Pusher/etc...
                Update( hashable_object ).send(async=True)

            ns = hashable_object.get_ns()
            parent_api = hashable_object.get_parent_api()

    def log_for_sumo(self, hashable_object):
        """
        log the mongo object the instant we pick it up in from the oplog.
        be sure to present and identifiable token for the object,
        as well as the oplog objects 'ts' field, from which we can
        get a unix timestamp of the time it was added to mongo.

        :param hashable_object: an instance of OpLogObj
        :return:
        """

        # create a hashable using just the 'o' fields object,
        # which is the actual dataden object
        dd_hashable = Hashable(hashable_object.get_o())

        # log this object from the oplog, including the dataden object's hash value.
        # the hash value of the inner object should be logged later on
        # so that we can track this object thru the system.
        log_msg = 'MONGO_LOG=%s, MONGO_OBJ_TS=%s, MONGO_OBJ=%s, DD_HASH=%s,' \
                  '' % ('OpLogTrigger', hashable_object.get_ts().time,
                        str(hashable_object), dd_hashable.hsh())
        print(log_msg)

    def reload_triggers(self):
        self.triggers = self.trigger_cache.get_triggers()

    def get_ns(self):
        return '%s.%s' % (self.db_name, self.coll_name)

    def get_last_ts(self):
        """
        sets the last_ts internally, and then returns the same value.
        must be called before query() is generated

        :return:
        """
        #self.timer.start()
        cur = self.oplog.find().sort([('$natural', -1)])
        for obj in cur:
            self.last_ts = OpLogObj( obj ).get_ts()
            #self.timer.stop(msg='get_last_ts()')
            return self.last_ts

    def query(self):
        """
        when we get many triggers, the need arises for us to run the results
        thru a filter of our originally requested filters, because we are
        trying to get it done in a single query, and there will be permutations
        of namespace-parent_api that we dont actually want!!!

        we do query for efficiency, because itll actually
        be a lot faster to get more than we need in a single query + filter out some things,
        than it would be to get exactly what we need in multiple queries.

        :return:
        """
        if self.single_trigger_override():
            #
            # single trigger specified
            single_trig = '<<< %s.%s %s >>>' % (self.db_name, self.coll_name, self.parent_api)
            print('single_trigger_override() True - triggering on %s' % single_trig)
            q = {
                'ts' : {'$gt' : self.last_ts},
                #'ts' : {'$gt' : str( self.last_ts.time * 1000 + self.last_ts.inc) },
                'ns' : '%s.%s' % (self.db_name, self.coll_name),
                'o.%s' % self.PARENT_API__ID : self.parent_api,
            }
        else:
            #
            # "normal" operation - uses the enabled triggers to build the query!
            # coll.find(
            #   {
            #       '$or' : [
            #           {'$and' : [ {'ns':'mlb.game'}, {'o.parent_api__id':'pbp'} ] },
            #           {'$and' : [ {'ns':'mlb.game'}, {'o.parent_api__id':'summary'} ] }
            #       ]
            #   }
            # ).count()
            q_triggers = []
            for trig in self.triggers:
                where_args = [
                    {'ns':'%s.%s'%(trig.db,trig.collection)},
                    {'o.%s'%self.PARENT_API__ID:trig.parent_api}
                ]
                q_triggers.append(
                    { '$and' : where_args }
                )

            q = {
                'ts' : {'$gt' : self.last_ts},   # older version required this
                #'ts' : {'$gt' : str( self.last_ts.time * 1000 + self.last_ts.inc) },
                # 'ns' : { '$in' : ns_list },
                # 'o.%s' % self.PARENT_API__ID : { '$in': api_list },
                '$or' : q_triggers,

            }

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

    # def display(self):
    #     print('%s [ trigger running on <<< %s.%s %s >>' % (self.__class__.__name__,
    #                                 self.db_name, self.coll_name, 'parent_api: %s' % self.parent_api) )

    def trigger_debug(self, object):
        print( object )

    def trigger(self):
        raise UnimplementedTriggerCallbackException(
            self.__class__.__name__ + 'must implement trigger() method')
