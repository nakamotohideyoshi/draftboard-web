#
# sports/sport/base_parser.py

import re
from django.core.cache import cache
from mysite.celery_app import locking
from django.utils import timezone
from dataden.util.timestamp import Parse as DataDenDatetime
from dataden.cache.caches import PlayByPlayCache, LiveStatsCache
from django.db.transaction import atomic
import json
from django.contrib.contenttypes.models import ContentType
from sports.models import SiteSport, Position
from dataden.classes import DataDen
import sports.classes
import dateutil.parser
import push.classes

#
################################################################################
#################### this will get the {player-srid} and the {game-srid}       #
################################################################################
# %cpaste
# import re
# import operator
# from ast import literal_eval
# f = open('site-setup/lillard_updates.txt', 'r')
# lines = f.readlines()
# f.close()
# items = []
# for line in lines:
#     d = literal_eval( line )
#     items.append( d )
# sorted_items = sorted(items, key=lambda k: k['ts']) # ascending
# len(sorted_items)
# for item in sorted_items:
#     if item.get('ns') == 'nba.player':
#         print(item.get('ts'), '>>>', item.get('o').get('statistics__list'))
#     elif item.get('ns') == 'nba.event':
#         print(item.get('ts'), '>>>', item.get('o').get('description'))
#         pattern = r"'player':\s'([^']*)'"
#         player_srids = re.findall(pattern, str(item))
#         for psrid in player_srids:
#             print('        player: ', psrid)
#         pattern_game = r"'game__id':\s'([^']*)'"
#         game_srids = re.findall(pattern_game, str(item))
#         for gsrid in game_srids:
#             print('        game:   ', gsrid)
# --
####################################################################################

class PatternFinder(object):

    def __init__(self, s):
        self.s = s

    def findall(self, pattern):
        return list(re.findall(pattern, self.s))

class SridFinder(PatternFinder):
    """
    has methods to find global ids from a dictionary.
    global ids are simply long strings of alpha-numeric
    character values of dict fields.
    """

    class InvalidArgumentTypeException(Exception): pass

    srid_pattern = r"'([^']*)'"    # will match anything between single quotes

    def __init__(self, data):
        if not isinstance(data, dict):
            err_msg = '"data" param must be a dict. type was: %s' % type(data)
            raise self.InvalidArgumentTypeException(err_msg)
        super().__init__(str(data))

    def get_for_field(self, fieldname):
        """
        return all the srids of fields (ie: dict keys) with this name.

        returns a list of string srids found
        """

        pattern = r"'%s':\s%s" % (fieldname, self.srid_pattern)
        return self.findall(pattern)

# class PbpStatsLinker(object):
#     """
#     this class is designed to extract the player-srid(s) and game-srid
#     from a play-by-play object (dictionary), and it uses pusher to
#     send a pbp object after it finds the corresponding PlayerStats to
#     send along with it.
#     """
#
#     def __init__(self, pbp):
#         """
#         construct this object with a play by play event object
#         which contains the description, players, teams, etc.
#         that are involved in a unique scoring play.
#         """
#         self.pbp = pbp
#
#     def get_data(self):
#         pass # TODO - implement?

class AbstractDataDenParser(object):
    """
    for parsing each individual sport, which will have some differences
    """
    def __init__(self):
        self.ns                 = None
        self.parent_api         = None
        self.o                  = None

    def add_pbp(self, obj):
        pbp_cache = PlayByPlayCache( self.ns.split('.')[0] ) # the self.ns is "sport.collection"
        pbp_obj = obj.get_o()
        pbp_cache.add( pbp_obj )

    def name(self):
        """
        helper method to get the class name of the instance, mainly for logging
        :return:
        """
        return self.__class__.__name__

    def unimplemented(self, ns, parent_api):
        print('')
        print('UNIMPLEMENTED <<< %s | %s >>> ... generally this means DataDen<Sport> .parse() just needs an addition to the switch statement.' % (ns,parent_api))

    def parse(self, obj, verbose=False):
        self.ns         = obj.get_ns()
        self.parent_api = obj.get_parent_api()
        self.target     = (self.ns, self.parent_api)
        self.o          = obj.get_o()

        if verbose:
            print ('%s.parse() | %s %s %s' % ( self.name(),
                   self.ns, self.parent_api, str(obj.get_o()) ) )

        # child parse() will execute here -- they must call super().parse( obj )
        # then this class will have setup self.ns and self.parent_api for them

class AbstractDataDenParseable(object):
    """
    Essentially provides an interface via the 'parse()' method,
    for parsing a specific object from dataden mongo db,
    specifically an object which has a namespace and a parent_api,
    such as: nba.player stats.
    """

    class DataDenParseableSendException(Exception): pass

    def __init__(self, wrapped=True):
        self.name           = self.__class__.__name__
        self.original_obj   = None
        self.o              = None
        self.wrapped        = wrapped
        self.srid_finder    = None

    def get_obj(self):
        return self.original_obj

        self.start = None
        self.stop = None

    def timer_start(self):
        self.start = timezone.now()

    def timer_stop(self):
        if self.start is None:
            return
        self.stop = timezone.now()
        print((self.stop - self.start).total_seconds(), 'sec to parse')


    def parse(self, obj, target=None):
        """
        Subclasses should call super().parse(obj,target) which
        will strip the oplog wrapper from the obj, and set
        the mongo object to self.o.
        """
        self.original_obj = obj
        #print( self.name, str(obj)[:100], 'target='+str(target) )
        if self.wrapped:
            self.o  = obj.get_o()
        else:
            self.o  = obj

        #
        # constrcut an SridFinder with the dictionary data
        #print('self.o -- ', str(self.o))        # TODO remove print
        self.srid_finder = SridFinder(self.o)

    def get_site_sport(self, obj):
        """
        Return the sport by splitting the mongo object's 'ns' on the dot
        and taking the leftmost part!

        As long as sports never have dots in their name we're fine.

        """
        #
        # get the sport name (ie: the db from where this obj came)
        sport_name = obj.get_ns().split('.')[0]

        #
        # if this excepts, i dont want to catch the exception
        # because i want it to crash.
        return SiteSport.objects.get( name=sport_name )

    def get_srids_for_field(self, fieldname):
        """
        returns a list of string "srids" (globally unique sportradar ids)

        using regular expressions, get the srids for the named field.
        for example: if fieldname is 'game__id', get every game srid found.
        """
        #print( fieldname, str(self.srid_finder.get_for_field(fieldname)))
        return self.srid_finder.get_for_field(fieldname)

    def send(self):
        """
        inheriting classes should override this method to send/pusher/signal
        the data after its been parsed.

        child classes may call this method in their implementation to
        validate that parse() has been called
        """
        if self.o is None:
            err_msg = 'call parse() before calling send()'
            raise self.DataDenParseableSendException(err_msg)

