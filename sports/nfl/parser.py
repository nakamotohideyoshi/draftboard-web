#
# sports/nfl/parser.py

import re
from django.db.transaction import atomic
from sports.sport.base_parser import AbstractDataDenParseable
import sports.nfl.models
from sports.nfl.models import (
    Team,
    Game,
    Player,
    PlayerStats,
    GameBoxscore,
    GamePortion,
    Pbp,
    PbpDescription,
    Season,
)
from sports.sport.base_parser import (
    AbstractDataDenParser,
    DataDenTeamHierarchy,
    DataDenGameSchedule,
    DataDenPlayerRosters,
    DataDenPlayerStats,
    DataDenTeamBoxscores,
    DataDenPbpDescription,
    DataDenInjury,
    SridFinder,
    DataDenSeasonSchedule,
)
import json
from dataden.classes import DataDen
import push.classes
from django.conf import settings
from sports.sport.base_parser import TsxContentParser
from push.classes import DataDenPush, PbpDataDenPush
from util.dicts import (
    Reducer,
    Shrinker,
    Manager,
)
from mysite.utils import QuickCache

class TeamHierarchy(DataDenTeamHierarchy):
    """
    TeamHierarchy simply needs to set the right Team model internally.
    """
    team_model = Team

    def __init__(self):
        super().__init__()

    def parse(self, obj):
        super().parse(obj)  # setup PlayerStats instance

        # the classic feed had to override this, but the new Official feed now does not
        # o = obj.get_o()
        # self.team.alias = o.get('id', None)   # nfl ids are the team acronym, which is the alias

        self.team.save() # commit changes

class SeasonSchedule(DataDenSeasonSchedule):
    """
    parse a "season" object to get an srid, and the year/type of the season.

    note for NFL the srid field of a Season object looks like a url,
    because thats whats actually found in the field we typically
    find srids. plus, the url uniquely identifies the season so its fine.

    example:

        {'type': 'PRE', 'name': 'PRE', 'year': 2016.0,
        'parent_api__id': 'schedule', 'id': '659d2bd0-c43e-4bb0-8503-9d576911d029',
        'weeks': [{'week': '60bfeef5-51db-4e2f-bb85-377a6386ac6d'},
        {'week': '1d810a06-3f3b-4865-a0ba-f28091dd8d6f'},
        {'week': '79300bc5-2fc5-489a-9d4f-ef641e6f5885'},
        {'week': '051e133e-75ef-4818-835a-87e84fdc53b2'},
        {'week': 'acd0b2ac-8d64-4eac-8f34-365b807e996d'}],
        'dd_updated__id': 1464828462196,
        'xmlns': 'http://feed.elasticstats.com/schema/nfl/premium/schedule-v2.0.xsd'}

    """

    season_model = Season

    # override the default season_year field
    field_season_year = 'year'

    def __init__(self):
        super().__init__()

    def parse(self, obj, target=None):
        super().parse(obj, target)

        if self.season is None:
            return

        self.season.save()

class GameSchedule(DataDenGameSchedule):
    """
    GameSchedule simply needs to set the right Team & Game model internally
    """

    team_model      = Team
    game_model      = Game
    season_model    = Season

    # override parent field for retrieving season srid
    field_season_srid = 'season__id'

    def __init__(self):
        super().__init__()

    def parse(self, obj):
        """
        parse the object and save the draftboard model
        """
        super().parse(obj)
        if self.game is None:
            return

        o = obj.get_o()

        # super sets these fields (start is pulled from 'scheduled')
        #   ['srid','home','away','start','status','srid_home','srid_away','title']]
        weather_info            = o.get('weather', '')
        self.game.weather_json  = weather_info
        self.game.save()

class PlayerRosters(DataDenPlayerRosters):

    team_model      = Team
    player_model    = Player

    # dont add players that play these positions to the system
    exclude_positions = [
        'DST','DE', 'OLB', 'CB',  'K',
        'DT', 'DT', 'FS',  'OT',  'OG',
        'SS', 'C',  'MLB', 'P',   'LB',
        'OL', 'LS', 'NT',  'SAF', 'G',
        'DB', 'T',
    ]

    def __init__(self):
        super().__init__()
        self.position_key = 'position'

    def parse(self, obj, target=None):
        # set the fields that arent set, and update the players name (super() grabs invalid fields)
        o = obj.get_o()

        # ignore players that arent relevant for fantasy purposes
        position = o.get(self.position_key)
        if position in self.exclude_positions:
            return # skip parsing this player

        # super sets up some internal stuff and is required to be
        # called before parsing nfl player specific fields
        super().parse( obj )

        # override the first name with preferred first name
        self.player.first_name = o.get('preferred_name')

        # override the birth date
        self.player.birth_date      = o.get('birth_date', '')

        # get draft information
        draft_info = o.get('draft__list', {})
        self.player.draft_pick      = draft_info.get('number', '')
        self.player.draft_round     = draft_info.get('round', '')
        self.player.draft_year      = draft_info.get('year', '')
        self.player.srid_draft_team = draft_info.get('team', '')

        self.player.save()

