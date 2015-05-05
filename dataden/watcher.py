#
# dataden/watcher.py

from pymongo import MongoClient
from pymongo.cursor import _QUERY_OPTIONS, CursorType
import re, time

#
# TODO - get the oplog collection and do our thing with it
# TODO - see if we have access to this on heroku !?

class UnimplementedTriggerException(Exception):
    pass

#
# abstract
class Trigger(object):
    """
    uses local.oplog.rs to implement mongo triggers
    """

    DB_LOCAL    = 'local'
    OPLOG       = 'oplog.rs'

    def __init__(self, db, coll):
        self.client         = MongoClient() # defaults to localhost:27017
        self.last_ts        = None
        self.db_name        = db            # ie: 'nba', 'nfl'
        self.coll_name      = coll          # ie: 'player', 'standings'

        self.db_local   = self.client.get_database( self.DB_LOCAL )
        self.oplog      = self.db_local.get_collection( self.OPLOG )

    def run(self, last_ts=None):
        """
        run the watcher, and start triggering on relevant db_name/coll_name.
        if last_ts is set, start from as far back as (but not guaranteed to be) last_ts.

        :return:
        """
        if last_ts:
            self.last_ts = last_ts # user wants to start from at least this specific ts
        else:
            self.last_ts = self.get_last_ts() # get most recent ts, (by default, dont reparse the world)

        while True:
            cur = self.get_cursor( self.oplog, self.query() )

            count = 0
            for obj in cur:
                #print( obj.get('ts'), obj.get('ns') )
                self.last_ts = obj['ts']
                #
                # TODO = comment this back in later, for now going to test print stuff
                #self.trigger(msg)
                self.trigger_debug(obj)
                count += 1

            print( str(count), 'objects triggered on')
            time.sleep(0.1) # not necessary

    def get_last_ts(self):
        """
        sets the last_ts internally, and then returns the same value.
        must be called before query() is generated

        :return:
        """
        cur = self.oplog.find().sort([('$natural', -1)])
        for obj in cur:
            self.last_ts = obj['ts']
            return self.last_ts

    def query(self):
        q = {
            'ts' : {'$gt' : self.last_ts},
            'ns' : '%s.%s' % (self.db_name, self.coll_name)
        }
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

    def trigger_debug(self, object):
        print( object )

    def trigger(self):
        raise UnimplementedTriggerException(self.__class__.__name__ + 'must implement trigger() method')

class NbaPlayer(Trigger):

    #
    # may want to specify the parent api id as well

    DB_NBA      = 'nba'
    COLL_PLAYER = 'player'

    def __init__(self):
        super().__init__(self.DB_NBA, self.COLL_PLAYER)


    #
    # ORIGINAL
    # last_id = -1
    # cur = db.capped_collection.find().sort([('$natural', -1)])
    # for msg in cur:
    #     last_id = msg['ts']
    #     break
    #
    # while True:
    #     cur = get_cursor(
    #         db.capped_collection,
    #         re.compile('^foo'),
    #         await_data=True)
    #     for msg in cur:
    #         last_id = msg['ts']
    #         do_something(msg)
    #     time.sleep(0.1)
    #
    # def get_cursor(collection, topic_re, last_id=-1, await_data=True):
    #     options = { 'tailable': True }
    #     spec = {
    #         'ts': { '$gt': last_id }, # only new messages
    #         'k': topic_re }
    #     if await_data:
    #         options['await_data'] = True
    #     cur = collection.find(spec, **options)
    #     cur = cur.hint([('$natural', 1)]) # ensure we don't use any indexes
    #     if await:
    #         cur = cur.add_option(_QUERY_OPTIONS['oplog_replay'])
    #     return cur