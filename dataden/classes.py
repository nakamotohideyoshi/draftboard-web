#
# dataden/classes.py

from pymongo import MongoClient, ASCENDING, DESCENDING
import dataden.cache.caches
import dataden.models
from django.conf import settings

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
            self.client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
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

    #
    # to determine the season, i should just get the most RECENT closed game
    # and get what its season and season_type are, and consider us to be that
    # then get all games of that season and type.

    #
    # nba_seasons = dd.find('nba','season_schedule','schedule', {'parent_api__id':'schedule'})
    # { 'type' : 'PST',
    #     'parent_api__id' :
    #     'schedule' }
    #
    # nfl_seasons = dd.find('nfl','season','schedule', {'parent_api__id':'schedule'})
    # {
    #     "season" : 2015,
    #     "type" : "REG",
    #     "xmlns" : "http://feed.elasticstats.com/schema/nfl/schedule-v1.0.xsd",
    #     "parent_api__id" : "schedule",
    #
    def find_games(self, sport='nfl', year=None, season_ids=[], week=None, verbose=True):
        """
        Get the game objects from the schedule feed for the specified 'season' (ie: year)

        Do this by getting:
            1. the season objects for the given 'year'
            2. all the games with match season__id

        If 'year' is None, retrievs all the games in database.
        If 'season_ids' is not specified, gets all for the year.
        """
        if verbose: print('searching games...')
        if year:
            if verbose: print('    ','year:', year)

            if season_ids:
                if verbose: print('    ','season_ids specified:')
            else:
                seasons = self.find(sport,'season','schedule',{'season':year})
                for s in seasons:
                    if s not in season_ids:
                        season_ids.append( s.get('id') )

            # print them for clarity
            if verbose:
                for sid in season_ids:
                    print('    ','    ... ', sid)

            # only return games from the specified week, if the param is not None
            target = {'season__id':{'$in':season_ids}}

            if week:
                if verbose: print('    ','week:', week)
                # print('    ','')
                # get the season(s) objects for this week
                week_game_ids = []
                seasons = self.find(sport,'season', 'schedule',{'id':{'$in':season_ids}})

                # this looks complicated but its just very
                # specifically extracting a nested list
                # of gameid(s) -- as specified by the year, season, week --
                # and it puts those gameids into 'week_game_ids'
                for season in seasons:
                    weeks_list = season.get('weeks', [])
                    for week_json in weeks_list:
                        game_list = week_json.get('week', {})
                        if game_list.get('week',-1) != week:
                            continue
                        inner_games = game_list.get('games',[])
                        if inner_games == []:
                            # its possible its a single game
                            week_game_ids.append( game_list.get('game') )
                        else:
                            for obj in inner_games:
                                gameid = obj.get('game', None)
                                if gameid not in week_game_ids:
                                    week_game_ids.append( gameid )

                #print( 'target game ids:', str(week_game_ids))
                target = {'id':{'$in':week_game_ids}}

            # get the games with the specified target query
            if verbose: print( str(target) )
            games = self.find(sport,'game','schedule',target)

        else:
            games = self.find(sport,'game','schedule') # gets all games in db

        #
        # build a msg to explain how many, and where we found games, its vvvvery (4 V's) useful most times
        games_found_msg = '%s %s' % (str(games.count()), 'game(s) found by DataDen for:')
        if year:
            games_found_msg += '\n    year: %s'      % str(year)
            if season_ids:
                games_found_msg += '\n    season_ids:'
                for season_id in season_ids:
                    games_found_msg += '\n        - %s' % season_id
            if week:
                games_found_msg += '\n    week: %s' % str(week)
        else:
            games_found_msg += ' all-time!'

        print( games_found_msg )
        return games

class AbstractSeasonGames(DataDen):

    def __init__(self, sport, year, schedule_collection, parent_api):
        super().__init__()
        self.sport                  = sport
        self.year                   = year
        self.schedule_collection    = schedule_collection
        self.parent_api             = parent_api

    def get_game_ids_regular_seaons(self):
        raise Exception( 'child class must override get_game_ids_regular_season() to get the games for its sport' )

    def get_game_ids(self, season_type=None):
        """
        get the games for this season

        get the regular season games for the year if the season_type is not specified
        :return:
        """
        raise Exception('child class must override get_game_ids() to get the games for its sport')

    def get_seasons(self, target={}):
        return self.find(self.sport, self.schedule_collection, self.parent_api, target=target )

class NbaSeasonGames(AbstractSeasonGames):

    SEASON_PRE = 'PRE'
    SEASON_REG = 'REG'
    SEASON_PST = 'PST'

    def __init__(self, year):
        super().__init__('nba', year, 'season_schedule', 'schedule')

    def get_game_ids_regular_season(self):
        return self.get_game_ids(season_type=self.SEASON_REG)

    def get_game_ids(self, season_type):
        # N2QyZGYyNWNpZDUyOWJlZDM0LTVhOGQtNDZkNC05ZWVmLTExNGJkMTM0MDg2Nw==",
        # "id" : "529bed34-5a8d-46d4-9eef-114bd1340867",
        # "type" : "PST",
        # "year" : 2015,
        # "parent_api__id" : "schedule",

        target = {
            'type' : season_type,
            'year' : int(self.year),
        }
        seasons = self.get_seasons(target=target)
        if seasons.count() != 1:
            raise Exception('found more than 1 season object for %s/%s/%s!'%(self.sport,
                                                            str(self.year), season_type))

        game_ids = []
        for s in seasons:
            games_list = s.get('games__list')
            for g in games_list:
                game_ids.append( g.get('game') )
            break

        print('%s game_ids' % (len(game_ids)))
        return game_ids

class NflSeasonGames(AbstractSeasonGames):

    SEASON_PRE = 'PRE'
    SEASON_REG = 'REG'
    SEASON_PST = 'PST'

    def __init__(self, year):
        super().__init__('nfl', year, 'season', 'schedule')

    def get_game_ids_regular_season(self):
        return self.get_game_ids(season_type=self.SEASON_REG)

    def get_game_ids(self, season_type):
        # N2QyZGYyNWNpZDUyOWJlZDM0LTVhOGQtNDZkNC05ZWVmLTExNGJkMTM0MDg2Nw==",
        # "id" : "529bed34-5a8d-46d4-9eef-114bd1340867",
        # "type" : "PST",
        # "year" : 2015,
        # "parent_api__id" : "schedule",

        target = {
            'season' : int(self.year),
            'type' : season_type,
        }
        seasons = self.get_seasons(target=target)
        if seasons.count() != 1:
            raise Exception('found more than 1 season object for %s/%s/%s!'%(self.sport,
                                                            str(self.year), season_type))

        game_ids = []
        for s in seasons:
            weeks = s.get('weeks')
            for week_obj in weeks:
                inner_week = week_obj.get('week')
                week_number = inner_week.get('week')
                print( 'week_number:', str(week_number) )
                games = inner_week.get('games')
                for game in games:
                    game_ids.append( game.get('game') )
            break

        print('%s game_ids' % (len(game_ids)))
        return game_ids