class PlayerStats(DataDenPlayerStats):
    """
    parse NFL player stats. player stats are broken up into different objects where
    each object comes from a list containing the stats for that category.
    categories are for things like rushing, passing, receiving, etc...

    for the complete list of categories, look at the distinct "parent_list__id" field
    of the player collection:

        $> db.player.distinct('parent_list__id')
        ['players__list',
         'player_records__list',
         'rushing__list',
         'receiving__list',
         'punts__list',
         'punt_returns__list',
         'penalties__list',
         'passing__list',
         'kickoffs__list',
         'kick_returns__list',
         'fumbles__list',
         'field_goals__list',
         'kicks__list',
         'defense__list',
         'int_returns__list',
         'misc_returns__list',
         'conversions__list',
         'kick__list',
         'rush__list',
         'pass__list',
         'receive__list',
         'penalty__list',
         'statistics__list',
         'field_goal__list',
         'extra_point__list',
         'return__list',
         'fumble__list',
         'conversion__list',
         'punt__list',
         'block__list',
         'defense_conversion__list',
         'misc__list']
        $>

    now you can query for a category of stats for a player
    by also querying with its 'parent_list__id':

        $> db.player.findOne({'parent_api__id':'stats', 'parent_list__id':'rushing__list'})
            or
        $> db.player.findOne({'parent_api__id':'stats', 'parent_list__id':'passing__list'})

    example from  "passing__list":

        {
            'air_yards': 198.0,
             'attempts': 45.0,
             'avg_yards': 5.7,
             'cmp_pct': 57.8,
             'completions': 26.0,
             'dd_updated__id': 1464829036635,
             'game__id': '554aac47-088a-42fc-9888-366c3cec5968',
             'id': 'aae6d92e-5f28-43ee-b0dc-522e80e99f76',
             'interceptions': 1.0,
             'jersey': 18.0,
             'longest': 22.0,
             'longest_touchdown': 19.0,
             'name': 'Peyton Manning',
             'parent_api__id': 'stats',
             'parent_list__id': 'passing__list',
             'position': 'QB',
             'rating': 86.9,
             'redzone_attempts': 8.0,
             'reference': '00-0010346',
             'sack_yards': 18.0,
             'sacks': 3.0,
             'team__id': 'ce92bd47-93d5-4fe9-ada4-0fc681e6caa0',
             'touchdowns': 3.0,
             'yards': 256.0}
        }

    note that a player can be, and probably will be if they accrued stats,
    in most of these categories for each game they've played! In this example,
    Jericho Cotchery was in 11 of the lists!

        $> db.player.find({'parent_api__id':'stats','id':'dc2b3e27-0bc1-4ea7-b80e-f9ef81cab2c9'}).count()
         11
        $>

    """

    game_model          = Game
    player_model        = Player
    player_stats_model  = sports.nfl.models.PlayerStats

    def __init__(self):
        super().__init__()

    def parse(self, obj):
        super().parse(obj)   # sets up self.ps  (the PlayerStats instance - may be None)

        if self.p is None or self.ps is None or self.g is None:
            return

        # if self.ps is None:
        o = obj.get_o()

        self.ps.position            = self.p.position # copy the dst Player's position in here
        self.ps.primary_position    = self.p.position # copy the dst Player's position in here

        parent_list = o.get('parent_list__id', None)

        if parent_list == "passing__list":
            self.ps.pass_td     = o.get('touchdowns',       0)
            self.ps.pass_yds    = o.get('yards',            0)
            self.ps.pass_int    = o.get('interceptions',    0)
        if parent_list == "rushing__list":
            self.ps.rush_td     = o.get('touchdowns',   0)
            self.ps.rush_yds    = o.get('yards',        0)
        elif parent_list == "receiving__list":
            self.ps.rec_td      = o.get('touchdowns',   0)
            self.ps.rec_yds     = o.get('yards',        0)
            self.ps.rec_rec     = o.get('receptions',   0)
        elif parent_list == "punt_returns__list":
            self.ps.ret_punt_td = o.get('touchdowns',   0)
        elif parent_list == "kick_returns__list":
            self.ps.ret_kick_td = o.get('touchdowns',   0)
        elif parent_list == "fumbles__list":
            self.ps.off_fum_lost    = o.get('lost_fumbles',     0)
            self.ps.off_fum_rec_td  = o.get('own_rec_tds',      0)
        elif parent_list == "conversions__list":
            # {
            #   'jersey': 11.0, 'category': 'receive', 'dd_updated__id': 1464828941114,
            #   'id': 'f9036897-99d5-4d9a-8965-0c7e0f9e43bd', 'team__id': 'cb2f9f1f-ac67-424e-9e72-1475cb0ed398',
            #   'successes': 1.0, 'reference': '00-0030460', 'game__id': 'acbb3001-6bb6-41ce-9e91-942abd284e4c',
            #   'attempts': 1.0, 'position': 'WR', 'parent_api__id': 'stats',
            #   'name': 'Markus Wheaton', 'parent_list__id': 'conversions__list'
            # }
            self.ps.two_pt_conv = o.get('successes',    0)
        else:
            # print( str(o) )
            # print( 'obj parent_list__id was not found !')
            return

        self.ps.save()