class DataDenSeasonSchedule(AbstractDataDenParseable):
    """
    parse a sports "season schedule" object. this is the object
    which contains an srid, year, and season-type for the sport.

    the year will be the calendar year the sport started in,
    and the season type will designate preseason/regular season/post / etc...
    """

    class ValidationException(Exception): pass # raised for bad field values during parse()

    season_types = ['pre','reg','pst']

    season_model = None # subclasses will need to set their own

    # default field names for extracting the values we want
    field_srid          = 'id'
    field_season_year   = 'year'
    field_season_type   = 'type'

    def __init__(self):
        if self.season_model is None:
            err_msg = '"season_model" class must be set'
            raise Exception(err_msg)

        # once parsed, the sports.<sports>.models.Season instance
        self.season = None

        super().__init__()

    def validate_srid(self, o):
        """ clean and return the srid value """
        val = o.get(self.field_srid, None)
        if not isinstance(val, str):
            err_msg = 'srid [%s] is not a string: %s' % (type(val), str(val))
            raise self.ValidationException(err_msg)
        return val

    def validate_season_year(self, o):
        """ clean and return the season_year value """
        val = o.get(self.field_season_year, None)
        if isinstance(val, float):
            val = int(val)
        if not isinstance(val, int):
            err_msg = 'season_year [%s] is not an integer: %s' % (type(val), str(val))
            raise self.ValidationException(err_msg)
        return val

    def validate_season_type(self, o):
        """ clean and return the season_type value """
        val = o.get(self.field_season_type, None)
        if not isinstance(val, str):
            err_msg = 'season_type [%s] is not a string: %s' % (type(val), str(val))
            raise self.ValidationException(err_msg)
        val = val.lower()
        if val not in self.season_types:
            err_msg = 'season_type [%s] not in acceptable ' \
                      'types %s. try overriding: season_types' % (val, self.season_types)
            raise self.ValidationException(err_msg)
        return val

    def parse(self, obj, target=None):
        """
        """
        super().parse( obj, target )

        # example:
        # {
        #   'parent_api__id': 'schedule',
        #   'year': 2015.0,
        #   'id': '529bed34-5a8d-46d4-9eef-114bd1340867',
        #   'type': 'PST',
        # }

        srid            = self.validate_srid(self.o)
        season_year     = self.validate_season_year(self.o)
        season_type     = self.validate_season_type(self.o)

        #print('season srid, season_year, season_type:', srid, season_year, season_type)
        try:
            self.season = self.season_model.objects.get( srid=srid, season_year=season_year, season_type=season_type )
        except self.season_model.DoesNotExist:
            self.season             = self.season_model()
            self.season.srid        = srid
            self.season.season_year = season_year
            self.season.season_type = season_type
            #self.season.save() # inheriting class must call save()

class DataDenTeamHierarchy(AbstractDataDenParseable):
    """
    Parse a team object form the hieraarchy feed (parent_api).

    From dataden/mongo, parse the <sport>.team namespace for the parent_api: 'hierarchy',
    ie: parse a team from the the sport.

    this class should work as-is for nba and nhl,
    but you may need to override some things for other sports
    """

    team_model = None

    def __init__(self):
        if self.team_model is None:
            raise Exception('"team_model" cant be None')

        self.team = None

        super().__init__()

    def parse(self, obj, target=None):
        super().parse( obj, target )

        # db.team.findOne({'parent_api__id':'hierarchy'})
        # {
        #     "_id" : "cGFyZW50X2FwaV9faWRoaWVyYXJjaHlsZWFndWVfX2lkNDM1MzEzOGQtNGMyMi00Mzk2LTk1ZDgtNWY1ODdkMmRmMjVjY29uZmVyZW5jZV9faWQzOTYwY2ZhYy03MzYxLTRiMzAtYmMyNS04ZDM5M2RlNmY2MmZkaXZpc2lvbl9faWQ1NGRjNzM0OC1jMWQyLTQwZDgtODhiMy1jNGMwMTM4ZTA4NWRpZDU4M2VjZWE2LWZiNDYtMTFlMS04MmNiLWY0Y2U0Njg0ZWE0Yw==",
        #     "alias" : "MIA",
        #     "id" : "583ecea6-fb46-11e1-82cb-f4ce4684ea4c",
        #     "market" : "Miami",
        #     "name" : "Heat",
        #     "parent_api__id" : "hierarchy",
        #     "dd_updated__id" : NumberLong("1431472829579"),
        #     "league__id" : "4353138d-4c22-4396-95d8-5f587d2df25c",
        #     "conference__id" : "3960cfac-7361-4b30-bc25-8d393de6f62f",
        #     "division__id" : "54dc7348-c1d2-40d8-88b3-c4c0138e085d",
        #     "venue" : "b67d5f09-28b2-5bc6-9097-af312007d2f4"
        #   }

        o = self.o

        srid            = o.get('id',               None)
        srid_league     = o.get('league__id',       None)
        srid_conference = o.get('conference__id',   None)
        srid_division   = o.get('division__id',     None)
        market          = o.get('market',           None)
        name            = o.get('name',             None)
        alias           = o.get('alias',            None)
        srid_venue      = o.get('venue',            '')

        try:
            self.team = self.team_model.objects.get( srid=srid )
        except self.team_model.DoesNotExist:
            self.team = self.team_model()
            self.team.srid      = srid

        self.team.srid_league       = srid_league
        self.team.srid_conference   = srid_conference
        self.team.srid_division     = srid_division
        self.team.market            = market
        self.team.name              = name
        self.team.alias             = alias
        self.team.srid_venue        = srid_venue
        # NOTE:
        # save() is NOT called here on purpose!
        # subclasses should must call super().parse(obj),
        # then make any applicable changes and save

