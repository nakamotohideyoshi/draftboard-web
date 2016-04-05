from __future__ import generators
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

    class InvalidTypeException(Exception): pass

    DB_CONFIG = 'config'

    COLL_SCHEDULE = 'schedule'

    PARENT_API__ID = 'parent_api__id'
    DD_UPDATED__ID = 'dd_updated__id'

    def __init__(self, client=None, no_cursor_timeout=False):
        """
        if client is None, we will attempt to connect on default localhost:27017

        :param client:
        :return:
        """

        self.client = None
        self.no_cursor_timeout = no_cursor_timeout

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
        # ensure the db_name is a string
        if not isinstance(db_name, str):
            raise self.InvalidTypeException(type(self).__name__, type(db_name).__name__)

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
            return coll.find( filter=target, projection=projection, no_cursor_timeout=self.no_cursor_timeout )

        # by default, dont apply projection
        return coll.find( filter=target, no_cursor_timeout=self.no_cursor_timeout )

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
            target[self.DD_UPDATED__ID] = {'$gte':ts_last_parse }
            # return self.find(db, coll, parent_api, {self.DD_UPDATED__ID:{'$gte':ts_last_parse }})
            return self.find(db, coll, parent_api, target)
        #
        # return empty cursor if no objects exist
        return all_objects

    def aggregate(self, db, coll, pipeline):
        """
        regular queries not enough for you? no? you want to branch out
         and do something that is unbelievably complex, huh? ... and
         you want to do it one single operation!? look no further.

        pipline example for getting the 'at_bat' out of the super-nested mlb inning structure:

            pipeline = [
                {"$match": {"id": "0f36323c-ba26-4272-ab93-f1630def90a1"} },
                {"$unwind": "$innings"},
                {"$match": {"innings.inning.inning_halfs.inning_half.at_bats.at_bat.pitchs.pitch": "70ad813e-98eb-4160-9c44-b860e64f21f4"} },
                {"$project": {"inning_halfs":"$innings.inning.inning_halfs"}},
                {"$unwind": "$inning_halfs"},
                {"$match": {"inning_halfs.inning_half.at_bats.at_bat.pitchs.pitch": "70ad813e-98eb-4160-9c44-b860e64f21f4"} },
                {"$project": {"at_bats":"$inning_halfs.inning_half.at_bats"}},
                {"$unwind": "$at_bats"},
                {"$match": {"at_bats.at_bat.pitchs.pitch": "70ad813e-98eb-4160-9c44-b860e64f21f4"} },
                {"$project": {"at_bat":"$at_bats.at_bat"}},
            ]

        :param pipeline: list of commands to run in order, using mongos aggregation framework
        :return: list of matched objs
        """
        return list(self.db(db).get_collection(coll).aggregate(pipeline))

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
#     def find_games(self, sport='nfl', year=None, season_ids=[], week=None, verbose=True):
#         """
#         Get the game objects from the schedule feed for the specified 'season' (ie: year)
#
#         Do this by getting:
#             1. the season objects for the given 'year'
#             2. all the games with match season__id
#
#         If 'year' is None, retrievs all the games in database.
#         If 'season_ids' is not specified, gets all for the year.
#         """
#         if verbose: print('searching games...')
#         if year:
#             if verbose: print('    ','year:', year)
#
#             if season_ids:
#                 if verbose: print('    ','season_ids specified:')
#             else:
#                 seasons = self.find(sport,'season','schedule',{'season':year})
#                 for s in seasons:
#                     if s not in season_ids:
#                         season_ids.append( s.get('id') )
#
#             # print them for clarity
#             if verbose:
#                 for sid in season_ids:
#                     print('    ','    ... ', sid)
#
#             # only return games from the specified week, if the param is not None
#             target = {'season__id':{'$in':season_ids}}
#
#             if week:
#                 if verbose: print('    ','week:', week)
#                 # print('    ','')
#                 # get the season(s) objects for this week
#                 week_game_ids = []
#                 seasons = self.find(sport,'season', 'schedule',{'id':{'$in':season_ids}})
#
#                 # this looks complicated but its just very
#                 # specifically extracting a nested list
#                 # of gameid(s) -- as specified by the year, season, week --
#                 # and it puts those gameids into 'week_game_ids'
#                 for season in seasons:
#                     weeks_list = season.get('weeks', [])
#                     for week_json in weeks_list:
#                         game_list = week_json.get('week', {})
#                         if game_list.get('week',-1) != week:
#                             continue
#                         inner_games = game_list.get('games',[])
#                         if inner_games == []:
#                             # its possible its a single game
#                             week_game_ids.append( game_list.get('game') )
#                         else:
#                             for obj in inner_games:
#                                 gameid = obj.get('game', None)
#                                 if gameid not in week_game_ids:
#                                     week_game_ids.append( gameid )
#
#                 #print( 'target game ids:', str(week_game_ids))
#                 target = {'id':{'$in':week_game_ids}}
#
#             # get the games with the specified target query
#             if verbose: print( str(target) )
#             games = self.find(sport,'game','schedule',target)
#
#         else:
#             games = self.find(sport,'game','schedule') # gets all games in db
#
#         #
#         # build a msg to explain how many, and where we found games, its vvvvery (4 V's) useful most times
#         games_found_msg = '%s %s' % (str(games.count()), 'game(s) found by DataDen for:')
#         if year:
#             games_found_msg += '\n    year: %s'      % str(year)
#             if season_ids:
#                 games_found_msg += '\n    season_ids:'
#                 for season_id in season_ids:
#                     games_found_msg += '\n        - %s' % season_id
#             if week:
#                 games_found_msg += '\n    week: %s' % str(week)
#         else:
#             games_found_msg += ' all-time!'
#
#         print( games_found_msg )
#         return games
#
# class AbstractSeasonGames(DataDen):
#
#     def __init__(self, sport, year, schedule_collection, parent_api):
#         super().__init__()
#         self.sport                  = sport
#         self.year                   = year
#         self.schedule_collection    = schedule_collection
#         self.parent_api             = parent_api
#
#     def get_game_ids_regular_seaons(self):
#         raise Exception( 'child class must override get_game_ids_regular_season() to get the games for its sport' )
#
#     def get_game_ids(self, season_type=None):
#         """
#         get the games for this season
#
#         get the regular season games for the year if the season_type is not specified
#         :return:
#         """
#         raise Exception('child class must override get_game_ids() to get the games for its sport')
#
#     def get_seasons(self, target={}):
#         return self.find(self.sport, self.schedule_collection, self.parent_api, target=target )
#
# class NbaSeasonGames(AbstractSeasonGames):
#
#     SEASON_PRE = 'PRE'
#     SEASON_REG = 'REG'
#     SEASON_PST = 'PST'
#
#     def __init__(self, year):
#         super().__init__('nba', year, 'season_schedule', 'schedule')
#
#     def get_game_ids_regular_season(self):
#         return self.get_game_ids(season_type=self.SEASON_REG)
#
#     def get_game_ids(self, season_type):
#         # N2QyZGYyNWNpZDUyOWJlZDM0LTVhOGQtNDZkNC05ZWVmLTExNGJkMTM0MDg2Nw==",
#         # "id" : "529bed34-5a8d-46d4-9eef-114bd1340867",
#         # "type" : "PST",
#         # "year" : 2015,
#         # "parent_api__id" : "schedule",
#
#         target = {
#             'type' : season_type,
#             'year' : int(self.year),
#         }
#         seasons = self.get_seasons(target=target)
#         if seasons.count() != 1:
#             raise Exception('found more than 1 season object for %s/%s/%s!'%(self.sport,
#                                                             str(self.year), season_type))
#
#         game_ids = []
#         for s in seasons:
#             games_list = s.get('games__list')
#             for g in games_list:
#                 game_ids.append( g.get('game') )
#             break
#
#         print('%s game_ids' % (len(game_ids)))
#         return game_ids
#
# class NflSeasonGames(AbstractSeasonGames):
#
#     SEASON_PRE = 'PRE'
#     SEASON_REG = 'REG'
#     SEASON_PST = 'PST'
#
#     def __init__(self, year):
#         super().__init__('nfl', year, 'season', 'schedule')
#
#     def get_game_ids_regular_season(self):
#         return self.get_game_ids(season_type=self.SEASON_REG)
#
#     def get_game_ids(self, season_type):
#         # N2QyZGYyNWNpZDUyOWJlZDM0LTVhOGQtNDZkNC05ZWVmLTExNGJkMTM0MDg2Nw==",
#         # "id" : "529bed34-5a8d-46d4-9eef-114bd1340867",
#         # "type" : "PST",
#         # "year" : 2015,
#         # "parent_api__id" : "schedule",
#
#         target = {
#             'season' : int(self.year),
#             'type' : season_type,
#         }
#         seasons = self.get_seasons(target=target)
#         if seasons.count() != 1:
#             raise Exception('found more than 1 season object for %s/%s/%s!'%(self.sport,
#                                                             str(self.year), season_type))
#
#         game_ids = []
#         for s in seasons:
#             weeks = s.get('weeks')
#             for week_obj in weeks:
#                 inner_week = week_obj.get('week')
#                 week_number = inner_week.get('week')
#                 print( 'week_number:', str(week_number) )
#                 games = inner_week.get('games')
#                 for game in games:
#                     game_ids.append( game.get('game') )
#             break
#
#         print('%s game_ids' % (len(game_ids)))
#         return game_ids

