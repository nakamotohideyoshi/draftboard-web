from __future__ import generators

import time
import xml.etree.ElementTree as ET

import requests
from django.conf import settings
from django.db import IntegrityError
from django.utils import timezone
from pymongo import MongoClient, DESCENDING

import dataden.cache.caches
import dataden.models
from util.slack import Webhook


class FeedTestWebhook(Webhook):
    # https://hooks.slack.com/services/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
    # identifier = 'T02S3E1FD/B3B1UL152/DvKjpIZf7ywKCgfq43MD8CmL' # #scheduler-logs
    identifier = 'T02S3E1FD/B3B1UL152/DvKjpIZf7ywKCgfq43MD8CmL'


class FeedTest(object):
    def __init__(self, game_srid, url, apikey):
        self.game_srid = game_srid
        self.url = url
        self.apikey = apikey
        self.session = requests.Session()
        self.r = None  # the HttpResponse from the last download()
        self.feed_model_class = dataden.models.PbpDebug
        self.et = None

        self.events = []

        # prepopulate the srids list with the ones we already have in the db
        self.srids = []
        for srid in self.feed_model_class.objects.filter(game_srid=self.game_srid):
            self.srids.append(srid)

        self.descriptions = []

        self.slack = FeedTestWebhook()

    def get_url(self):
        return '%s%s' % (self.url, self.apikey)

    def run(self, iterations=10, delay_ms=3000.0):
        print('%s iterations' % str(iterations))
        i = 1
        while i <= iterations:
            try:
                self.et = self.download()
                self.parse(self.et)
            except Exception as e:
                print(str(e))
                pass

            if i % 10 == 0:
                print('%s of %s' % (str(i), str(iterations)))
            time.sleep(float(
                float(delay_ms) / float(1000.0)))  # divide millis by 1000 to get values in seconds
            i += 1

    def download(self):
        """ download and return the ElementTree, after its initialized with the feed xml """
        self.r = self.session.get(self.get_url())
        return ET.fromstring(self.r.text)

    def parse(self, root):
        # parse the root node

        for node in root:
            if 'quarter' in node.tag:
                q = node.get('number')
                # print('quarter', node.get('number'))

                for events in node:
                    # if 'events' in events.tag:

                    for event in events:
                        # print( event.get('id'), event.get('clock') )

                        srid = event.get('id')
                        if srid in self.srids:
                            continue  # dont even both trying to go further

                        clock = str(event.get('clock'))
                        print(event.get('id'), clock)
                        self.events.append(event)
                        self.srids.append(srid)

                        desc = 'Q%s ' % str(q)
                        desc += clock + ' - '
                        for description in event:
                            if 'description' in description.tag:
                                desc = description.text
                                # print(desc)
                                self.descriptions.append(description)

                        self.add_to_db(srid=srid, description=desc, xml_str=None)

    def add_to_db(self, srid, description, xml_str=None):
        """
        returns True if this object was just created. (ie: the first time we parsed it).

        otherwise return False

        """
        xml_str = xml_str
        if xml_str is None:
            xml_str = ''

        # self.feed_model_class.objects.get(srid=srid, game_srid=game_srid)
        try:
            obj, created = self.feed_model_class.objects.get_or_create(
                url=self.url,
                game_srid=self.game_srid,
                srid=srid,
                description=description,
                xml_str=xml_str,
                delta_seconds_valid=True,
            )
        except IntegrityError:
            return False

        if created:
            print('new pbp:', str(description))
            self.slack.send('%s:' % str(timezone.now()) + ' ' + description)

        return created


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

    def create(db, collection, parent_api, enable=False):
        try:
            trig = dataden.models.Trigger.objects.get(db=db,
                                                      collection=collection, parent_api=parent_api)
        except dataden.models.Trigger.DoesNotExist:
            trig = dataden.models.Trigger()
            trig.db = db
            trig.collection = collection
            trig.parent_api = parent_api
            trig.enabled = enable
            trig.save()
        return Trigger(pk=trig.pk)

    create = staticmethod(create)


