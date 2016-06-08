#
# sports/nfl/parser.py

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

class TeamHierarchy(DataDenTeamHierarchy):
    """
    TeamHierarchy simply needs to set the right Team model internally.
    """
    team_model = Team

    def __init__(self):
        super().__init__()

    def parse(self, obj):
        super().parse(obj)  # setup PlayerStats instance

        o = obj.get_o()
        self.team.alias     = o.get('id', None)   # nfl ids are the team acronym, which is the alias
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

    def __init__(self):
        super().__init__()
        self.position_key = 'position'

    def parse(self, obj, target=None):
        super().parse( obj )

        #
        # set the fields that arent set, and update the players name (super() grabs invalid fields)
        o = obj.get_o()

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

    ###
    # for 2015 stats:
    #
    # players__list 0
    # player_records__list 0
    # rushing__list 2929
    # receiving__list 5965
    # punts__list 703
    # punt_returns__list 875
    # penalties__list 3998
    # passing__list 980
    # kickoffs__list 741
    # kick_returns__list 834
    # fumbles__list 1763
    # field_goals__list 584
    # kicks__list 613
    # defense__list 14518
    # int_returns__list 533
    # misc_returns__list 24
    # conversions__list 261
    # kick__list 0
    # rush__list 0
    # pass__list 0
    # receive__list 0
    # penalty__list 0
    # statistics__list 0
    # field_goal__list 0
    # extra_point__list 0
    # return__list 0
    # fumble__list 0
    # conversion__list 0
    # punt__list 0
    # block__list 0
    # defense_conversion__list 0
# misc__list 0
    ###
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

class GameBoxscores(AbstractDataDenParseable):
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

    def __init__(self):
        super().__init__()

    def parse(self, obj):
        """
        :param obj:
        :return:
        """

        # #
        # ###############################################################
        # # nfl official data game boxscores must setup:
        # #   self.original_obj, self.o, self.srid_finder
        # ###############################################################
        # self.original_obj = obj
        # if self.wrapped:
        #     self.o  = obj.get_o()
        # else:
        #     self.o  = obj
        # # construct an SridFinder with the dictionary data
        # self.srid_finder = SridFinder(self.o)
        # ###############################################################
        # ###############################################################
        super().parse(obj, target=None)
        o = self.o

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

class GamePbp(DataDenPbpDescription):

    game_model              = Game
    pbp_model               = Pbp
    portion_model           = GamePortion
    pbp_description_model   = PbpDescription

    def __init__(self):
        super().__init__()

    def parse(self, obj, target=None):
        super().parse( obj, target )

        if self.game is None:
            return

        #print('srid game', self.o.get('id'))
        quarters = self.o.get('quarters', {})

        for quarter_json in quarters:
            quarter_play_idx = 0
            quarter = quarter_json.get('quarter', {})
            quarter_number = quarter.get('number', None)

            if quarter_number is None:
                raise Exception('quarter_number is None! what the!?')

            #
            # get (or create) the game portion object
            game_portion = self.get_game_portion( 'quarter', quarter_number )

            drives = quarter.get('drives', [])

            for drive_json in drives:
                drive = drive_json.get('drive')     # half is a drive object! ill rename later
                #
                # create the plays
                plays = drive.get('plays', {})
                for play_json in plays:
                    srid_play   = play_json.get('play', -1)
                    summary     = play_json.get('summary','')
                    pbp_desc = self.get_pbp_description(game_portion, quarter_play_idx, '', save=False)
                    pbp_desc.srid = srid_play
                    pbp_desc.save()
                    quarter_play_idx += 1

                #
                # create the event s
                events = drive.get('events', {})
                for event_json in events:
                    sequence    = event_json.get('sequence', -1)
                    summary     = event_json.get('summary','')
                    pbp_desc = self.get_pbp_description(game_portion, sequence, summary)

class PlayPbp(DataDenPbpDescription):

    game_model              = Game
    pbp_model               = Pbp
    portion_model           = GamePortion
    pbp_description_model   = PbpDescription
    #
    player_stats_model      = sports.nfl.models.PlayerStats
    pusher_sport_pbp        = push.classes.PUSHER_NFL_PBP
    pusher_sport_stats      = push.classes.PUSHER_NFL_STATS

    def __init__(self):
        super().__init__()

    def parse(self, obj, target=None):
        #
        # dont need to call super for EventPbp - just get the event by srid.
        # if it doesnt exist dont do anything, else set the description
        #super().parse( obj, target )

        self.original_obj = obj # since we dont call super().parse() in this class
        self.srid_finder = SridFinder(obj.get_o())

        self.o = obj.get_o() # we didnt call super so we should do thisv
        srid_pbp_desc = self.o.get('id', None)
        pbp_desc = self.get_pbp_description_by_srid( srid_pbp_desc )
        if pbp_desc:
            description = self.o.get('summary', None)
            if pbp_desc.description != description:
                # only save it if its changed
                pbp_desc.description = description
                pbp_desc.save()
        # else:
        #     print( 'pbp_desc not found by srid %s' % srid_pbp_desc)

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
        (mongo_db_for_sport,'team','hierarchy'),
        (mongo_db_for_sport,'season','schedule'),
        (mongo_db_for_sport,'game','schedule'),
        (mongo_db_for_sport,'player','rosters'),
        (mongo_db_for_sport,'game','boxscores'),
        (mongo_db_for_sport,'player','stats'),
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
        #
        elif self.target == (self.mongo_db_for_sport+'.game','boxscores'):
            GameBoxscores().parse( obj )
            push.classes.DataDenPush( push.classes.PUSHER_BOXSCORES, 'game' ).send( obj, async=settings.DATADEN_ASYNC_UPDATES )

        #
        #
        elif self.target == (self.mongo_db_for_sport+'.team','hierarchy'):
            TeamHierarchy().parse( obj )

        #
        #
        elif self.target == (self.mongo_db_for_sport+'.player','rosters'):
            try:
                PlayerRosters().parse( obj )
            except PlayerRosters.PositionDoesNotExist as e:
                print(e)

        #
        #
        elif self.target == (self.mongo_db_for_sport+'.player','stats'):
            PlayerStats().parse( obj )

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
        super().cleanup_rosters(self.sport,                         # datadeb sport db, ie: 'nba'
                                sports.nfl.models.Team,             # model class for the Team
                                sports.nfl.models.Player,           # model class for the Player
                                parent_api='rosters')               # parent api where the roster players found

    def cleanup_injuries(self):
        pass # TODO for NFL Official Feed