class Season(DataDen):
    """
    Capable of getting the srids for the regular season games from dataden.

    Use the static factory(sport) method to get an instance of a season.

    usage:

        >>> season = Season.factory('nba')
        >>> reg_season_game_srids = season.get_game_ids_regular_season( 2015 )

    """

    # raised if a regular season not found for specified year
    class SeasonNotFoundException(Exception): pass

    # raised if multiple regular season objects for the specified year
    class MultipleSeasonObjectsReturnedException(Exception): pass

    # subclasses must override:
    sport = None

    # subclasses may override:
    schedule_collection = 'season_schedule'     #
    parent_api          = 'schedule'            #
    season_type_reg     = 'REG'                 #
    season_type_field   = 'type'                #
    season_year_field   = 'year'                #

    # Create based on class name:
    def factory(type):
        if type == "nba": return NbaSeason()
        if type == "nfl": return NflSeason()
        if type == "nhl": return NhlSeason()
        if type == "mlb": return MlbSeason()
        assert 0, "invalid Season: " + type
    factory = staticmethod(factory)

    def get_game_ids_regular_season(self, season):
        """
        the main reason to subclass Season is if you want
        a new sport and its regular season games are
        retrieved different than NBA/NHL (from DataDen)

        :param season: the season-year of the sport (ie: the year the season started in)
        :return:
        """

        seasons = self.get_seasons(season)
        self.validate_season(season, seasons) # make sure there is exactly 1 or raise exception
        # if num_season_objects == 0:
        #     raise self.SeasonNotFoundException('no seasons for %s' % title )
        #
        # if num_season_objects > 1:
        #     raise self.MultipleSeasonObjectsReturnedException('more than 1 season for %s' % title)

        game_ids = []
        games_list = seasons[0].get('games__list')
        for g in games_list:
            game_ids.append( g.get('game') )

        #print('... %s game_ids from the regular season' % (len(game_ids)))
        return game_ids

    def validate_season(self, year, seasons_found):
        """
        pass the response of the dataden find() to this after retrieving the seasons
        to make sure we have exactly 1 object -- if there are 0, or 2+ then raise exception.

        :param result:
        :return:
        """

        title = '%s/%s/%s' % (self.sport, str(year), self.season_type_reg)
        if seasons_found.count() == 0:
            raise self.SeasonNotFoundException('no seasons for %s' % title )

        if seasons_found.count() >= 2:
            for season_found in seasons_found:
                print('')
                print(str(season_found))
            raise self.MultipleSeasonObjectsReturnedException('more than 1 season for %s' % title)

    def get_seasons(self, season):
        """
        get the season objects that match the params.

        :param season: year that the season started in for the sport
        :param season_type: a value in ['PRE','REG','PST']
        :param target: override the target query to find the seasons more manually (specify year in here too)
        :return:
        """
        # default to this target query
        target = {
            self.season_type_field : self.season_type_reg,
            self.season_year_field : int(season),
        }

        return self.find(self.sport, self.schedule_collection, self.parent_api, target=target)