class GameBoxscoreReducer(Reducer):
    remove_fields = [
        '_id',
        'scoring_drives__list',
        'entry_mode',
        'situation__list',
        'number',
        'last_event__list',
        'xmlns',
        'scoring__list',
        'reference',
        'utc_offset',
        'parent_api__id',
    ]

class GameBoxscoreShrinker(Shrinker):
    fields = {
        'summary__list' : 'summary',
        'dd_updated__id' : 'ts',
        'id' : 'srid_game'
    }

class GameBoxscoreManager(Manager):
    reducer_class = GameBoxscoreReducer
    shrinker_class = GameBoxscoreShrinker

class GameBoxscoreParser(AbstractDataDenParseable):
    """
    example data for a GameBoxscore:
        {
            'attendance': 76512.0,
            'clock': '00:00',
            'dd_updated__id': 1464834044370,
            'entry_mode': 'INGEST',
            'id': '0141a0a5-13e5-4b28-b19f-0c3923aaef6e',
            'last_event__list': {'event': 'c68447b0-425f-4e7b-8200-581ca222c03d'},
            'number': 8.0,
            'parent_api__id': 'boxscores',
            'quarter': 4.0,
            'reference': 56510.0,
            'scheduled': '2015-09-13T17:02:41+00:00',
            'scoring__list': [{'quarter': 'fd31368b-a159-4f56-a022-afc691e34755'},
              {'quarter': '17ee8c4c-3e1c-4dbb-83eb-f54fabe2a117'},
              {'quarter': 'da1c72aa-a5eb-44db-a23f-f9e2284d7968'},
              {'quarter': '99063002-e5ee-4239-b686-f5aaa192e5d8'}],
            'scoring_drives__list': [{'drive': 'a956d9cb-d8ab-408c-91fc-442f06e338ff'},
              {'drive': '37c135a1-9d50-4da7-a975-f93a5bc2bfb5'},
              {'drive': 'd7474f02-e785-4638-b604-1065174d4a67'},
              {'drive': '3b6e7850-bfa5-4ac8-90f4-9bd14a5a12c9'}],
            'situation__list': {'clock': '00:00',
              'down': 2.0,
              'location': '4809ecb0-abd3-451d-9c4a-92a90b83ca06',
              'possession': '4809ecb0-abd3-451d-9c4a-92a90b83ca06',
              'yfd': 11.0},
            'status': 'closed',
            'summary__list': {'away': '4809ecb0-abd3-451d-9c4a-92a90b83ca06',
              'home': '22052ff7-c065-42ee-bc8f-c4691c50e624',
              'season': '46aa2ca3-c2fc-455d-8256-1f7893a87113',
              'venue': '7c11bb2d-4a53-4842-b842-0f1c63ed78e9',
              'week': '581edacd-e641-43d6-9e69-76b29a306643'},
            'utc_offset': -5.0,
            'weather': 'Partly Cloudy Temp: 69 F, Humidity: 58%, Wind: NW 10 mph'
        }
    """

    gameboxscore_model  = GameBoxscore
    team_model          = Team

    manager_class       = GameBoxscoreManager

    channel = push.classes.PUSHER_BOXSCORES  # 'boxscores'
    event = 'game'

    def __init__(self):
        super().__init__()

    def parse(self, obj, target):
        """
        :param obj:
        :return:
        """

        # parse triggered object will set original_obj
        # to the current object (with wrapper)
        # and set the self.o (to the unwrapped object)
        self.parse_triggered_object(obj)
        o = self.o # everything uses 'o already

        summary_list = o.get('summary__list', {})

        srid_game   = o.get('id', None)
        srid_home   = summary_list.get('home', None)
        srid_away   = summary_list.get('away', None)

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

        self.boxscore.srid_home     = srid_home
        self.boxscore.home          = h
        self.boxscore.away          = a
        self.boxscore.srid_away     = srid_away

        self.boxscore.quarter       = o.get('quarter', 0)
        self.boxscore.clock         = o.get('clock', '' )
        self.boxscore.coverage      = o.get('coverage', '')    # deprecated, but it will default to empty string
        self.boxscore.status        = o.get('status', '')
        self.boxscore.title         = o.get('title', '')

        self.boxscore.save()

    def send(self, *args, **kwargs):
        data = self.get_send_data()

        # pusher it
        push.classes.DataDenPush(self.channel, self.event).send(data)

