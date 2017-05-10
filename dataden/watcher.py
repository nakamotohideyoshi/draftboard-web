import threading
from logging import getLogger
from threading import Thread

import pymongo
from django.conf import settings
from django_redis import get_redis_connection
from pymongo import MongoClient
from pymongo.cursor import CursorType
from raven.contrib.django.raven_compat.models import client

from dataden.cache.caches import LiveStatsCache, TriggerCache
from dataden.signals import Update
from dataden.util.hsh import Hashable
from dataden.util.simpletimer import SimpleTimer
from util.timesince import timeit

# this setting can have a huge impact on the speed of stat updates
# because it will us celery tasks to do all the updates, but
# that can have the affect of hammering the disk - it works, but
# has not been battle tested on heroku yet. currently it will
# bring a vagrant VM to its knees.
ASYNC_UPDATES = settings.DATADEN_ASYNC_UPDATES  # False for dev
logger = getLogger('dataden.watcher')


class UnimplementedTriggerCallbackException(Exception):
    def __init__(self, class_name, variable_name):
        super().__init__("The trigger() callback is unimplemented.")


class ParentApis(object):
    def __init__(self, mongo_client=None):
        self.client = mongo_client
        if not self.client:
            # self.client = local.get_mongo_client() # cheese
            self.client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)

    def all(self):
        pass  # TODO


class OpLogObj(Hashable):
    """
    This is just a data bucket for for MongoDB OpLog objects.
    it has a few getter methods and some type checking.
    """

    exclude_field_names = ['dd_updated__id']

    def __init__(self, obj):
        self.original_obj = obj  # save the original object
        self.ts = obj.get('ts')
        self.ns = obj.get('ns')
        self.o = obj.get('o')

        #
        # certain fields we want to remove because
        # they arent relevant, or serializable and
        # will break the hash mechanism
        tmp = {}
        for field_name in self.exclude_field_names:
            val = self.o.pop(field_name, None)
            if val:
                tmp[field_name] = val

        #
        # the constructor for Hashable hashes the object once
        # so after this call, we can put the exclude fields back in
        super().__init__(self.o)

        for k, v in tmp.items():
            self.o[k] = v

    def __str__(self):
        return str(self.original_obj)

    def override_new(self):
        """
        subclasses can override this method to provide their own logic
        to return a boolean indicating if this object should bypass the
        trigger filter or not -- even if its not the first time its seen.
        """
        return False

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


class OpLogObjWrapper(OpLogObj):
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
        "ts": 0,  # currently, we dont care about this field
        "h": 0,  # currently, we dont care about this field
        "v": 2,  # currently, we dont care about this field
        "op": "u",  # currently, we dont care about this field

        "ns": None,  # ie: "nba.player",
        "o2": {
            "_id": None  # mongo obj's "_id" field
        },
        "o": None,  # regular_mongo_obj (ie: {})
    }

    def __init__(self, db, coll, mongo_obj):
        #
        # copy OPLOG_WRAPPER, and create our new wrapped obj with the important fields
        wrapped_obj = {}
        for key, val in self.OPLOG_WRAPPER.items():
            if key == 'ns':
                new_val = '%s.%s' % (db, coll)  # create the 'ns' string!
            elif key == 'o':
                new_val = mongo_obj  # !
            else:
                # set with whatever is in OPLOG_WRAPPER
                new_val = val
            wrapped_obj[key] = new_val

        #
        # now create the OpLogObj with our spoofed obj
        super().__init__(wrapped_obj)

    @staticmethod
    def wrap(data, ns=None):
        oplog_obj = OpLogObjWrapper.OPLOG_WRAPPER.copy()
        if ns is not None:
            # ns, the "namespace" is the <db>.<collection> the object comes from
            # as an example here is an at-bat from mlb:   'mlb.at_bat'
            oplog_obj['ns'] = ns
        oplog_obj['o'] = data
        return oplog_obj


class OpLogObjWithTs(OpLogObj):
    """
    override OpLogObj not to exclude any of the fields
    of the main DataDen object (note: we always ignore
    the mongo oplog wrapper when hsh() is called).
    """

    exclude_field_names = []