class DataDenGameSchedule(AbstractDataDenParseable):
    """
    Requires: the game_model & team_model to be set by inheriting classes

    Parses a game objects into the database with parse()

    this class should not need much modification for nba & nhl, but it will for other sports.
    """
    team_model      = None
    game_model      = None
    season_model    = None

    field_season_srid = 'season_schedule__id'

    def __init__(self):
        if self.team_model is None:
            raise Exception('"team_model cant be None!')
        if self.game_model is None:
            raise Exception('"game_model" cant be None!')
        if self.season_model is None:
            raise Exception('"season_model" cant be None!')

        self.game = None

        # mlb has the same srid for all three season_types,
        # so we have to hack this just a bit to
        # use the self.season if its already set. default is None
        self.season = None

        super().__init__()

    def parse(self, obj, target=None):
        super().parse( obj, target )

        o = self.o

        srid        = o.get('id')
        start_str   = o.get('scheduled')
        start       = DataDenDatetime.from_string( start_str )
        status      = o.get('status')

        srid_season = o.get(self.field_season_srid)
        srid_home   = o.get('home')
        srid_away   = o.get('away')
        title       = o.get('title', '')

        if self.season is None:
            # i guess the previous class didnt set it
            try:
                self.season = self.season_model.objects.get(srid=srid_season)
            except self.season_model.DoesNotExist:
                return

        try:
            h = self.team_model.objects.get(srid=srid_home)
        except self.team_model.DoesNotExist:
            #print( str(o) )
            #print( 'Team (home) for Game DoesNotExist! Have you parsed the "hierarchy" feed recently?')
            return

        try:
            a = self.team_model.objects.get(srid=srid_away)
        except self.team_model.DoesNotExist:
            #print( str(o) )
            #print( 'Team (away) for Game DoesNotExist! Have you parsed the "hierarchy" feed recently?')
            return

        try:
            self.game = self.game_model.objects.get(srid=srid)
        except self.game_model.DoesNotExist:
            self.game = self.game_model()
            self.game.srid = srid

        self.game.season    = self.season
        self.game.home      = h
        self.game.away      = a
        self.game.start     = start
        self.game.status    = status
        self.game.srid_home = srid_home
        self.game.srid_away = srid_away
        self.game.title     = title
        # child class must save the self.game !

class DataDenPlayerRosters(AbstractDataDenParseable):

    team_model      = None
    player_model    = None

    def __init__(self):
        if self.team_model is None:
            raise Exception('"team_model" cant be None!')
        if self.player_model is None:
            raise Exception('"player_model" cant be None!')

        self.position_key = 'primary_position'
        self.player = None

        super().__init__()

    def parse(self, obj, target=None):
        super().parse( obj, target )

        o = self.o

        srid        = o.get('id')
        srid_team   = o.get('team__id')

        first_name  = o.get('first_name')
        last_name   = o.get('last_name')

        birth_place = o.get('birth_place', '')
        birthdate   = o.get('birthdate', '')
        experience  = o.get('experience', 0.0)
        try:
            experience = float( experience )
        except ValueError:
            experience = 0.0

        height              = o.get('height', 0.0)      # inches
        weight              = o.get('weight', 0.0)      # lbs.
        jersey_number       = o.get('jersey_number', 0.0)

        position_name       = o.get(self.position_key, None) # nfl will want to override this
        if position_name is None:
            raise Exception('"%s" was None! cannot create player if their position is invalid!'%self.position_key)

        #primary_position    = o.get('primary_position')

        status              = o.get('status')   # roster status, ie: basically whether they are on it

        #
        # get the team - if it doesnt exist, return,
        # because if the team doesnt exist, we dont
        # want to create a player if they cant have a team
        try:
            t = self.team_model.objects.get(srid=srid_team)
        except self.team_model.DoesNotExist:
            #print( str(o) )
            #print( 'Team for Player DoesNotExist!')
            return

        #
        # determine the players sport, and then get or create their Position
        site_sport = self.get_site_sport(obj)
        try:
            position = Position.objects.get(site_sport=site_sport, name=position_name)
        except Position.DoesNotExist:
            position = Position()
            position.site_sport = site_sport
            position.name       = position_name
            position.save()

        #
        # get or create the player
        try:
            self.player = self.player_model.objects.get(srid=srid)
        except self.player_model.DoesNotExist:
            self.player = self.player_model()
            self.player.srid = srid

        self.player.team                = t             # team could easily change of course
        self.player.first_name          = first_name
        self.player.last_name           = last_name

        self.player.birth_place         = birth_place
        self.player.birthdate           = birthdate
        self.player.experience          = experience
        self.player.height              = height
        self.player.weight              = weight
        self.player.jersey_number       = jersey_number
        self.player.position            = position
        self.player.status              = status

        # self.player.save() is done in inheriting class!