class TeamBoxscoreReducer(Reducer):
    remove_fields = [
        '_id',
        'parent_list__id',
        'reference',
        'parent_api__id',
    ]

class TeamBoxscoreShrinker(Shrinker):
    fields = {
        'id' : 'srid_team',
        'dd_updated__id' : 'ts',
        'game__id' : 'srid_game',
    }

class TeamBoxscoreManager(Manager):
    reducer_class = TeamBoxscoreReducer
    shrinker_class = TeamBoxscoreShrinker

class TeamBoxscoreParser(AbstractDataDenParseable):
    """
    example data for a TeamBoxscore:
        {
            "_id": "cGFyZW50X2FwaV9faWRib3hzY29yZXNnYW1lX19pZDFjYTlhMGMxLWQxNDUtNGFjYi1hY2EyLWNiMmI1ZmU1MjliOXBhcmVudF9saXN0X19pZHN1bW1hcnlfX2xpc3RpZDQyNTRkMzE5LTFiYzctNGY4MS1iNGFiLWI1ZTZmMzQwMmI2OQ==",
            "alias": "TB",
            "id": "4254d319-1bc7-4f81-b4ab-b5e6f3402b69",
            "market": "Tampa Bay",
            "name": "Buccaneers",
            "points": 14,
            "reference": 4970,
            "remaining_timeouts": 2,
            "used_timeouts": 1,
            "parent_api__id": "boxscores",
            "dd_updated__id": 1464834061361,
            "game__id": "1ca9a0c1-d145-4acb-aca2-cb2b5fe529b9",
            "parent_list__id": "summary__list"
        }
    """

    gameboxscore_model  = GameBoxscore
    team_model          = Team

    manager_class       = TeamBoxscoreManager

    channel = push.classes.PUSHER_BOXSCORES  # 'boxscores'
    event = 'team'

    def __init__(self):
        super().__init__()

    def parse(self, obj, target):
        """
        :param obj:
        :return:
        """

        # parse triggered object will set original_obj
        # to the current object (with wrapper)
        # and set the self.o (to the unwrapped object)
        self.parse_triggered_object(obj)
        # o = self.o # everything uses 'o already
        #
        # summary_list = o.get('summary__list', {})
        #
        # srid_game   = o.get('id', None)
        # srid_home   = summary_list.get('home', None)
        # srid_away   = summary_list.get('away', None)
        #
        # try:
        #     h = self.team_model.objects.get( srid=srid_home )
        # except self.team_model.DoesNotExist:
        #     #print( str(o) )
        #     #print( 'Team (home_team) does not exist for srid so not creating GameBoxscore')
        #     return
        #
        # try:
        #     a = self.team_model.objects.get( srid=srid_away )
        # except self.team_model.DoesNotExist:
        #     #print( str(o) )
        #     #print( 'Team (away_team) does not exist for srid so not creating GameBoxscore')
        #     return

        # try:
        #     self.boxscore = self.gameboxscore_model.objects.get(srid_game=srid_game)
        # except self.gameboxscore_model.DoesNotExist:
        #     self.boxscore = self.gameboxscore_model()
        #     self.boxscore.srid_game = srid_game

        # self.boxscore.srid_home     = srid_home
        # self.boxscore.home          = h
        # self.boxscore.away          = a
        # self.boxscore.srid_away     = srid_away
        #
        # self.boxscore.quarter       = o.get('quarter', 0)
        # self.boxscore.clock         = o.get('clock', '' )
        # self.boxscore.coverage      = o.get('coverage', '')    # deprecated, but it will default to empty string
        # self.boxscore.status        = o.get('status', '')
        # self.boxscore.title         = o.get('title', '')

        # self.boxscore.save()

    def send(self, *args, **kwargs):
        data = self.get_send_data()

        # pusher it
        push.classes.DataDenPush(self.channel, self.event).send(data)

class PlayReducer(Reducer):
    remove_fields = [
        'away_points',
        'wall_clock',
        'home_points',
        # 'statistics__list',       # this has the passer/rusher / receiver/defense guy
        'parent_api__id',
        '_id',
        # 'alt_description',        # this one reads better than the 'description' field imo
        'quarter__id',              # not sure if we will want the quarter information or not
        'reference',                # matches sequence from the looks of it
        'id',                       # srid of this play
        # 'type',                   # ex: "pass"
        'sequence',                 # order of the play within the game i think
        # 'start_situation__list',  # ex: {"yfd": 5, "location": <srid>, "down": 2, "clock": "14:30", "possession": <srid>}
        # 'dd_updated__id',         # unix ts play was parsed
        'parent_list__id',          # 'pbp'
        'description',              # has the player numbers - use 'alt_description'
        'drive__id',                # srid of the drive this play is contained within
        # 'game__id',               # game srid
        # 'end_situation__list',    # ex: {"yfd": 5, "location": <srid>, "down": 2, "clock": "14:30", "possession": <srid>}
    ]