class UpdateWorker(Thread):
    """
    This is a worker thread that churns through events from the mongo oplog. It checks to see
    if we've seen the event already, if not, create a celery task to parse it.
    """

    def __init__(self, obj_list, oplogobj_class, live_stats_cache, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.oplogobj_class = oplogobj_class
        self.obj_list = obj_list
        self.live_stats_cache = live_stats_cache

    def run(self):
        """ start working by calling: start() """
        try:
            counter = 0
            for obj in self.obj_list:
                # create a hashable object as the key to cache it with
                hashable_object = self.oplogobj_class(obj)

                # the live stats cache will add every item it sees to the redis cache
                if self.live_stats_cache.update(hashable_object):
                    # the object is new or has been updated.
                    # send the update signal along with the object to Pusher/etc...
                    counter += 1
                    Update(hashable_object).send(async=True)

            # Some debugging info for current redis connection count
            r = get_redis_connection()
            connection_pool = r.connection_pool

            logger.info(
                'UpdateWorker.run() (%s workers, %s redis connections). '
                '%s of %s Dataden objects  sent to Celery' %
                (threading.active_count(), connection_pool._created_connections,
                 counter, len(self.obj_list)))

        # We want redis connection errors to kill the thread. Otherwise we end up with a
        # deadlock situation and the dyno process is stuck.
        # except redis.ConnectionError as e:
        #     # If you get a `Too many connections` error coming from here, it
        #     # actually means there are not enough connections left in the
        #     # connection pool in order to complete this worker's task. You can
        #     # either bump up the redis connection pool limit, or increase the
        #     # number of object each worker handles with the `work_size` attribute.
        #     raise e

        # Catch any other exceptions that are likely to be event-specific, which means we do
        # not want to kill the thread. Log the error and continue processing remaining events.
        except Exception as e:
            logger.error(e)
            client.captureException()
            raise e


class Trigger(object):
    """
    uses local.oplog.rs to implement mongo triggers
    """
    work_size = 2000

    DB_LOCAL = 'local'
    OPLOG = 'oplog.rs'

    PARENT_API__ID = 'parent_api__id'

    # originally, it works fine, just slow startup for complex queries/big oplogs
    cursor_type = CursorType.TAILABLE_AWAIT
    # cursor_type = CursorType.TAILABLE

    live_stats_cache_class = LiveStatsCache

    oplogobj_class = OpLogObj

    def __init__(self, cache='default', clear=False, init=False, db=None, coll=None,
                 parent_api=None, t=None):
        """
        by default, uses all the enabled Trigger(s), see /admin/dataden/trigger/

        clear=True  does a world wipe of the cache.
        all=True    parses the oplog from the begining, instead of from "now"

        if 'db', 'coll', and 'parent_api' all exist, just run
        the Trigger with a single trigger enabled, specified by those params

        't' can be used to pass a dataden.models.Trigger instead of
                having to type the db, coll, and parent_api
        """
        self.init = init  # default: False, if True, parse entire log
        self.client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
        # self.client = MongoClient() # localhost/default port
        self.last_ts = None

        #
        # usually these are all set to None, and we use the admin configured triggers
        self.db_name = db  # ie: 'nba', 'nfl'
        self.coll_name = coll  # ie: 'player', 'standings'
        self.parent_api = parent_api  # dataden's name for the feed to look in
        if t is not None:
            ns_parts = t.ns.split('.')
            self.db_name = ns_parts[0]
            self.coll_name = ns_parts[1]
            self.parent_api = t.parent_api

        self.timer = SimpleTimer()

        # self.db_local   = self.client.get_database( self.DB_LOCAL )
        # self.oplog      = self.db_local.get_collection( self.OPLOG )
        # self.oplog = self.client.local.oplog.rs

        # self.live_stats_cache   = LiveStatsCache( cache, clear=clear )
        self.live_stats_cache = self.live_stats_cache_class(cache, clear=clear)

        self.trigger_cache = TriggerCache()

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

        if last_ts:
            # user wants to start from at least this specific ts
            self.last_ts = last_ts
        else:
            # get most recent ts, (by default, dont reparse the world)
            self.last_ts = self.get_last_ts(now=True)  # now=True means dont query it, just guess it

        # do this previous to query() being called
        self.reload_triggers()

        #
        # using a tailable cursor allows us to loop on it
        # and we will pick up new objects as they come into
        # the oplog based on whatever our query is!
        obj_list = []
        ctr = 0
        cur = self.get_cursor(self.query())
        while cur.alive:

            try:
                obj = cur.next()
            except StopIteration:
                # we should realize theres nothing left and
                # send current UpdateWorker unless theres
                # actually 0 things left to send
                if len(obj_list) > 0:
                    worker = UpdateWorker(obj_list, self.oplogobj_class, self.live_stats_cache)
                    worker.start()  # join it? will it die? should we hold onto it?
                    # and reset ctr and obj_list
                    ctr = 0
                    obj_list = []  # and reset obj_list

                continue

            ctr += 1
            obj_list.append(obj)

            if ctr >= self.work_size:
                worker = UpdateWorker(obj_list, self.oplogobj_class, self.live_stats_cache)
                worker.start()  # join it? will it die? should we hold onto it?
                # and reset ctr and obj_list
                ctr = 0
                obj_list = []  # and reset obj_list

                # starves the last couple object every round....

                # work method now:
                # # create a hashable object as the key to cache it with
                # hashable_object = self.oplogobj_class(obj)
                #
                # # the live stats cache will add every item it sees to the redis cache
                # if self.live_stats_cache.update( hashable_object ):
                #     # the object is new or has been updated.
                #     # send the update signal along with the object to Pusher/etc...
                #     print('trigger:', str(obj))
                #     Update( hashable_object ).send(async=True)

    @staticmethod
    def log_for_sumo(hashable_object):
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
        logger.info(log_msg)

    def reload_triggers(self):
        logger.info('Reloading triggers...')
        self.triggers = self.trigger_cache.get_triggers()

    def get_ns(self):
        return '%s.%s' % (self.db_name, self.coll_name)

    @timeit
    def get_last_ts(self, now=True):
        """
        sets the last_ts internally, and then returns the same value.
        must be called before query() is generated

        :return:
        """
        # first = oplog.find().sort('$natural', pymongo.DESCENDING).limit(-1).next()
        # ts = first['ts']

        # originally, works, but sorting large oplog time consuming
        # if now:
        #     now = time.time()
        #     self.last_ts = Timestamp(int(now), int((now*10000000) % 10000000))
        # else:

        first = self.client.local.oplog.rs.find().sort('$natural', pymongo.DESCENDING).limit(
            1).next()
        self.last_ts = first.get('ts')
        return self.last_ts
        # cur = self.client.local.oplog.rs.find().sort([('$natural', -1)])
        # for obj in cur:
        #     self.last_ts = self.oplogobj_class( obj ).get_ts()
        #     return self.last_ts

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
            # single_trig = '<<< %s.%s %s >>>' % (self.db_name, self.coll_name, self.parent_api)
            # print('single_trigger_override() True - triggering on %s' % single_trig)
            q = {
                'ts': {'$gt': self.last_ts},
                # 'ts' : {'$gt' : str( self.last_ts.time * 1000 + self.last_ts.inc) },
                'ns': '%s.%s' % (self.db_name, self.coll_name),
                'o.%s' % self.PARENT_API__ID: self.parent_api,
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
                    {'ns': '%s.%s' % (trig.db, trig.collection)},
                    {'o.%s' % self.PARENT_API__ID: trig.parent_api}
                ]
                q_triggers.append(
                    {'$and': where_args}
                )

            q = {
                'ts': {'$gt': self.last_ts},
                '$or': q_triggers,
            }

        if self.init == True:  # explicity showing if its == True, because this will be rare
            self.init = False  # toggle it off after the first run though !
            q.pop('ts', None)

        return q

    @timeit
    def get_cursor(self, query, hint=[('$natural', 1)]):
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
        # if cursor_type is None:
        #     cursor_type = CursorType.TAILABLE_AWAIT

        # while True:
        #     cursor = oplog.find({'ts': {'$gt': ts}}, tailable=True, await_data=True)
        #     # oplogReplay flag - not exposed in the public API
        #     cursor.add_option(8)
        #     while cursor.alive:
        #         for doc in cursor:
        #             ts = doc['ts']
        #             # Do something...
        #         time.sleep(1)

        cur = self.client.local.oplog.rs.find(query,
                                              cursor_type=self.cursor_type)  # , await_data=True)
        # cur = collection.find(query, cursor_type=self.cursor_type)
        ##cur.add_option(8)
        # cur = cur.hint(hint) # maybe later
        return cur

    def trigger_debug(self, object):
        print(object)

    def trigger(self):
        raise UnimplementedTriggerCallbackException(
            self.__class__.__name__ + 'must implement trigger() method')


class TriggerAll(Trigger):
    """
    this trigger sends out all objects all objects it sees
    after placing them in the cache.
    """

    oplogobj_class = OpLogObjWithTs

    def run(self, last_ts=None):
        """
        use the live stats cache to update() the hashable
        objects from the oplog but instead of only
        sending objects without changes based on the return
        value of update() this method sends every
        object, every time!
        """

        if last_ts:
            # user wants to start from at least this specific ts
            self.last_ts = last_ts
        else:
            # get most recent ts, (by default, dont reparse the world)
            self.last_ts = self.get_last_ts()

        # do this previous to query() being called
        self.reload_triggers()

        #
        # using a tailable cursor allows us to loop on it
        # and we will pick up new objects as they come into
        # the oplog based on whatever our query is!
        cur = self.get_cursor(self.oplog, self.query(), cursor_type=self.cursor_type)
        while cur.alive:

            try:
                obj = cur.next()
            except StopIteration:
                continue

            # create a hashable object as the key to cache it with
            hashable_object = self.oplogobj_class(obj)

            # the live stats cache will add every item it sees to the redis cache
            self.live_stats_cache.update(hashable_object)

            # the object is new or has been updated.
            # send the update signal along with the object to Pusher/etc...
            Update(hashable_object).send(async=True)