class DataDenPlayerStats(AbstractDataDenParseable):

    game_model          = None
    player_model        = None
    player_stats_model  = None

    def __init__(self):
        if self.game_model is None:
            raise Exception('"game_model" cant be None!')
        if self.player_model is None:
            raise Exception('"player_model" cant be None!')
        if self.player_stats_model is None:
            raise Exception('"player_stats_model" cant be None!')

        self.position_key = 'primary_position' # NFL will need to override this!

        self.p  = None  # the Player associated with the player stats
        self.ps = None  # this will hold the PlayerStats object

        super().__init__()

    def parse(self, obj, target=None):
        """
        get or create the game player and set it to self.ps

        sub-classes must take care of settings the actual per-sport stats!

        :param obj:
        :param target:
        :return:
        """
        super().parse( obj, target )

        o = obj.get_o()
        srid_game   = o.get('game__id', None)
        srid_player = o.get('id', None)

        try:
            self.p = self.player_model.objects.get(srid=srid_player)
        except self.player_model.DoesNotExist:
            # first_name  = o.get('first_name', None)
            # last_name   = o.get('last_name', None)
            # full_name   = '%s %s' % (str(first_name), str(last_name))
            #print( str(o) )
            #print('Player object for PlayerStats DoesNotExist')
            return # dont create the playerstats then

        try:
            self.g = self.game_model.objects.get(srid=srid_game)
        except self.game_model.DoesNotExist:
            #print( str(o) )
            #print('Game object for PlayerStats DoesNotExist')
            return # dont create the playerstats then

        try:
            self.ps = self.player_stats_model.objects.get( srid_game=srid_game, srid_player=srid_player )
        except self.player_stats_model.DoesNotExist:
            self.ps = self.player_stats_model()
            self.ps.srid_game    = srid_game
            self.ps.srid_player  = srid_player
            self.ps.player  = self.p
            self.ps.game    = self.g
            #
            # #
            # # only setup the position inside "except" so that we dont perform extra
            # # queries after it has been created. because we really only care the first time.
            # site_sport      = self.get_site_sport(obj)
            # position_name   = self.o.get(self.position_key, None)
            # if position_name is None:
            #     raise Exception('"%s" value is None -- cant determine player position!'%self.position_key)
            # try:
            #     position = Position.objects.get(name=position_name)
            # except Position.DoesNotExist:
            #     position = Position()
            #     position.name = position_name
            #     position.save()
            #
            # #
            # # set it but it wont be saved until child performs save()
            self.ps.position = self.p.position

class DataDenGameBoxscores(AbstractDataDenParseable):

    gameboxscore_model  = None
    team_model          = None

    def __init__(self):
        if self.gameboxscore_model is None:
            raise Exception('"gameboxscore_model" cant be None!')
        if self.team_model is None:
            raise Exception('"team_model" cant be None!')

        self.boxscore = None

        self.HOME = 'home_team'
        self.AWAY = 'away_team'

        super().__init__()

    def parse(self, obj, target=None):
        super().parse( obj, target )

        # db.game.findOne({'parent_api__id':'boxscores','status':'inprogress'})
        # {
        #     "_id" : "cGFyZW50X2FwaV9faWRib3hzY29yZXNpZGMzNGMwZDRjLWU1ZGQtNDMzOS04YjIyLWZhZWUyOWEzZDFhMQ==",
        #     "away_team" : "4417d3cb-0f24-11e2-8525-18a905767e44",
        #     "clock" : "14:22",
        #     "coverage" : "full",
        #     "home_team" : "441781b9-0f24-11e2-8525-18a905767e44",
        #     "id" : "c34c0d4c-e5dd-4339-8b22-faee29a3d1a1",
        #     "period" : 1,
        #     "scheduled" : "2015-05-19T00:00:00+00:00",
        #     "start_time" : "2015-05-19T00:15:00+00:00",
        #     "status" : "inprogress",
        #     "title" : "Game 2",
        #     "xmlns" : "http://feed.elasticstats.com/schema/hockey/game-v2.0.xsd",
        #     "parent_api__id" : "boxscores",
        #     "dd_updated__id" : NumberLong("1431995308494"),
        #     "teams" : [
        #         {
        #             "team" : "441781b9-0f24-11e2-8525-18a905767e44"
        #         },
        #         {
        #             "team" : "4417d3cb-0f24-11e2-8525-18a905767e44"
        #         }
        #     ]
        # }

        o = obj.get_o()
        srid_game   = o.get('id', None)
        srid_home   = o.get(self.HOME, None)
        srid_away   = o.get(self.AWAY, None)

        try:
            h = self.team_model.objects.get( srid=srid_home )
        except self.team_model.DoesNotExist:
            #print( str(o) )
            #print( 'Team (home_team) does not exist for srid so not creating GameBoxscore')
            return

        try:
            a = self.team_model.objects.get( srid=srid_away )
        except self.team_model.DoesNotExist:
            #print( str(o) )
            #print( 'Team (away_team) does not exist for srid so not creating GameBoxscore')
            return

        try:
            self.boxscore = self.gameboxscore_model.objects.get(srid_game=srid_game)
        except self.gameboxscore_model.DoesNotExist:
            self.boxscore = self.gameboxscore_model()
            self.boxscore.srid_game = srid_game

        self.boxscore.srid_home  = srid_home
        self.boxscore.home       = h
        self.boxscore.away       = a
        self.boxscore.srid_away  = srid_away

        self.boxscore.clock      = o.get('clock', '' )
        self.boxscore.coverage   = o.get('coverage', '')
        self.boxscore.status     = o.get('status', '')
        self.boxscore.title      = o.get('title', '')