class PlayShrinker(Shrinker):
    fields = {
        'dd_updated__id' : 'ts',
        'alt_description' : 'description',
        'game__id' : 'srid_game',
        'statistics__list' : 'statistics',
        'start_situation__list' : 'start_situation',
        'end_situation__list' : 'end_situation',
    }

class ExtraInfo(object):
    """
    extracts consistent tokens from the human readable play description text,
     to name one example: the pass or rush 'side' of the field which is
     typically one of the values in the list: ['left', 'middle', 'right']
    """

    # the NFLOfficial play objects have a "type" field. primarily we care
    # if the value of the "type" field is 'pass' or 'rush' but it can be other things
    type_pass = 'pass'
    type_rush = 'rush'
    expected_types = [type_pass, type_rush]

    # formation type, if unknown, we call it 'default'
    formation           = 'formation'
    default_formation   = 'default'

    # pass/rush dict keys
    side                = 'side'
    distance            = 'distance'
    scramble            = 'scramble'

    # major event flags
    touchdown           = 'touchdown'
    intercepted         = 'intercepted'
    fumbles             = 'fumbles'
    no_huddle           = 'no_huddle'
    wildcat             = 'wildcat'

    # specific values for distance, and side known as 99.99% likely
    distance_short  = 'short'
    distance_deep   = 'deep'
    side_left       = 'left'
    side_middle     = 'middle'
    side_right      = 'right'

    # regular expressions we will hunt for (all lowercase)
    regex_distance  = r'(short|deep)'
    regex_side      = r'(left|middle|right)'
    regex_no_huddle = r'no[\s]+huddle'
    regex_wildcat   = r'direct[\s]+snap'

    # formation is only a single thing right now and its simpler to string match it
    str_formation_shotgun = 'shotgun'
    str_touchdown = 'touchdown'
    str_intercepted = 'intercepted'
    str_fumbles = 'fumbles'
    str_scrambles = 'scrambles'

    def __init__(self, type, description):
        """
        create an ExtraInfo object from a play description (the human readable text)
        :param description: ex: (10:20) A.Morris left end to MIA 26 for 10 yards (J.Jenkins).
        """
        self.type = type
        self.description = description
        self.ld_description = self.description.lower()

        # initialize our underlying dict with default values
        self.data = {
            self.formation : self.default_formation,
            self.touchdown : False,
            self.intercepted : False,
            self.fumbles : False,
            self.wildcat : False,
        }

        # 1. parse things that could always be there (ie: extra_data top level fields)
        # set flags for important events like: touchdowns, interceptions, fumbles...
        self.update_major_flags()

        # 2. if 'type' is in the execpted_types, parse its specific information
        self.data[self.type] = self.get_play_type_data(self.type)

    def get_data(self):
        """ return the data as a dict """
        return self.data

    def update_major_flags(self):
        """ """
        # get the string name of the offensive formation
        self.data[self.formation]   = self.parse_formation()        # in ['shotgun', 'default']

        # flags
        self.data[self.no_huddle]   = self.parse_no_huddle()        # bool
        self.data[self.touchdown]   = self.parse_touchdown()        # bool
        self.data[self.intercepted] = self.parse_intercepted()      # bool
        self.data[self.fumbles]     = self.parse_fumbles()          # bool
        self.data[self.wildcat]     = self.parse_wildcat()          # bool

        return self.data

    def parse_formation(self):
        """ extract and return the formation """
        formation_name = self.default_formation
        if self.str_formation_shotgun in self.ld_description:
            formation_name = self.str_formation_shotgun

        return formation_name

    def parse_no_huddle(self):
        """ return boolean indicating if its offense is using the no-huddle """
        matches = re.findall(self.regex_no_huddle, self.ld_description)
        return len(matches) > 0

    def parse_touchdown(self):
        """ return boolean touchdown flag """
        return self.str_touchdown in self.ld_description

    def parse_intercepted(self):
        """ return boolean intercepted flag """
        return self.str_intercepted in self.ld_description

    def parse_fumbles(self):
        """ return boolean fumbles flag """
        return self.str_fumbles in self.ld_description

    def parse_wildcat(self):
        """ return boolean wildcat flag """
        matches = re.findall(self.regex_wildcat, self.ld_description)
        return len(matches) > 0

    def parse_distance(self):
        """ """
        matches = re.findall(self.regex_distance, self.ld_description)
        #print('matches:', str(matches))
        if len(matches) > 0:
            return matches[0]
        return None # we might want to raise an exception here # TODO - no 'distance' found

    def parse_side(self):
        """ """
        matches = re.findall(self.regex_side, self.ld_description)
        #print('matches:', str(matches))
        if len(matches) > 0:
            return matches[0]
        return None  # we might want to raise an exception here # TODO - no 'side' found

    def parse_scramble(self):
        """ return boolean scrambles flag, specifically for the 'rush' data """
        return self.str_scrambles in self.ld_description

    def get_play_type_data(self, type):
        """ build the special data for the play type passed in """
        if type == self.type_pass:
            return self.get_pass_data()

        elif type == self.type_rush:
            return self.get_rush_data()

        else:
            # we dont parse specific info for this play type
            return {}

    def get_pass_data(self):
        """ special data for 'pass' play """
        pass_data = {
            self.distance: self.parse_distance(),   # in ['short', 'deep']
            self.side: self.parse_side(),           # in ['left', 'middle', 'right']
        }
        return pass_data

    def get_rush_data(self):
        """ special data for 'rush' play """
        rush_data = {
            self.scramble: self.parse_scramble(),   # True indicates QB is rusher, otherwise false
            self.side: self.parse_side(),           # in ['left', 'middle', 'right']
        }
        return rush_data