class NbaSeason(Season):

    sport = 'nba'

class NhlSeason(NbaSeason):

    sport = 'nhl'

class MlbSeason(Season):

    sport = 'mlb'

    parent_api          = 'schedule_reg'        # for mlb its part of the parent_api
    schedule_collection = 'season_schedule'
    season_type_field   = 'type'                # in the 'season_schedule' collection
    season_year_field   = 'year'                # in the 'season_schedule' collection

    def __get_game_srids(self, season_schedule_obj):
        """
        extract and return the game srids from this object

            "games__list": [
                {
                    "game": "0417b544-cb8b-4836-a035-5ed6d292bfe0"
                },
                ...

        :param season_schedule_obj:
        :return:
        """
        games_list = season_schedule_obj.get('games__list', [])
        return [ g.get('game') for g in games_list if 'game' in g.keys() ]

    def get_game_ids_regular_season(self, season):
        """
        overrides default behaviour to get the srids of the regular season games

        :param season:
        :return:
        """
        target = {
            self.season_type_field : self.season_type_reg,
            self.season_year_field : int(season),
        }
        seasons = self.find(self.sport, self.schedule_collection, self.parent_api, target=target)
        # a little error checking to ensure we have the object we want (and only 1 of them)
        self.validate_season(season, seasons)

        # build and return a list of game srids from the season object
        return self.__get_game_srids(seasons[0])

class NflSeason(Season):

    sport = 'nfl'

    schedule_collection = 'season'
    season_type_field   = 'type'                #
    season_year_field   = 'season'              #

    def get_game_ids_regular_season(self, season):
        """
        overrides default behavior to get regular season games

        :param season:
        :return:
        """

        seasons = self.get_seasons(season)
        # raises exception if its not exactly 1 object in a list
        self.validate_season(season, seasons)

        game_ids = []
        weeks = seasons[0].get('weeks')
        for week_obj in weeks:
            inner_week = week_obj.get('week')
            week_number = inner_week.get('week')
            #print( 'week_number:', str(week_number) )
            games = inner_week.get('games')
            for game in games:
                game_ids.append( game.get('game') )

        #print('%s game_ids' % (len(game_ids)))
        return game_ids