class DataDenTeamBoxscores(AbstractDataDenParseable):

    gameboxscore_model  = None

    def __init__(self):
        if self.gameboxscore_model is None:
            raise Exception('"gameboxscore_model" cant be None!')

        self.boxscore = None

        self.POINTS = 'points' # default field name where points are found

        super().__init__()

    def parse(self, obj, target=None):
        # db.team.findOne({'game__id':'c34c0d4c-e5dd-4339-8b22-faee29a3d1a1','parent_api__id':'boxscores'})
        # {
        #     "_id" : "cGFyZW50X2FwaV9faWRib3hzY29yZXNnYW1lX19pZGMzNGMwZDRjLWU1ZGQtNDMzOS04YjIyLWZhZWUyOWEzZDFhMWlkNDQxN2QzY2ItMGYyNC0xMWUyLTg1MjUtMThhOTA1NzY3ZTQ0",
        #     "id" : "4417d3cb-0f24-11e2-8525-18a905767e44",
        #     "market" : "Tampa Bay",
        #     "name" : "Lightning",
        #     "points" : 6,
        #     "parent_api__id" : "boxscores",
        #     "dd_updated__id" : NumberLong("1432004309403"),
        #     "game__id" : "c34c0d4c-e5dd-4339-8b22-faee29a3d1a1",
        #     "scoring__list" : [
        #         {
        #             "period" : {
        #                 "number" : 1,
        #                 "points" : 2,
        #                 "sequence" : 1
        #             }
        #         },
        #         {
        #             "period" : {
        #                 "number" : 2,
        #                 "points" : 1,
        #                 "sequence" : 2
        #             }
        #         },
        #         {
        #             "period" : {
        #                 "number" : 3,
        #                 "points" : 3,
        #                 "sequence" : 3
        #             }
        #         }
        #     ],
        super().parse( obj, target )

        o = obj.get_o()
        srid_game   = o.get('game__id', None)
        srid_team   = o.get('id', None)

        try:
            self.boxscore = self.gameboxscore_model.objects.get(srid_game=srid_game)
        except self.gameboxscore_model.DoesNotExist:
            # it hasnt been created yet, but only create it in GameBoxscores.
            return

        if self.boxscore.srid_home == srid_team:
            self.boxscore.home_score        = o.get('points', 0)
            self.boxscore.home_scoring_json = json.loads( json.dumps(o.get('scoring__list', [])))
            self.boxscore.save()

        elif self.boxscore.srid_away == srid_team:
            self.boxscore.away_score        = o.get('points', 0)
            self.boxscore.away_scoring_json = json.loads( json.dumps(o.get('scoring__list', [])))
            self.boxscore.save()

        else:
            # this team differs from the teams on this boxscore !
            self.boxscore = None
            #print( str(o) )
            #print( 'The team[%s] doesnt match home or away team!')
            return

class DataDenPbpDescription(AbstractDataDenParseable):
    """
    Parses the pbp text description objects.
    """

    class SridGameNotFoundException(Exception): pass

    class SridGameMultipleSridsFoundException(Exception): pass

    game_model              = None # fields: srid
    portion_model           = None #
    pbp_model               = None
    pbp_description_model   = None
    #
    player_stats_model      = None # ie: sports.<sport>.models.PlayerStats
    pusher_sport_pbp        = None # ie: push.classes.PUSHER_NBA_PBP
    pusher_sport_stats      = None # ie: push.classes.PUSHER_NBA_STATS

    def __init__(self):
        if self.game_model is None:
            raise Exception('"game_model" cant be None!')
        if self.pbp_model is None:
            raise Exception('"pbp_model" cant be None!')
        if self.pbp_description_model is None:
            raise Exception('"pbp_description_model" cant be None!')

        self.KEY_GAME_ID = 'id'

        self.game           = None
        self.game_ctype     = None # set if self.game is set

        self.pbp            = None
        self.pbp_ctype      = None # set if self.pbp is set

        self.live_stats_cache = LiveStatsCache()

        super().__init__()

    def __get_content_type(self, model):
        """
        Helper for ContentType.objects.get_for_model(model)

        :param model:
        :return:
        """
        return ContentType.objects.get_for_model(model)

    def get_game_portion(self, category, sequence, save=True):
        """
        Get or create the GamePortion for this PbpDescription.
        The GamePortion is the inning_half(mlb), quarter(nba/nfl), or period(nhl)
        that the PbpDescription is associated with.

        :param category:
        :param sequence:
        :return:
        """
        try:
            #
            # GamePortions are unique based on their srid_game, category, & sequence!
            portion = self.portion_model.objects.get(game_type__pk=self.game_ctype.id,
                                game_id=self.game.id, sequence=sequence )
        except self.portion_model.DoesNotExist:
            portion = self.portion_model()
            portion.srid_game          = self.game.srid
            portion.game               = self.game
            portion.sequence           = sequence
            portion.category           = category # pulling this out will allow us to change the category
            if save:
                portion.save()
        return portion

    def get_game_portion_by_srid(self, srid):
        try:
            portion = self.portion_model.objects.get(srid=srid)
        except self.portion_model.DoesNotExist:
            portion = None
        return portion

    def get_pbp_description(self, portion, idx, description, save=True):
        """
        Get or create the PbpDescription for the GamePortion,
        and the Pbp object this pbp is associated with.

        Caller should set the idx, and the text description.

        :param portion:
        :return:
        """
        portion_ctype = self.__get_content_type(portion)
        try:
            #
            # GamePortions are unique based on their srid_game, category, & sequence!
            desc = self.pbp_description_model.objects.get( idx=idx,
                                portion_type__pk=portion_ctype.id, portion_id=portion.id,
                                pbp_type__pk=self.pbp_ctype.id, pbp_id=self.pbp.id )
        except self.pbp_description_model.DoesNotExist:
            desc = self.pbp_description_model()
            desc.pbp         = self.pbp
            desc.portion     = portion
            desc.idx         = idx

        if desc.description != description:
            #print( '>>>>> setting description to:"%s"' % description)
            desc.description = description
            if save:
                desc.save()
        return desc

    def get_pbp_description_by_srid(self, srid):
        try:
            #print( 'pbp_description_model:', str(self.pbp_description_model), 'srid:', srid )
            pbp_desc = self.pbp_description_model.objects.get(srid=srid)
            #print( '... got it:', str(pbp_desc), 'pk:', str(pbp_desc.pk))
        except self.pbp_description_model.DoesNotExist:
            #print( '... does not exist!')
            pbp_desc = None
        return pbp_desc

    def parse(self, obj, target=None):
        """
        For the given obj:
        a) set self.game to the game the pbp data is from
        b) get or create the self.pbp that points to game for the pbp
        c) determine which GamePortion this pbp is specifically for
        d) create/update the pbp description

        :param obj:
        :param target:
        :return:
        """
        super().parse( obj, target )

        #
        # get the Game and set it to self.game
        srid_game = self.o.get(self.KEY_GAME_ID, None)
        try:
            self.game = self.game_model.objects.get(srid=srid_game)
        except self.game_model.DoesNotExist:
            #print( str(self.o) )
            #print( 'Game for pbp does not exist' )
            return
        self.game_ctype = self.__get_content_type(self.game)

        #
        # get the Pbp model, and set it to self.pbp for subclasses to use
        try:
            self.pbp = self.pbp_model.objects.get(srid_game=srid_game)
        except self.pbp_model.DoesNotExist:
            self.pbp = self.pbp_model()
            self.pbp.srid_game  = srid_game
            self.pbp.game       = self.game
            self.pbp.save() # create it
        self.pbp_ctype = self.__get_content_type(self.pbp)

        #
        # from here the child class may need to use:
        #   self.get_game_portion()
        #   self.get_pbp_description()

    def add_to_cache(self, obj):
        """
        adds the pbp obj to the cache.

        :return: True if object was just added. else returns False
        """
        return self.live_stats_cache.update_pbp( self.get_obj() )

    def send(self):
        """
        pusher the pbp + stats info as one piece of data.
        :return:
        """
        super().send()

        if not self.add_to_cache(self.get_obj()):
            return  # return out of method - we dont need to send this obj again

        #
        # try to retrieve the player(s) and game srids to look up linked PlayerStats
        # and add them to the player_stats list if found.
        player_stats = self.find_player_stats()

        #
        # send normally, or as linked data depending on the found PlayerStats instances
        if len(player_stats) == 0:
            # solely push pbp object
            push.classes.DataDenPush( self.pusher_sport_pbp, 'event' ).send( self.o )
        else:
            # push combined pbp+stats data

            # delete the cache_token (if they exist) for each player_stats pushered
            # so if there are any pending/countdown tasks which havent fired yet, they
            # will effectively be cancelled (ie: eliminate the double-send or late stats update).
            self.delete_cache_tokens(player_stats)
            data = self.build_linked_pbp_stats_data( player_stats )
            push.classes.DataDenPush( self.pusher_sport_pbp, 'linked' ).send( data )

    def delete_cache_tokens(self, player_stats_objects):
        for player_stats in player_stats_objects:
            cache.delete(player_stats.get_cache_token())

    def get_srid_game(self, fieldname):
        """
        we should expect to find only 1 game srid
        :return:
        """
        game_srids = list(set(self.get_srids_for_field(fieldname)))
        if len(game_srids) < 1:
            raise self.SridGameNotFoundException(str(self.o))
        elif len(game_srids) > 1:
            raise self.SridGameMultipleSridsFoundException(str(self.o))
        return game_srids[0]

    def find_player_stats(self):
        """
        extract player and game srids and return a list
        of any matching PlayerStats models found
        :return:
        """

        game_srid       = self.get_srid_game('game__id')

        # we may find any number of player srids - including 0
        player_srids    = self.get_srids_for_field('player')

        return self.player_stats_model.objects.filter(srid_game=game_srid,
                                                    srid_player__in=player_srids)

    def build_linked_pbp_stats_data(self, player_stats):
        """
        builds and returns a dictionary in the form:

            {
                "nba_pbp"   : { <typical nba_pbp pusher formatted data> },
                "nba_stats" : [
                    { <PlayerStats pusher formatted data> },
                    { <PlayerStats pusher formatted data> },
                ],
            }

        """
        data = {
            self.pusher_sport_pbp   : self.o,
            self.pusher_sport_stats : [ ps.to_json() for ps in player_stats ]
        }
        return data

