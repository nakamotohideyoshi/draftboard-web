#
# dataden/classes.py

from pymongo import MongoClient, ASCENDING, DESCENDING
import dataden.cache.caches
import dataden.models
from mysite.settings import base as base_settings

class Trigger(object):
    """
    retrieve a Trigger from the database by its pk, throws DoesNotExist
    """

    def __init__(self, pk):
        """
        assumes it exists since you are getting it by pk
        """
        self.t = dataden.models.Trigger.objects.get(pk=pk)

    def get_enabled(self):
        return self.t.enabled

    def enable(sport):
        """
        Enables all the triggers for the specific sport.
        """
        triggers = dataden.models.Trigger.objects.all()
        for t in triggers:
            if t.db == sport:
                t.enabled = True
                t.save()
    enable = staticmethod(enable)

    def disable(sport):
        """
        Enables all the triggers for the specific sport.
        """
        triggers = dataden.models.Trigger.objects.all()
        for t in triggers:
            if t.db == sport:
                t.enabled = False
                t.save()
    disable = staticmethod(disable)

    def __str__(self):
        """
        print the model this class is a wrapper for
        """
        return str(self.t)

    def set_enabled(self, enable):
        """
        set_enabled( True ) turns the trigger on
        set_enabled( False ) disables the trigger
        """
        self.t.enabled = enable
        self.t.save()

    def create( db, collection, parent_api, enable=False ):
        try:
            trig = dataden.models.Trigger.objects.get( db=db,
                    collection=collection, parent_api=parent_api)
        except dataden.models.Trigger.DoesNotExist:
            trig = dataden.models.Trigger()
            trig.db             = db
            trig.collection     = collection
            trig.parent_api     = parent_api
            trig.enabled        = enable
            trig.save()
        return Trigger( pk=trig.pk )
    create = staticmethod( create )

class DataDen(object):
    """
    caleb: im intending on this being the thru-point for rest_api calls
    """

    DB_CONFIG = 'config'

    COLL_SCHEDULE = 'schedule'

    PARENT_API__ID = 'parent_api__id'
    DD_UPDATED__ID = 'dd_updated__id'

    def __init__(self, client=None):
        """
        if client is None, we will attempt to connect on default localhost:27017

        :param client:
        :return:
        """

        self.client = None

        #
        # get the default cache for DataDen
        self.live_stats_cache = dataden.cache.caches.LiveStatsCache()

    def connect(self):
        if self.client:
            #print('connected to mongo')
            return
        #
        # else
        try:
            self.client = MongoClient(base_settings.MONGO_HOST, base_settings.MONGO_PORT)
        except:
            self.client = None
            raise Exception('error connecting to mongo!')

    def db(self, db_name):
        self.connect()
        return self.client.get_database( db_name )

    def find(self, db, coll, parent_api, target={}, projection={}):
        """
        Perform a mongo find( target ) on the namespace and parent_api!

        'parent_api' is always added as a top level field of 'target' dictionary

        :return:
        """

        coll = self.db( db ).get_collection(coll)
        target[ self.PARENT_API__ID ] = parent_api
        if projection and projection.keys():
            #
            # if the projection has any keys, use it
            return coll.find( target, projection )

        # by default, dont apply projection
        return coll.find( target )

    def find_recent(self, db, coll, parent_api, target={}):
        """
        Get a cursor the objects from these args which were parsed by the most recent parsing.

        If there are objects with different 'dd_updated__id' values (a timestamp),
        this method only returns the objects with the most recent timestamp.

        Returns None if no objects are found.

        :param db:
        :param coll:
        :param parent_api:
        :param target:
        :return:
        """
        all_objects = self.find(db, coll, parent_api, target).sort(self.DD_UPDATED__ID, DESCENDING)
        for obj in all_objects:
            #
            # get the timestamp of the first object (because we are sorted descending
            ts_last_parse = obj.get(self.DD_UPDATED__ID, None)

            #
            # get all the most recently parsed injury objects from dataden.
            #  use '$gte' in case new objects have been added recently !
            return self.find(db, coll, parent_api, {self.DD_UPDATED__ID:{'$gte':ts_last_parse }})
        #
        # return empty cursor if no objects exist
        return all_objects

    def enabled_sports(self):
        coll = self.db(self.DB_CONFIG).get_collection(self.COLL_SCHEDULE)
        return coll.distinct('sport')

    def walk(self, sport=None, examples=False):
        """
        if sport is None, walks all enabled_sports().

        given the sport name, ie: 'mlb' or 'nfl', dump out all the unique objects
        for namespace and parent_api combinations

        very useful for debugging or if you want to see all the different
        types of stat objects for the given sport

        if examples=True, it dumps out a findOne() for every unique object
        which can help visualize the data quite a bit. However, you've been
        warned that a lot of times find_one() grabs a useless piece of data
        for a player who might not have played in the game and it can be
        lacking inner data. At the same time, it will dump out a massive
        amount of objects, but should be pretty easy to read in a large
        text editor

        :param sport:
        :return:
        """
        if sport:
            walk_sports = [ sport ]
        else:
            walk_sports = self.enabled_sports()

        for sport in walk_sports:
            print(sport)
            collection_names = self.db(sport).collection_names()
            for collection_name in collection_names:
                coll = self.db(sport).get_collection(collection_name)
                print('    ' + collection_name)
                parent_apis = coll.distinct(self.PARENT_API__ID)
                for parent_api in parent_apis:
                    print('        ' + parent_api )
                    if examples:
                        ex = coll.find_one({ self.PARENT_API__ID : parent_api })
                        print( '            ' + str(ex) )