class DataDen(object):
    """
    caleb: im intending on this being the thru-point for rest_api calls
    """

    class InvalidTypeException(Exception):
        pass

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
            # print('connected to mongo')
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
        return self.client.get_database(db_name)

    def find(self, db, coll, parent_api, target={}, projection={}):
        """
        Perform a mongo find( target ) on the namespace and parent_api!

        'parent_api' is always added as a top level field of 'target' dictionary

        :return:
        """

        coll = self.db(db).get_collection(coll)
        target[self.PARENT_API__ID] = parent_api
        if projection and projection.keys():
            #
            # if the projection has any keys, use it
            return coll.find(filter=target, projection=projection,
                             no_cursor_timeout=self.no_cursor_timeout)

        # by default, dont apply projection
        return coll.find(filter=target, no_cursor_timeout=self.no_cursor_timeout)

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
            target[self.DD_UPDATED__ID] = {'$gte': ts_last_parse}
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
            walk_sports = [sport]
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
                    print('        ' + parent_api)
                    if examples:
                        ex = coll.find_one({self.PARENT_API__ID: parent_api})
                        print('            ' + str(ex))


class Season(DataDen):
    """
    Capable of getting the srids for the regular season games from dataden.

    Use the static factory(sport) method to get an instance of a season.

    usage:

        >>> season = Season.factory('nba')
        >>> reg_season_game_srids = season.get_game_ids_regular_season( 2015 )

    """

    # raised if a regular season not found for specified year
    class SeasonNotFoundException(Exception):
        pass

    # raised if multiple regular season objects for the specified year
    class MultipleSeasonObjectsReturnedException(Exception):
        pass

    # subclasses must override:
    sport = None

    # subclasses may override:
    schedule_collection = 'season_schedule'  #
    parent_api = 'schedule'  #
    season_type_reg = 'REG'  #
    season_type_field = 'type'  #
    season_year_field = 'year'  #

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
        self.validate_season(season, seasons)  # make sure there is exactly 1 or raise exception
        # if num_season_objects == 0:
        #     raise self.SeasonNotFoundException('no seasons for %s' % title )
        #
        # if num_season_objects > 1:
        #     raise self.MultipleSeasonObjectsReturnedException('more than 1 season for %s' % title)

        game_ids = []
        games_list = seasons[0].get('games__list')
        for g in games_list:
            game_ids.append(g.get('game'))

        # print('... %s game_ids from the regular season' % (len(game_ids)))
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
            err_msg = 'no seasons for %s' % title
            err_msg += '\n you may need to update /admin/sports/sitesport/ to the current season-year!'
            raise self.SeasonNotFoundException(err_msg)

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
            self.season_type_field: self.season_type_reg,
            self.season_year_field: int(season),
        }

        return self.find(self.sport, self.schedule_collection, self.parent_api, target=target)


class NbaSeason(Season):
    sport = 'nba'


class NhlSeason(NbaSeason):
    sport = 'nhl'


class MlbSeason(Season):
    sport = 'mlb'

    parent_api = 'schedule_reg'  # for mlb its part of the parent_api
    schedule_collection = 'season_schedule'
    season_type_field = 'type'  # in the 'season_schedule' collection
    season_year_field = 'year'  # in the 'season_schedule' collection

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
        return [g.get('game') for g in games_list if 'game' in g.keys()]

    def get_game_ids_regular_season(self, season):
        """
        overrides default behaviour to get the srids of the regular season games

        :param season:
        :return:
        """
        target = {
            self.season_type_field: self.season_type_reg,
            self.season_year_field: int(season),
        }
        seasons = self.find(self.sport, self.schedule_collection, self.parent_api, target=target)
        # a little error checking to ensure we have the object we want (and only 1 of them)
        self.validate_season(season, seasons)

        # build and return a list of game srids from the season object
        return self.__get_game_srids(seasons[0])


class NflSeason(Season):
    sport = 'nfl'

    schedule_collection = 'season'
    season_type_field = 'type'  #
    season_year_field = 'season'  #

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
            # print( 'week_number:', str(week_number) )
            games = inner_week.get('games')
            for game in games:
                game_ids.append(game.get('game'))

        # print('%s game_ids' % (len(game_ids)))
        return game_ids