class DataDenInjury(AbstractDataDenParseable):
    """
    Ensures the player associated with the injury exists, and sets
    up both objects for subclasses.
    """

    player_model    = None
    injury_model    = None

    key_iid    = '' # 'id' # for nba/nhl - other sports will want to override this

    def __init__(self, wrapped=True):
        if self.player_model is None:
            raise Exception('"player_model" cant be None!')
        if self.injury_model is None:
            raise Exception('"injury_model" cant be None!')
        if self.key_iid == '':
            raise Exception('"key_iid" must be set to the name of the specal injury "iid" field')

        self.srid_player_key = 'player__id'

        self.player         = None # the player associated with the injury
        self.player_ctype   = None
        self.injury         = None
        self.parse_called   = False # flipped True if parse() method has been called

        super().__init__(wrapped) # validates to ensure the subclass set the models properly

    def get_player(self):
        """
        Throws exception if called before parse() is called.

        Returns the sports.model.Player instance associated with the injury.

        May return None if player was not found.

        :return:
        """
        if not self.parse_called:
            raise Exception('parse() has not been called yet.')
        return self.player

    def parse(self, obj, target=None):
        """
        Setup self.player and self.injury, but does NOT call save() on self.injury.
        Subclass must make any additional edits and save() the instance if necessary!

        :param obj:
        :param target:
        :return:
        """
        super().parse( obj, target )
        self.parse_called = True

        srid_player = self.o.get(self.srid_player_key, None)
        try:
            self.player = self.player_model.objects.get(srid=srid_player)
        except self.player_model.DoesNotExist:
            #print( str(self.o) )
            #print( 'Player (%s) for injury does not exist'%srid_player)
            return

        self.player_ctype = ContentType.objects.get_for_model(self.player)

        iid = self.o.get(self.key_iid, None)
        ddtimestamp = self.o.get('dd_updated__id')
        #print( str(ddtimestamp) )
        try:
            self.injury = self.injury_model.objects.get(iid=iid) #,
                                # player_type__pk=self.player_ctype.id,
                                # player_id=self.player.id )
        except self.injury_model.DoesNotExist:
            self.injury = self.injury_model()
            self.injury.iid     = iid
            self.injury.ddtimestamp = ddtimestamp

        self.injury.player      = self.player

        # subclass will need to perform the save() to create/update !
#
# class ContentItemDb:
#     """
#     helper class to keep track of the model instances we have created
#
#     """
#
#     class Item
#
#     def __init__(self, tsxcontent):
#         self.tsxcontent     = tsxcontent
#         self.tsxitem_list   = []
#
#     def add_item(self, tsxitem):
#         # initialize the item list if necessary
#         if self.tsxitem_list is None:
#             self.tsxitem_list = []
#
#         # save the reference to the tsxcontent instance
#         tsxitem.tsxcontent = self.tsxcontent
#
#         # hold on to it
#         self.tsxitem_list.append( tsxitem )