class PlayManager(Manager):
    """
    wraps the Reducer & Shrinker tools for compacting and cleaning up NFL pbp data.
    """

    reducer_class = PlayReducer
    shrinker_class = PlayShrinker

    field_statistics    = 'statistics__list'

    field_defense       = 'defense__list'
    field_kick          = 'kick__list'

    field_pass          = 'pass__list'
    field_return        = 'return__list'
    field_rush          = 'rush__list'
    field_receive       = 'receive__list'

    ignore_fields = [
        field_defense, field_kick
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.clean_statistics_list()

        self.update_extra_info()

    def update_extra_info(self):
        """ parse the description text and inject extra info """
        type = self.raw_data.get('type')
        description = self.raw_data.get('alt_description')
        self.raw_data['extra_info'] = ExtraInfo(type, description).get_data()

    def clean_statistics_list(self):
        # get statistics list  -- dont forget to replace it after we clean it up
        statistics = self.raw_data.get(self.field_statistics)
        if statistics is None:
            return # nothing to do - it didnt exist

        # there are some lists we will just want to pop off
        for field in self.ignore_fields:
            try:
                statistics.pop(field)
            except KeyError:
                pass # it wasnt there to begin with - so dont worry about it

        # 1. cleanup pass__list
        # convert sack to a boolean
        pass_list = statistics.get(self.field_pass, {})
        sack = pass_list.get('sack')
        if pass_list != {} and sack is not None:
            pass_list['sack'] = self.int2bool(sack)
            # and now put this data back into the internal data
            statistics[self.field_pass] = pass_list
            self.raw_data[self.field_statistics] = statistics

        # 2. cleanup return__list
        return_list = statistics.get(self.field_return, {})
        retrn = return_list.get('return')
        if return_list != {} and retrn is not None:
            return_list['return'] = self.int2bool(retrn)
            # put it back in
            statistics[self.field_return] = return_list
            self.raw_data[self.field_statistics] = statistics

class PossessionReducer(Reducer):
    remove_fields = [
        'game__id',
        'quarter__id',
        'play__id',
        'reference',
        '_id',
        'dd_updated__id',
        'parent_api__id',
        'id',
        'parent_list__id',
        'drive__id',
    ]

class PossessionShrinker(Shrinker):
    fields = {} # there arent any

class PossessionManager(Manager):
    reducer_class = PossessionReducer
    shrinker_class = PossessionShrinker

class LocationReducer(Reducer):
    remove_fields = [
        'parent_list__id',
        'play__id',
        'id',
        'game__id',
        'parent_api__id',
        'drive__id',
        '_id',
        'dd_updated__id',
        'quarter__id',
        'reference',
    ]

class LocationShrinker(Shrinker):
    fields = { } # there arent any

class LocationManager(Manager):
    reducer_class = LocationReducer
    shrinker_class = LocationShrinker

# # for the 'statistics__list' : 'pass__list' stats
# class PassReducer(Reducer):
#     remove_fields = [] # TODO
# class PassShrinker(Shrinker):
#     fields = {} # TODO
# class PassManager(Manager):
#     reducer_class = PassReducer
#     shrinker_class = PassShrinker
#
# # for the 'statistics__list' : 'receive__list' stats
# class ReceiveReducer(Reducer):
#     remove_fields = [] # TODO
# class ReceiveShrinker(Shrinker):
#     fields = {} # TODO
# class ReceiveManager(Manager):
#     reducer_class = ReceiveReducer
#     shrinker_class = ReceiveShrinker
#
# # for the 'statistics__list' : 'rush__list' stats
# class RushReducer(Reducer):
#     remove_fields = [] # TODO
# class RushShrinker(Shrinker):
#     fields = {} # TODO
# class RushManager(Manager):
#     reducer_class = RushReducer
#     shrinker_class = RushShrinker

class PlayParser(DataDenPbpDescription):

    class PlayCache(QuickCache):
        name = 'PlayCache_nflo_pbp'

    class StartPossessionCache(QuickCache):
        name = 'StartPossessionCache_nflo_pbp'
        field_id = 'play__id'

    class StartLocationCache(QuickCache):
        name = 'StartLocationCache_nflo_pbp'
        field_id = 'play__id'

    class EndPossessionCache(QuickCache):
        name = 'EndPossessionCache_nflo_pbp'
        field_id = 'play__id'

    class EndLocationCache(QuickCache):
        name = 'EndLocationCache_nflo_pbp'
        field_id = 'play__id'

    field_pbp_object = 'pbp'

    game_model              = Game
    pbp_model               = Pbp
    portion_model           = GamePortion
    pbp_description_model   = PbpDescription

    player_stats_model      = sports.nfl.models.PlayerStats
    pusher_sport_pbp        = push.classes.PUSHER_NFL_PBP
    pusher_sport_stats      = push.classes.PUSHER_NFL_STATS

    manager_class           = PlayManager

    def __init__(self):
        super().__init__()
        self.ts = None
        self.play_srid = None

    def update_required_parts(self, ts, play_srid):
        """ must be called after we've cached the item we just set with parse() """

        # very important to set ts, and play_srid internally now
        # because they are the values enabling us to get our complete object
        self.ts = ts
        self.play_srid = play_srid

        # these three items are required in order to send this item
        required_parts = []

        play = self.PlayCache().fetch(ts, play_srid)
        required_parts.append(play)

        start_location = self.StartPossessionCache().fetch(ts, play_srid)
        required_parts.append(start_location)

        start_possession = self.StartLocationCache().fetch(ts, play_srid)
        required_parts.append(start_possession)

        end_location = self.EndPossessionCache().fetch(ts, play_srid)
        required_parts.append(end_location)

        end_possession = self.EndLocationCache().fetch(ts, play_srid)
        required_parts.append(end_possession)

        return required_parts

    def cache_target(self, o, target):
        ts = o.get('dd_updated__id')
        play_srid = None
        if target == ('nflo.play', 'pbp'):
            play_srid = o.get('id')
            self.PlayCache(o)
            #tmp_o = c.fetch(ts, play_srid)
        elif target == ('nflo.possession', 'pbp'):
            play_srid = o.get('play__id')
            situation_type = o.get('parent_list__id')
            if situation_type == 'start_situation__list':
                self.StartPossessionCache(o)
            else: # 'end_situation__list'
                self.EndPossessionCache(o)
        elif target == ('nflo.location', 'pbp'):
            play_srid = o.get('play__id')
            situation_type = o.get('parent_list__id')
            if situation_type == 'start_situation__list':
                self.StartLocationCache(o)
            else: # 'end_situation__list'
                self.EndLocationCache(o)

        if ts is not None and play_srid is not None:
            return (ts, play_srid)
        # else:
        return None # TODO dont return None! raise something... the caller expects a tuple...

    def parse(self, obj, target):
        # this strips off the dataden oplog wrapper, and sets the SridFinder internally.
        # now we can use self.o which is the data object we care about.
        self.parse_triggered_object(obj)

        # update the current object it its own cache first
        ts, play_srid = self.cache_target(self.o, target)

        # completes all the required parts (if they exist yet)
        required_parts = self.update_required_parts(ts, play_srid)

        if None not in required_parts:
            self.send()

    def get_send_data(self):
        """ build the linked object from the parts """

        #
        # assumes that everthing must exist at this point for us to be able to build it!
        play = self.PlayCache().fetch(self.ts, self.play_srid)

        start_location = self.StartLocationCache().fetch(self.ts, self.play_srid)
        start_possession = self.StartPossessionCache().fetch(self.ts, self.play_srid)

        end_location = self.EndLocationCache().fetch(self.ts, self.play_srid)
        end_possession = self.EndPossessionCache().fetch(self.ts, self.play_srid)

        # "start_situation__list": {
        #   "down": 2,
        #   "yfd": 5,
        #   "location": "22052ff7-c065-42ee-bc8f-c4691c50e624",
        #   "clock": "14:30",
        #   "possession": "22052ff7-c065-42ee-bc8f-c4691c50e624"
        # }

        play['start_situation__list']['possession'] = PossessionManager(start_possession).get_data()
        play['start_situation__list']['location']   = LocationManager(start_location).get_data()

        play['end_situation__list']['possession']   = PossessionManager(end_possession).get_data()
        play['end_situation__list']['location']     = LocationManager(end_location).get_data()

        data = {
            self.field_pbp_object : PlayManager(play).get_data(),
        }

        #print('get_send_data:', str(data))
        return data

    def send(self, *args, **kwargs):
        super().send(*args, **kwargs) #force=True)

class Injury(DataDenInjury):

    player_model = Player
    injury_model = sports.nfl.models.Injury

    key_iid     = 'id' # the name of the field in the obj

    def __init__(self, wrapped=True):
        super().__init__(wrapped)

    def parse(self, obj, target=None):
        super().parse(obj, target)

        if self.player is None or self.injury is None:
            return

        # "game_status" : "PRO",
        # "id" : "54106d2b-dd47-4f39-9139-5b36c084a78d",
        # "practice_status" : "Unknown",
        # "start_date" : "2015-01-02T00:00:00+00:00",
        # "parent_api__id" : "gameroster",
        # "dd_updated__id" : NumberLong("1432749271863"),
        # "game__id" : "20048978-0f43-4755-a6de-e2d6b3b3fcd2",
        # "team__id" : "CAR",
        # "player__id" : "f4baa4a3-8548-4cc1-bba8-e5e8d5d4656e",
        # "parent_list__id" : "injuries__list",
        # "description" : "Not Injury Related",

        #
        # extract the information from self.o
        self.injury.srid                = self.o.get('id',          '') # not set by parent
        self.injury.practice_status     = self.o.get('practice_status', '')
        self.injury.status              = self.o.get('game_status', '')
        self.injury.description         = self.o.get('description', '')
        self.injury.save()

        #
        # connect the player object to the injury object
        self.player.injury = self.injury
        self.player.save()

class DataDenNfl(AbstractDataDenParser):

    mongo_db_for_sport = 'nflo'

    triggers = [
        (mongo_db_for_sport, 'team', 'hierarchy'),
        (mongo_db_for_sport, 'season', 'schedule'),
        (mongo_db_for_sport, 'game', 'schedule'),
        (mongo_db_for_sport, 'player', 'rosters'),
        (mongo_db_for_sport, 'game', 'boxscores'),
        (mongo_db_for_sport, 'team', 'boxscores'),
        (mongo_db_for_sport, 'player', 'stats'),

        # play by play
        (mongo_db_for_sport, 'play', 'pbp'),
        (mongo_db_for_sport, 'location', 'pbp'),
        (mongo_db_for_sport, 'possession', 'pbp'),

    ]

    def __init__(self):
        self.game_model = Game # unused
        self.sport = 'nfl'

    def parse(self, obj):
        """
        :param obj:
        :return:
        """
        super().parse( obj ) # setup self.ns, self.parent_api

        #
        # switch statement selects the type of object to parse
        # the Namespace-ParentApi combination

        #
        #
        if self.target == (self.mongo_db_for_sport+'.season','schedule'):
            SeasonSchedule().parse( obj )

        #
        #
        elif self.target == (self.mongo_db_for_sport+'.game','schedule'):
            GameSchedule().parse( obj )

        #
        # parse a game obj from the boxscores feed
        elif self.target == (self.mongo_db_for_sport+'.game','boxscores'):
            game_boxscore_parser = GameBoxscoreParser()
            game_boxscore_parser.parse(obj, self.target)
        #
        # parse a team object from the boxscores feed
        elif self.target == (self.mongo_db_for_sport+'.team','boxscores'):
            # dont send it unless its from the parent__list: 'summary__list'
            team_boxscore_parser = TeamBoxscoreParser()
            team_boxscore_parser.parse(obj, self.target)
        #
        # parse a team object from the hierarchy feed
        elif self.target == (self.mongo_db_for_sport+'.team','hierarchy'):
            TeamHierarchy().parse( obj )

        #
        # parse a player from the rosters feed
        elif self.target == (self.mongo_db_for_sport+'.player','rosters'):
            try:
                PlayerRosters().parse( obj )
            except PlayerRosters.PositionDoesNotExist as e:
                print(e)

        #
        # parse a players stats (from a game) from the stats feed
        elif self.target == (self.mongo_db_for_sport+'.player','stats'):
            PlayerStats().parse( obj )

        #
        # pbp -> its a 'play' and corresponding 'location' and 'possession' objects
        elif self.target == (self.mongo_db_for_sport + '.play', 'pbp') \
            or self.target == (self.mongo_db_for_sport + '.location', 'pbp') \
            or self.target == (self.mongo_db_for_sport + '.possession', 'pbp'):

            parser = PlayParser()
            parser.parse(obj, self.target) # will call send() if it can
        #
        #
        else: self.unimplemented( self.target[0], self.target[1] )

    @atomic
    def cleanup_rosters(self):
        """
        give the parent method the Team, Player classes,
        and rosters parent api so it can flag players
        who are no long on the teams roster on_active_roster = False
        """
        super().cleanup_rosters(self.mongo_db_for_sport,            # name of mongo db for the sport
                                sports.nfl.models.Team,             # model class for the Team
                                sports.nfl.models.Player,           # model class for the Player
                                parent_api='rosters')               # parent api where the roster players found

    def cleanup_injuries(self):
        pass # TODO for NFL Official Feed