class TsxContentParser(AbstractDataDenParseable):
    """
    Parses The Sports Xchange news, injuries, and transactions
    from dataden objects into site models.

    This is the base class for The Sports Xchange content
    parsed from DataDen, ie: SportRadar.us

    Details:

        objects are content news items from tsx from 3 categories:
              a) news
              b) injury
              c) transaction

        here are the 2 properties that, in combination,
        categorize the news items into one of the
        three categories (news, injury, or transaction):
              A) 'injury'
              B) 'transaction'

        the values determine the type of content object
        we create in our own database:
              1) 'injury' == True                             --> indicates injury content
              2) 'transaction' == True                        --> indicates transaction content (like a trade)
              3) 'injury' == False && 'transaction' == False  --> indicates general news content

    """

    class ContentObjectSportDoesNotMatchException(Exception): pass

    # node property value
    TRUE_VALUES     = ['true']
    FALSE_VALUES    = ['false']

    def __init__(self, sport):
        super().__init__()  # super().__init__(wrapped=True) # wrapped defaults to True

        # we will need to be able to query DataDen/mongo
        self.dd                     = DataDen()

        # set the sport internally, and get the SiteSportManager
        self.sport                  = sport
        self.site_sport_manager     = sports.classes.SiteSportManager()
        self.site_sport             = self.site_sport_manager.get_site_sport(self.sport)
        self.sport_player_class     = self.site_sport_manager.get_player_class(self.site_sport)

        # the sports.sport.models.TsxContent model does not get inherited
        self.content_model_class    = sports.models.TsxContent

        # content model classes
        self.news_model_class       = self.site_sport_manager.get_tsxnews_class(self.sport)
        self.injury_model_class     = self.site_sport_manager.get_tsxinjury_class(self.sport)
        self.transaction_model_class = self.site_sport_manager.get_tsxtransaction_class(self.sport)

        # content reference model classes (things that point to content)
        self.team_model_class       = self.site_sport_manager.get_tsxteam_class(self.sport)
        self.player_model_class     = self.site_sport_manager.get_tsxplayer_class(self.sport)

    def parse(self, content_obj, target=None, verbose=False):
        """

        :param obj: the content object
        :param target: defaults to None. Can be a tuple in the form:
                        ('sport.collection', 'parent_api')
        :return: a 3-tuple in the form:    ( tsxcontent, tsxitems, tsxrefs )
                    'tsxcontest' the the model instance for the content
                    'tsxitems' is a list of every TsxItem (... ie TsxNews, TsxInjury, or TsxTransaction objects)
                    'tsxrefs' is a list of every TsxTeam or TsxPlayer for each TsxItem
        """

        #
        # sets self.o internally
        super().parse( content_obj, target )

        #
        # validity check to make sure were using
        # the right sport model classes for the content object
        if self.sport != self.o.get('sport'):
            err_msg = 'self.sport: %s  !=  self.o.get("sport"): %s' % (self.sport, str(self.o.get('sport')))
            raise self.ContentObjectSportDoesNotMatchException(err_msg)

        #
        # save the TsxContent object in the db (uses self.o for the data)
        tsxcontent, c  = self.get_or_create_tsxcontent()        # subsequent methods require the TsxContent be built first
        if verbose: print(str(tsxcontent))
        tsxitems    = self.update_tsxitems( tsxcontent )        # update its items

        #
        # return the created and/or update models in a 3-tuple!
        return (tsxcontent, tsxitems)

    def get_or_create_tsxcontent(self):
        #
        # get or create the TsxContent model instance
        #print(str(self.o))
        srid = self.o.get('id')
        content_model, c = self.content_model_class.objects.get_or_create(sport=self.sport, srid=srid)
        return content_model, c

    def update_tsxitems(self, tsxcontent):
        #
        # get all the content items associated with this content object
        content_items = self.dd.find(self.sport, 'item', 'content', {'content__id':tsxcontent.srid})

        # parse all the content items for the tsxcontent
        tsxitem_list = []
        for item_obj in content_items:
            tsxitem = self.parse_item( tsxcontent, item_obj )
            tsxitem_list.append( tsxitem )
        return tsxitem_list

    def parse_item(self, tsxcontent, item_obj):
        """
        Parse a tsx item from dataden into its respective TsxContent parts

        Example item_obj:

            {'injury': 'false',
             'transaction': 'true',
             'refs__list': {
                'ref__list': {
                    'type': 'organization',
                    'sportsdata_id': '583ec928-fb46-11e1-82cb-f4ce4684ea4c',
                    'name': 'Detroit Pistons'
                }
             },
             'dd_updated__id': 1450237938758,
             'type': 'news',
             'byline': 'The Sports Xchange',
             'dateline': '12/14/2015',
             'updated': '2015-12-15T01:19:43+00:00',
             'content__id': 'http://api.sportsdatallc.org/content-nba-t3/tsx/news/2015/12/15/all.xml',
             'parent_api__id': 'content',
             'id': 'a3fd181c-5a98-48c7-9d02-061c7ec672f6',
             'credit': 'The Sports Xchange',
             'title': 'NBA Note - Detroit Pistons Dinwiddie, Spencer',
             'content__list': {
                'long': "G Spencer Dinwiddie was recalled from the Grand Rapids Drive of the NBA Development League. Dinwiddie has played in nine games for Detroit this season, averaging 4.4 points, 1.0 rebounds and 1.4 assists in 12.3 minutes per game. Dinwiddie had seven points with three rebounds and two assists in Sunday's game for Grand Rapids."
             },
             'provider__list': {
                'provider_content_id': '001426155',
                'original_publish': '2015-12-14T17:02:09+00:00',
                'name': 'tsx'
             },
             'created': '2015-12-15T01:19:42+00:00'
            }

        :param item_obj:
        :return: a new/updated TsxItem instance
        """
        #
        # either going to be news, injury, or transaction
        is_injury      = item_obj.get('injury') in self.TRUE_VALUES
        is_transaction = item_obj.get('transaction') in self.TRUE_VALUES

        if is_injury:
            #
            # highest precedence.
            # anything flagged injury, we strictly consider injury related
            # even if it has any other flags
            self.__parse_item_for_class(tsxcontent, item_obj, self.injury_model_class)

        elif is_transaction:
            #
            # anything flagged as a transaction
            self.__parse_item_for_class(tsxcontent, item_obj, self.transaction_model_class)

        else:
            #
            # the most common item type, news is anything thats
            # not flagged as something more specific
            self.__parse_item_for_class(tsxcontent, item_obj, self.news_model_class)

    def __parse_datetime(self, datetime_str):
        """
        use pythons dateutil module to parse a string and return the datetime object

        :param datetime_str:
        :return:
        """
        return dateutil.parser.parse(datetime_str)

    @atomic
    def __parse_item_for_class(self, tsxcontent, item_obj, tsx_item_model_class):
        """
        parse an item object for the given TsxContent object using the item class.

        :param tsxcontent:
        :param item_obj:
        :param tsx_item_model_class:
        :return:
        """
        try:
            tsxitem = tsx_item_model_class.objects.get( srid=item_obj.get('id') )
        except tsx_item_model_class.DoesNotExist:
            tsxitem = tsx_item_model_class()
        #
        # get the sub-dicts first
        content_obj    = item_obj.get('content__list',{})
        provider_obj   = item_obj.get('provider__list',{})

        # set the tsxcontent reference
        tsxitem.tsxcontent          = tsxcontent

        tsxitem.srid                = item_obj.get('id')
        tsxitem.pcid                = provider_obj.get('provider_content_id')
        tsxitem.content_created     = self.__parse_datetime(item_obj.get('created',''))
        tsxitem.content_modified    = self.__parse_datetime(item_obj.get('updated',''))
        tsxitem.content_published   = self.__parse_datetime(provider_obj.get('original_publish',''))
        tsxitem.title               = item_obj.get('title')         # ie: 'NBA Note - Team, Player'
        tsxitem.byline              = item_obj.get('byline')        # ie: 'The Sports Xchange'
        tsxitem.dateline            = item_obj.get('dateline','')   # ie: '12/14/2015'
        tsxitem.credit              = item_obj.get('credit')
        tsxitem.content             = content_obj.get('long')
        # print('')
        # print(str(item_obj))
        tsxitem.save()

        #
        # now parse each TsxRef (teams or players)
        # which reference the tsxitem.
        ref_list = self.__get_ref_list(item_obj)
        # print('***')
        # print('ref_list', str(ref_list))
        # print('***')
        for ref_obj in ref_list:
            ref_instance = None
            if ref_obj.get('type') == 'profile':
                ref_instance = self.__parse_ref_for_class( tsxitem, ref_obj, self.player_model_class)
            elif ref_obj.get('type') == 'organization':
                ref_instance = self.__parse_ref_for_class( tsxitem, ref_obj, self.team_model_class)
            else:
                print('__parse_item_for_class() - invalid ref type: %s, not in ["profile","organization"]' % str(ref_obj.get('type')))
                pass

        return tsxitem

    def __get_ref_list(self, item_obj):
        """
        get the 'refs__list' out of the item object

        refs__list will be a dict (a single object)
          OR
        refs__list will be a list (with may objects!

        example single:
            'refs__list': {
                'ref__list': {
                    'type': 'organization',
                    'sportsdata_id': '583ec928-fb46-11e1-82cb-f4ce4684ea4c',
                    'name': 'Detroit Pistons'
                }
            },

        example list:

            "refs__list" : [
                { "ref" : { "name" : "Sessions, Ramon", "sportsdata_id" : "91ac13f8-e8d3-4902-b451-83ff32d2cf28", "type" : "profile" } },
                { "ref" : { "name" : "Washington Wizards", "sportsdata_id" : "583ec8d4-fb46-11e1-82cb-f4ce4684ea4c", "type" : "organization" } }
            ]

        :param ref_data:
        :return:
        """
        refs = []
        refs_data = item_obj.get('refs__list')
        if isinstance(refs_data, dict) and len(refs_data.items()) > 0:
            refs.append(refs_data.get('ref__list')) # get the actual ref object (type, sportsdata_id, name)
        elif isinstance(refs_data, list):
            for ref in refs_data:
                refs.append(ref.get('ref'))         # get the actual ref object (type, sportsdata_id, name)
        return refs

    def __parse_ref_for_class(self, tsxitem, ref_obj, tsx_ref_model_class):
        """
        extra the values of ref_obj to create a TsxRef (team or player) using
        the tsx_ref_model_class, and associate it with the TsxItem passed in.

        :param tsxitem:
        :param tsx_ref_model_class:
        :return:
        """

        sportsdataid = ref_obj.get('sportsdata_id')
        sportradarid = ref_obj.get('sportradar_id')
        if sportradarid is None:
            # if sportradar property doesnt exist, use the sportsdataid
            sportradarid = sportsdataid

        #
        # try to get the sports.<sport>.models.Player
        player = self.get_sport_player(sportradarid)
        if player is None:
            #print('couldnt find player for ref_obj: %s' % (str(ref_obj)))
            return None

        #
        # get or create it... we'll need to get the ContentType of the tsxitem first
        tsxitem_type = ContentType.objects.get_for_model(tsxitem)
        #print('')
        #print(str(ref_obj))
        tsxref, c = tsx_ref_model_class.objects.get_or_create(sportsdataid=sportsdataid,
                                                              sportradarid=sportradarid,
                                                              player=player,
                                                              name=ref_obj.get('name'),
                                                              tsxitem_type=tsxitem_type,
                                                              tsxitem_id=tsxitem.pk,
                                                              content_published=tsxitem.content_published)

        return tsxref

    def get_sport_player(self, sportradarid):
        try:
            return self.sport_player_class.objects.get(srid=sportradarid)
        except self.sport_player_class.DoesNotExist:
            return None













