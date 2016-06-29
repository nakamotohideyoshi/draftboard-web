#
# sports/mlb/parser.py

import os
import urllib
from redis import Redis
from util.dicts import (
    Reducer,
    Shrinker,
)
from util.timesince import timeit
from collections import (
    OrderedDict,
    Counter,
)
from django.db.transaction import atomic
from django.core.cache import cache
from sports.classes import SiteSportManager
from sports.trigger import CacheList
import sports.mlb.models
from sports.mlb.models import (
    Team,
    Game,
    Player,
    GameBoxscore,
    Pbp,
    PbpDescription,
    GamePortion,
    Season,
    ProbablePitcher,
)
import sports.mlb.models # mainly to use sports.mlb.models.PlayerStats and avoid conflict with PlayerStats parser
from sports.sport.base_parser import (
    AbstractDataDenParser,
    AbstractDataDenParseable,
    DataDenTeamHierarchy,
    DataDenGameSchedule,
    DataDenPlayerRosters,
    DataDenPlayerStats,
    DataDenGameBoxscores,
    DataDenTeamBoxscores,
    DataDenPbpDescription,
    DataDenInjury,
    SridFinder,
    DataDenSeasonSchedule,
)
import json
from ast import literal_eval
from django.contrib.contenttypes.models import ContentType
from dataden.classes import DataDen
from dataden.util.hsh import Hashable
import push.classes
from django.conf import settings
from sports.sport.base_parser import TsxContentParser
from draftgroup.classes import (
    PlayerUpdateManager,
    GameUpdateManager,
)

def get_redis_instance():
    url = os.environ.get('REDISCLOUD_URL') # TODO get this env var from settings
    if url is None:
        return Redis()
    else:
        redis_url = urllib.parse.urlparse(os.environ.get('REDISCLOUD_URL')) # TODO get this env var from settings
        r = Redis(host=redis_url.hostname, port=redis_url.port, password=redis_url.password, db=0)
        return r

class HomeAwaySummary(DataDenTeamBoxscores):

    gameboxscore_model  = GameBoxscore

    def __init__(self):
        super().__init__()

    def parse(self, obj, target=None):
        super().parse( obj, target )

        # db.home.findOne({'parent_api__id':'summary', 'game__id':'31781430-ed00-49c7-827f-e03a9a1e80d4'})
        # {
        #     "_id" : "cGFyZW50X2FwaV9faWRzdW1tYXJ5Z2FtZV9faWQzMTc4MTQzMC1lZDAwLTQ5YzctODI3Zi1lMDNhOWExZTgwZDRpZGM4NzRhMDY1LWMxMTUtNGU3ZC1iMGYwLTIzNTU4NGZiMGU2Zg==",
        #     "abbr" : "CIN",
        #     "errors" : 0,
        #     "hits" : 0,
        #     "id" : "c874a065-c115-4e7d-b0f0-235584fb0e6f",
        #     "market" : "Cincinnati",
        #     "name" : "Reds",
        #     "runs" : 0,
        #     "parent_api__id" : "summary",
        #     "dd_updated__id" : NumberLong("1431648742069"),
        #     "game__id" : "31781430-ed00-49c7-827f-e03a9a1e80d4",
        #     "probable_pitcher" : "1a574c70-eb33-4202-ab97-548645a4d15e",
        #     "starting_pitcher" : "1a574c70-eb33-4202-ab97-548645a4d15e",
        #     "roster__list" : [
        #         { "player" : "07af23d5-a3b9-4526-9e89-8c7f9f5facb4" },
        #         { "player" : "090ff436-c1e8-4927-b457-355cf4f9993b" }, ... more players
        #
        #     "lineup__list" : [
        #         { "player" : "07af23d5-a3b9-4526-9e89-8c7f9f5facb4" },
        #         { "player" : "090ff436-c1e8-4927-b457-355cf4f9993b" }, ... more players
        #     ],
        #     "scoring__list" : [
        #         {
        #             "inning" : {
        #                 "number" : 1,
        #                 "runs" : 0,
        #                 "sequence" : 1
        #             }
        #         },
        #         {
        #             "inning" : {
        #                 "number" : 2,
        #                 "runs" : 0,
        #                 "sequence" : 2
        #             }
        #         },
        #         {
        #             "inning" : {
        #                 "number" : 3,
        #                 "runs" : 0,
        #                 "sequence" : 3
        #             }
        #         },
        #         {
        #             "inning" : {
        #                 "number" : 4,
        #                 "runs" : "X",
        #                 "sequence" : 4
        #             }
        #         }
        #     ],
        #     "statistics__list" : {
        #         "hitting__list" : {
        #             "ab" : 8,
        #             "abhr" : 0,
        #             "abk" : 4,
        #             "ap" : 12,
        #             "avg" : 0,
        #             "babip" : 0,
        #             "bbk" : 2,
        #             "bbpa" : 0.333,
        #             "bip" : 6,
        #             "gofo" : 0.5,
        #             "iso" : 0,
        #             "lob" : 4,
        #             "obp" : 0.333,
        #             "ops" : 0.333,
        #             "pitch_count" : 59,
        #             "rbi" : 0,
        #             "seca" : 0.625,
        #             "slg" : 0,
        #             "xbh" : 0,
        #             "onbase__list" : {
        #                 "bb" : 4,
        #                 "d" : 0,
        #                 "fc" : 0,
        #                 "h" : 0,
        #                 "hbp" : 0,
        #                 "hr" : 0,
        #                 "ibb" : 0,
        #                 "roe" : 0,
        #                 "s" : 0,
        #                 "t" : 0,
        #                 "tb" : 0
        #             },
        #             "runs__list" : {
        #                 "earned" : 0,
        #                 "total" : 0,
        #                 "unearned" : 0
        #             },
        #             "outcome__list" : {
        #                 "ball" : 29,
        #                 "dirtball" : 2,
        #                 "foul" : 3,
        #                 "iball" : 0,
        #                 "klook" : 11,
        #                 "kswing" : 8,
        #                 "ktotal" : 19
        #             },
        #             "outs__list" : {
        #                 "fidp" : 0,
        #                 "fo" : 1,
        #                 "gidp" : 0,
        #                 "go" : 2,
        #                 "klook" : 1,
        #                 "kswing" : 1,
        #                 "ktotal" : 2,
        #                 "lidp" : 0,
        #                 "lo" : 3,
        #                 "po" : 0,
        #                 "sacfly" : 0,
        #                 "sachit" : 0
        #             },
        #             "steal__list" : {
        #                 "caught" : 1,
        #                 "pct" : 0.667,
        #                 "stolen" : 2
        #             }
        #         },
        #         "pitching__list" : {
        #             "bf" : 13,
        #             "era" : 6,
        #             "error" : 0,
        #             "gofo" : 0,
        #             "ip_1" : 9,
        #             "ip_2" : 3,
        #             "k9" : 6.003,
        #             "kbb" : 1,
        #             "lob" : 6,
        #             "oba" : 0.273,
        #             "pitch_count" : 50,
        #             "whip" : 1.667,
        #             "onbase__list" : {
        #                 "bb" : 2,
        #                 "d" : 1,
        #                 "fc" : 0,
        #                 "h" : 3,
        #                 "hbp" : 0,
        #                 "hr" : 0,
        #                 "ibb" : 0,
        #                 "roe" : 0,
        #                 "s" : 2,
        #                 "t" : 0,
        #                 "tb" : 4
        #             },
        #             "runs__list" : {
        #                 "earned" : 2,
        #                 "total" : 2,
        #                 "unearned" : 0
        #             },
        #             "outcome__list" : {
        #                 "ball" : 18,
        #                 "dirtball" : 0,
        #                 "foul" : 8,
        #                 "iball" : 0,
        #                 "klook" : 9,
        #                 "kswing" : 6,
        #                 "ktotal" : 15
        #             },
        #             "outs__list" : {
        #                 "fidp" : 0,
        #                 "fo" : 0,
        #                 "gidp" : 0,
        #                 "go" : 6,
        #                 "klook" : 0,
        #                 "kswing" : 2,
        #                 "ktotal" : 2,
        #                 "lidp" : 0,
        #                 "lo" : 0,
        #                 "po" : 0,
        #                 "sacfly" : 0,
        #                 "sachit" : 0
        #             },
        #             "steal__list" : {
        #                 "caught" : 1,
        #                 "stolen" : 0
        #             },
        #             "games__list" : {
        #                 "blown_save" : 0,
        #                 "complete" : 0,
        #                 "hold" : 0,
        #                 "loss" : 0,
        #                 "qstart" : 0,
        #                 "save" : 0,
        #                 "shutout" : 0,
        #                 "svo" : 0,
        #                 "win" : 0
        #             }
        #         },
        #         "fielding__list" : {
        #             "a" : 9,
        #             "dp" : 0,
        #             "error" : 0,
        #             "fpct" : 1,
        #             "po" : 9,
        #             "tc" : 18,
        #             "tp" : 0
        #         }
        #     },
        #     "players__list" : [
        #         { "player" : "07af23d5-a3b9-4526-9e89-8c7f9f5facb4" },
        #         { "player" : "090ff436-c1e8-4927-b457-355cf4f9993b" }, ... more players who played
        #     ]
        # }

        if self.boxscore is None:
            return

        srid_team = self.o.get('id', None)

        probable_pitcher    = self.o.get('probable_pitcher', None)
        starting_pitcher    = self.o.get('starting_pitcher', None)
        scoring_json        = json.loads( json.dumps( self.o.get('scoring__list', {}) ) )
        runs                = self.o.get('runs', 0)
        hits                = self.o.get('hits', 0)
        errors              = self.o.get('errors', 0)

        if self.boxscore.srid_home == srid_team:
            # home
            #print( 'home_score / runs:', str(runs) )
            self.boxscore.home_score        = runs
            self.boxscore.srid_home_pp      = probable_pitcher
            self.boxscore.srid_home_sp      = starting_pitcher
            self.boxscore.home_hits         = hits
            self.boxscore.home_errors       = errors

        elif self.boxscore.srid_away == srid_team:
            # away
            #print( 'away_score / runs:', str(runs) )
            self.boxscore.away_score        = runs
            self.boxscore.srid_away_pp      = probable_pitcher
            self.boxscore.srid_away_sp      = starting_pitcher
            self.boxscore.away_hits         = hits
            self.boxscore.away_errors       = errors

        else:
            #print( str(self.o) )
            print( 'HomeAwaySummary team[%s] does not match home or away!' % srid_team)
            return

        #print( 'boxscore results | home_score %s | away_score %s' % (str(self.boxscore.home_score),str(self.boxscore.away_score)))
        self.boxscore.save()

class GameBoxscores(DataDenGameBoxscores):

    gameboxscore_model  = GameBoxscore
    team_model          = Team

    def __init__(self):
        super().__init__()

    def parse(self, obj, target=None):
        super().parse( obj, target )

        if self.boxscore is None:
            return

        # FOR A CLOSED GAME!!!!
        # db.game.findOne({'parent_api__id':'boxscores', 'status':'closed'})  # NOTE: 'status':'closed'
        # {
        #     "_id" : "cGFyZW50X2FwaV9faWRib3hzY29yZXNpZGM4MjQ1NmFjLWE0YjktNGNhZi04MTI0LTBhZmE3NGY5Y2YzNA==",
        #     "attendance" : 37441,
        #     "away_team" : "27a59d3b-ff7c-48ea-b016-4798f560f5e1",
        #     "coverage" : "full",
        #     "day_night" : "N",
        #     "game_number" : 1,
        #     "home_team" : "43a39081-52b4-4f93-ad29-da7f329ea960",
        #     "id" : "c82456ac-a4b9-4caf-8124-0afa74f9cf34",
        #     "scheduled" : "2015-05-10T01:10:00+00:00",
        #     "status" : "closed",
        #     "xmlns" : "http://feed.elasticstats.com/schema/baseball/v5/game.xsd",
        #     "parent_api__id" : "boxscores",
        #     "dd_updated__id" : NumberLong("1431234264301"),
        #     "venue" : "f1c03dac-3c0f-437c-a325-8d5702cd321a",
        #     "broadcast__list" : {
        #         "network" : "ROOT SPORTS"
        #     },
        #     "final__list" : {  ##### when the game is OVER it holds this
        #         "inning" : 9,
        #         "inning_half" : "T"
        #     },
        #     "home" : "43a39081-52b4-4f93-ad29-da7f329ea960",
        #     "away" : "27a59d3b-ff7c-48ea-b016-4798f560f5e1",
        #     "pitching__list" : {
        #         "win__list" : {
        #             "player" : "9760f1d6-9560-45ed-bc73-5ec2205905a2"
        #         },
        #         "loss__list" : {
        #             "player" : "a193c72e-e252-49c4-8ae5-2836039afda7"
        #         },
        #         "hold__list" : {
        #             "player" : "6f61629a-8c64-4469-b67a-48d470b7c990"
        #         }
        #     }
        # }

        #### FOR AN ACTIVE GAME!!! ...
        # db.game.findOne({'parent_api__id':'boxscores', 'status':'inprogress'})
        # {
        #     "_id" : "cGFyZW50X2FwaV9faWRib3hzY29yZXNpZDMxNzgxNDMwLWVkMDAtNDljNy04MjdmLWUwM2E5YTFlODBkNA==",
        #     "away_team" : "a7723160-10b7-4277-a309-d8dd95a8ae65",
        #     "coverage" : "full",
        #     "day_night" : "N",
        #     "game_number" : 1,
        #     "home_team" : "c874a065-c115-4e7d-b0f0-235584fb0e6f",
        #     "id" : "31781430-ed00-49c7-827f-e03a9a1e80d4",
        #     "scheduled" : "2015-05-14T23:10:00+00:00",
        #     "status" : "inprogress",
        #     "xmlns" : "http://feed.elasticstats.com/schema/baseball/v5/game.xsd",
        #     "parent_api__id" : "boxscores",
        #     "dd_updated__id" : NumberLong("1431645673334"),
        #     "venue" : "f102d8fb-de67-4b86-9053-8b55f578d45c",
        #     "broadcast__list" : {
        #         "network" : "FS-O"
        #     },
        #     "outcome__list" : {
        #         "current_inning" : 1,
        #         "current_inning_half" : "T",
        #         "type" : "pitch",
        #         "count__list" : {
        #             "balls" : 1,
        #             "half_over" : "false",
        #             "inning" : 1,
        #             "inning_half" : "T",
        #             "outs" : 1,
        #             "strikes" : 2
        #         },
        #         "hitter" : "36ee970b-0cff-4d50-b8ac-9bd16fae2dd1",
        #         "pitcher" : "1a574c70-eb33-4202-ab97-548645a4d15e",
        #         "runners__list" : [
        #             {
        #                 "runner" : "898c62b6-95bf-4973-a435-c6cb42a52158"
        #             },
        #             {
        #                 "runner" : "e47bf865-f612-47f6-8a21-3110bb455e31"
        #             }
        #         ]
        #     },
        #     "home" : "c874a065-c115-4e7d-b0f0-235584fb0e6f",
        #     "away" : "a7723160-10b7-4277-a309-d8dd95a8ae65"
        # }



        self.boxscore.attendance     = self.o.get('attendance', 0)
        self.boxscore.day_night      = self.o.get('day_night', '')
        self.boxscore.game_number    = self.o.get('game_number', '')

        #     "pitching__list" : {
        #         "win__list" : {
        #             "player" : "9760f1d6-9560-45ed-bc73-5ec2205905a2"
        #         },
        #         "loss__list" : {
        #             "player" : "a193c72e-e252-49c4-8ae5-2836039afda7"
        #         },
        #         "hold__list" : {
        #             "player" : "6f61629a-8c64-4469-b67a-48d470b7c990"
        #         }
        #     }

        pitching_list   = self.o.get('pitching__list', {})
        win_list        = pitching_list.get('win__list', {})
        loss_list       = pitching_list.get('loss__list', {})
        #hold_list       = pitching_list.get('hold__list', {}) # can return an array, (multiple "holds")
        #save_list       = pitching_list.get('save__list', {})
        #blown_save_list = pitching_list.get('blown_save__list', {})

        # when its final
        self.boxscore.srid_win       = win_list.get('player', None)
        self.boxscore.srid_loss      = loss_list.get('player', None)
        #boxscore.srid_hold      = hold_list.get('player', None)
        #boxscore.srid_save      = save_list.get('player', None)
        #boxscore.srid_blown_save = blown_save_list.get('player', None)

        outcome_list    = self.o.get('outcome__list', None)
        if outcome_list:
            #         "current_inning" : 1,
            #         "current_inning_half" : "T",
            #         "type" : "pitch",
            #         "count__list" : {
            #             "balls" : 1,
            #             "half_over" : "false",
            #             "inning" : 1,
            #             "inning_half" : "T",
            #             "outs" : 1,
            #             "strikes" : 2
            #         },
            self.boxscore.inning         = outcome_list.get('current_inning', '')
            self.boxscore.inning_half    = outcome_list.get('current_inning_half', '')

        final_list      = self.o.get('final__list', None)
        if final_list:
            #     "final__list" : {  ##### when the game is OVER it holds this
            #         "inning" : 9,
            #         "inning_half" : "T"
            #     },
            self.boxscore.inning         = final_list.get('inning', '')
            self.boxscore.inning_half    = final_list.get('inning_half', '')

        self.boxscore.save() # commit changes

class TeamHierarchy(DataDenTeamHierarchy):

    team_model = Team

    def __init__(self):
        super().__init__()

    def parse(self, obj, target=None):
        super().parse( obj, target )

        # in mlb, we set the 'abbr' to the alias
        self.team.alias = self.o.get('abbr', None)
        self.team.save()

class SeasonSchedule(DataDenSeasonSchedule):
    """
    parse a "season" object to get an srid, and the year/type of the season.
    """

    season_model = Season

    def __init__(self):
        super().__init__()

    def parse(self, obj, target=None):
        super().parse(obj, target)

        if self.season is None:
            #print('mlb Season was None - not saving')
            return

        self.season.save()

class GameSchedule(DataDenGameSchedule):

    team_model      = Team
    game_model      = Game
    season_model    = Season

    def __init__(self):
        super().__init__()

    def parse(self, obj, target=None):
        #
        # get and pre-set the season object -- mlb is special
        o = obj.get_o()
        srid = o.get('season_schedule__id')
        # we only know the season_type from chopping up the parent_api__id !
        season_type = str(o.get('parent_api__id')).split('_')[1]
        # although its unique on srid, year and type, mlb just has srid and type in this obj
        #print('srid', srid, 'season_type', season_type)
        self.season = self.season_model.objects.get(srid=srid, season_type=season_type)

        super().parse(obj, target)

        if self.game is None:
            return

        # {
        #     "_id" : "cGFyZW50X2FwaV9faWRzY2hlZHVsZV9yZWdsZWFndWVfX2lkMmZhNDQ4YmMtZmMxNy00ZDNkLWJlMDMtZTYwZTA4MGZkYzI2c2Vhc29uLXNjaGVkdWxlX19pZDk1MjNmMDM5LTA3MGMtNDlkMS1iMmUzLTVmMThiNTdjNWVlM3BhcmVudF9saXN0X19pZGdhbWVzX19saXN0aWQwMDI1NWYyNC0zNGI1LTQ4MDgtODRkOS04NjNkNDA5Nzc2ODU=",
        #     "attendance" : 41545,
        #     "away_team" : "25507be1-6a68-4267-bd82-e097d94b359b",
        #     "coverage" : "full",
        #     "day_night" : "N",
        #     "game_number" : 1,
        #     "home_team" : "a7723160-10b7-4277-a309-d8dd95a8ae65",
        #     "id" : "00255f24-34b5-4808-84d9-863d40977685",
        #     "scheduled" : "2015-04-17T02:15:00+00:00",
        #     "status" : "closed",
        #     "parent_api__id" : "schedule_reg",
        #     "dd_updated__id" : NumberLong("1431469581209"),
        #     "league__id" : "2fa448bc-fc17-4d3d-be03-e60e080fdc26",
        #     "season_schedule__id" : "9523f039-070c-49d1-b2e3-5f18b57c5ee3",
        #     "parent_list__id" : "games__list",
        #     "venue" : "2d7542f5-7b80-49f7-9b24-c53ffdc75af6",
        #     "home" : "a7723160-10b7-4277-a309-d8dd95a8ae65",
        #     "away" : "25507be1-6a68-4267-bd82-e097d94b359b",
        #     "broadcast__list" : {
        #         "network" : "CSN-BA"
        #     }
        # }

        self.game.attendance  = self.o.get('attendance',   0)
        self.game.day_night   = self.o.get('day_night',    None)
        self.game.game_number = self.o.get('game_number',  None)
        self.game.srid_venue  = self.o.get('venue', '')

        self.game.save()

class PlayerTeamProfile(DataDenPlayerRosters):

    team_model      = Team
    player_model    = Player

    def __init__(self):
        super().__init__()

    def parse(self, obj, target=None):
        super().parse( obj, target )

        # db.player.findOne({'parent_api__id':'team_profile'})
        # {
        #     "_id" : "cGFyZW50X2FwaV9faWR0ZWFtX3Byb2ZpbGV0ZWFtX19pZDU1NzE0ZGE4LWZjYWYtNDU3NC04NDQzLTU5YmZiNTExYTUyNHBhcmVudF9saXN0X19pZHBsYXllcnNfX2xpc3RpZDRhNDAzNjNmLTMxZjUtNDg3ZS1iNjEzLWU1NDU2ZjBmMDc1Mw==",
        #     "bat_hand" : "R",
        #     "birthcity" : "San Isidro",
        #     "birthcountry" : "Dominican Republic",
        #     "birthdate" : "1987-04-24",
        #     "first_name" : "Welington",
        #     "full_name" : "Welington Castillo",
        #     "height" : 70,
        #     "id" : "4a40363f-31f5-487e-b613-e5456f0f0753",
        #     "jersey_number" : 5,
        #     "last_name" : "Castillo",
        #     "mlbam_id" : 456078,
        #     "position" : "C",
        #     "preferred_name" : "Welington",
        #     "primary_position" : "C",
        #     "pro_debut" : "2010-08-11",
        #     "status" : "A",
        #     "throw_hand" : "R",
        #     "updated" : "2014-06-22T15:29:36+00:00",
        #     "weight" : 210,
        #     "parent_api__id" : "team_profile",
        #     "dd_updated__id" : NumberLong("1431545632159"),
        #     "team__id" : "55714da8-fcaf-4574-8443-59bfb511a524",
        #     "parent_list__id" : "players__list"
        # }

        self.player.preferred_name  = self.o.get('preferred_name', None)

        self.player.birthcity       = self.o.get('birthcity', '')
        self.player.birthcountry    = self.o.get('birthcountry', '')

        self.player.pro_debut       = self.o.get('pro_debut',    '')
        self.player.throw_hand      = self.o.get('throw_hand',   '')
        self.player.bat_hand        = self.o.get('bat_hand',     '')

        self.player.save()

class PlayerStats(DataDenPlayerStats):

    game_model          = Game
    player_model        = Player

    cache_list_unique_name = 'cache_list_player_stats'

    #
    # Set PlayerStatsPitcher when necessary - this gets set
    # just to make the constructor happy and not throw exceptions.
    # But we need to (and we will) dynamically set the right
    # playerstats model based on whether its a pitcher or hitting in parse() method
    player_stats_model  = sports.mlb.models.PlayerStatsHitter

    def __init__(self):
        super().__init__()

        # we are going to use CacheList to save the last (only the last)
        # occurrence of this player in order that we can return
        # the hitter for the linked pbp object to be able to have his stats
        self.cache_list = CacheList(cache=cache, unique_name=self.cache_list_unique_name)

    @staticmethod
    def get_cache_list():
        return CacheList(cache=cache, unique_name=PlayerStats.cache_list_unique_name)

    def parse(self, obj, target=None):
        #     {
        #     "_id" : "cGFyZW50X2FwaV9faWRzdW1tYXJ5Z2FtZV9faWRjODI0NTZhYy1hNGI5LTRjYWYtODEyNC0wYWZhNzRmOWNmMzRob21lX19pZDQzYTM5MDgxLTUyYjQtNGY5My1hZDI5LWRhN2YzMjllYTk2MHBhcmVudF9saXN0X19pZHBsYXllcnNfX2xpc3RpZDAxZWFmZjU5LTliMzQtNDdmZC1hZjY0LTU0YjJlNmYyMjYyOA==",
        #     "first_name" : "Nelson",
        #     "id" : "01eaff59-9b34-47fd-af64-54b2e6f22628",
        #     "jersey_number" : 23,
        #     "last_name" : "Cruz",
        #     "position" : "OF",
        #     "preferred_name" : "Nelson",
        #     "primary_position" : "LF",
        #     "status" : "A",
        #     "parent_api__id" : "summary",
        #     "dd_updated__id" : NumberLong("1431231070789"),
        #     "game__id" : "c82456ac-a4b9-4caf-8124-0afa74f9cf34",
        #     "home__id" : "43a39081-52b4-4f93-ad29-da7f329ea960",
        #     "parent_list__id" : "players__list",
        #     "statistics__list" : {
        #         "hitting__list" : {
        #             "ab" : 3,
        #             "abhr" : 0,
        #             "abk" : 0,
        #             "ap" : 4,
        #             "avg" : 0.667,
        #             "babip" : 0.667,
        #             "bbk" : 0,
        #             "bbpa" : 0.25,
        #             "bip" : 3,
        #             "gofo" : 0,
        #             "iso" : 0.333,
        #             "lob" : 0,
        #             "obp" : 0.75,
        #             "ops" : 1.75,
        #             "pitch_count" : 14,
        #             "rbi" : 1,
        #             "seca" : 0.667,
        #             "slg" : 1,
        #             "xbh" : 1,
        #             "onbase__list" : {
        #                 "bb" : 1,
        #                 "d" : 1,
        #                 "fc" : 0,
        #                 "h" : 2,
        #                 "hbp" : 0,
        #                 "hr" : 0,
        #                 "ibb" : 0,
        #                 "roe" : 0,
        #                 "s" : 1,
        #                 "t" : 0,
        #                 "tb" : 3
        #             },
        #             "runs__list" : {
        #                 "earned" : 1,
        #                 "total" : 1,
        #                 "unearned" : 0
        #             },
        #             "outcome__list" : {
        #                 "ball" : 6,
        #                 "dirtball" : 1,
        #                 "foul" : 0,
        #                 "iball" : 0,
        #                 "klook" : 2,
        #                 "kswing" : 2,
        #                 "ktotal" : 4
        #             },
        #             "outs__list" : {
        #                 "fidp" : 0,
        #                 "fo" : 0,
        #                 "gidp" : 0,
        #                 "go" : 1,
        #                 "klook" : 0,
        #                 "kswing" : 0,
        #                 "ktotal" : 0,
        #                 "lidp" : 0,
        #                 "lo" : 0,
        #                 "po" : 0,
        #                 "sacfly" : 0,
        #                 "sachit" : 0
        #             },
        #             "steal__list" : {
        #                 "caught" : 0,
        #                 "pct" : 0,
        #                 "stolen" : 0
        #             },
        #             "games__list" : {
        #                 "complete" : 0,
        #                 "finish" : 0,
        #                 "play" : 0,
        #                 "start" : 0
        #             }
        #         },
        #         "fielding__list" : {
        #             "a" : 0,
        #             "dp" : 0,
        #             "error" : 0,
        #             "fpct" : 1,
        #             "po" : 4,
        #             "rf" : 0,
        #             "tc" : 4,
        #             "tp" : 0,
        #             "games__list" : {
        #                 "complete" : 0,
        #                 "finish" : 0,
        #                 "play" : 0,
        #                 "start" : 0
        #             }
        #         }
        #     }
        # }


        # "pitching__list" : {
		# 	"bf" : 3,
		# 	"era" : 0,
		# 	"error" : 0,
		# 	"gofo" : 0,
		# 	"ip_1" : 3,
		# 	"ip_2" : 1,
		# 	"k9" : 18,
		# 	"kbb" : 0,
		# 	"lob" : 0,
		# 	"oba" : 0,
		# 	"pitch_count" : 15,
		# 	"whip" : 0,
		# 	"onbase__list" : {
		# 		"bb" : 0,
		# 		"d" : 0,
		# 		"fc" : 0,
		# 		"h" : 0,
		# 		"hbp" : 0,
		# 		"hr" : 0,
		# 		"ibb" : 0,
		# 		"roe" : 0,
		# 		"s" : 0,
		# 		"t" : 0,
		# 		"tb" : 0
		# 	},
		# 	"runs__list" : {
		# 		"earned" : 0,
		# 		"total" : 0,
		# 		"unearned" : 0
		# 	},
		# 	"outcome__list" : {
		# 		"ball" : 5,
		# 		"dirtball" : 0,
		# 		"foul" : 4,
		# 		"iball" : 0,
		# 		"klook" : 4,
		# 		"kswing" : 1,
		# 		"ktotal" : 5
		# 	},
		# 	"outs__list" : {
		# 		"fidp" : 0,
		# 		"fo" : 1,
		# 		"gidp" : 0,
		# 		"go" : 0,
		# 		"klook" : 2,
		# 		"kswing" : 0,
		# 		"ktotal" : 2,
		# 		"lidp" : 0,
		# 		"lo" : 0,
		# 		"po" : 0,
		# 		"sacfly" : 0,
		# 		"sachit" : 0
		# 	},
		# 	"steal__list" : {
		# 		"caught" : 0,
		# 		"stolen" : 0
		# 	},
		# 	"games__list" : {
		# 		"blown_save" : 0,
		# 		"complete" : 0,
		# 		"finish" : 0,
		# 		"hold" : 0,
		# 		"loss" : 0,
		# 		"play" : 1,
		# 		"qstart" : 0,
		# 		"save" : 0,
		# 		"shutout" : 0,
		# 		"start" : 0,
		# 		"svo" : 0,
		# 		"win" : 0
		# 	}
		# },

        # db.player.distinct('primary_position')
        # >>> [ "1B", "LF", "3B", "CF", "RF", "C", "2B", "SP", "RP", "SS", "DH" ]
        o = obj.get_o()

        # stash this player in the cache, for his srid
        player_srid = o.get('id')
        self.cache_list.add(player_srid, o)

        #
        # we do NOT want to parse the objects if they do not have 'statistics__list' key!
        the_stats = o.get('statistics__list', None)
        if the_stats is None:
            return

        fielding = o.get('fielding__list', {}) # info about whether they played/started the game
        game_info = fielding.get('games__list', {})

        #
        # before super().parse()
        # decide whether this is a hitter or pitcher here, based on 'position'
        arch_position = o.get('position')  # ['IF','OF','C','P','DH']
        if arch_position == 'P':
            self.player_stats_model  = sports.mlb.models.PlayerStatsPitcher
            super().parse( obj, target )
            # after calling super().parse() check if self.ps is None, return if it is
            if self.ps is None:
                return

            # collect pitching stats
            statistics = o.get('statistics__list', {}) # default will useful if it doenst exist

            pitching = statistics.get('pitching__list', {})

            games   = pitching.get('games__list', {})
            onbase  = pitching.get('onbase__list', {})
            runs    = pitching.get('runs__list', {})
            steals  = pitching.get('steal__list', {})
            outs    = pitching.get('outs__list', {})

            self.ps.ip_1    = pitching.get('ip_1', 0.0) # outs, basically. for 1 inning pitched == 3 (4 possible?)
            self.ps.ip_2    = pitching.get('ip_2', 0.0) # 1 == one inning pitched
            self.ps.win     = bool( games.get('win', 0) )
            self.ps.loss    = bool( games.get('loss', 0) )
            self.ps.qstart  = bool( games.get('qstart', 0) )
            self.ps.ktotal  = outs.get('ktotal', 0)
            self.ps.er      = runs.get('earned', 0)  # earned runs allowed
            self.ps.r_total = runs.get('total', 0)   # total runs allowed (earned and unearned)
            self.ps.h       = onbase.get('h', 0)     # hits against
            self.ps.bb      = onbase.get('bb', 0)    # walks against
            self.ps.hbp     = onbase.get('hbp', 0)   # hit batsmen
            self.ps.cg      = bool( games.get('complete', 0) ) # complete game
            self.ps.cgso    = bool( games.get('shutout', 0) ) and self.ps.cg # complete game shut out
            self.ps.nono    = bool( self.ps.h ) and self.ps.cg # no hitter if hits == 0, and complete game

        else:
            # its a hitter
            self.player_stats_model  = sports.mlb.models.PlayerStatsHitter
            super().parse( obj, target )
            if self.ps is None:
                return # if super().parse() doesnt create this, get out of here

            statistics = o.get('statistics__list', {})

            hitting = statistics.get('hitting__list', {}) # default will useful if it doenst exist

            onbase  = hitting.get('onbase__list', {})
            runs    = hitting.get('runs__list', {})
            steals  = hitting.get('steal__list', {})
            outs    = hitting.get('outs__list', {})

            self.ps.bb  = onbase.get('bb', 0)
            self.ps.s   = onbase.get('s', 0)
            self.ps.d   = onbase.get('d', 0)
            self.ps.t   = onbase.get('t', 0)
            self.ps.hr  = onbase.get('hr', 0)
            self.ps.rbi = hitting.get('rbi', 0)
            self.ps.r   = runs.get('total', 0)
            self.ps.hbp = onbase.get('hbp', 0)
            self.ps.sb  = steals.get('stolen', 0)
            self.ps.cs  = steals.get('caught', 0)

            self.ps.ktotal  = outs.get('ktotal', 0)

            self.ps.ab  = hitting.get('ab', 0)
            self.ps.ap  = hitting.get('ap', 0)
            self.ps.lob = hitting.get('lob', 0)
            self.ps.xbh = hitting.get('xhb', 0)

        #
        # hitters and pitchers both get these pieces of info
        self.ps.played  = bool( game_info.get('play', 0) )
        self.ps.started = bool( game_info.get('start', 0) )

        self.ps.save() # commit changes

class AbstractManager(object):

    # exceptions for validity checking
    class InvalidReducer(Exception): pass
    class InvalidShrinker(Exception): pass

    # must be set by child classes
    reducer_class = None
    shrinker_class = None

    def __init__(self, raw_data):
        """
        adds the key values in the 'stats' dict into the
        """
        if self.reducer_class is None:
            raise self.InvalidReducer('"reducer_class" cant be None')
        if self.shrinker_class is None:
            raise self.InvalidShrinker('"shrinker_class" cant be None')

        self.raw_data = raw_data

    def get_data(self, additional_data=None):
        # reduce the raw data - pop() unwanted fields
        reduced = self.reducer_class(self.raw_data).reduce()
        # shrink the reduced data
        shrunk = self.shrinker_class(reduced).shrink()

        # add_data should be called after
        return self.add_data(shrunk, additional_data)

    def add_data(self, base_data, additional=None):
        if additional is not None:
            for k,v in additional.items():
                # add this key:value of additional data,
                # but only if the field doesnt exist already in orig
                if base_data.get(k, None) is None:
                    base_data[k] = v
        return base_data

class AbstractStatReducer(object):
    """
    pop()'s keys out of dictionaries for the strict purpose
    or removing superfluous data right before we pusher the data
    to cut down on packet size.
    """

    class InvalidDataType(Exception): pass

    # inheriting classes should set this to a list of string field names to remove
    remove_fields = []

    str_true = "true"
    str_false = "false"
    str_bools = [str_true, str_false]

    def __init__(self, data):
        if not isinstance(data, dict):
            raise self.InvalidDataType('"data" must be of type "dict"')
        self.data = data # save the original data
        self.reduced = self.data.copy() # clone the data coming in

    def str2bool(self, val):
        if not isinstance(val, str):
            return val

        if val == self.str_false:
            return False
        elif val == self.str_true:
            return True
        else:
            return False # default !?

    def get_internal_data(self):
        return self.reduced

    def pre_reduce(self):
        """ you should override this in child class if you want to perform customizations """
        pass # by default does nothing, side effects nothing

    def reduce(self):
        self.pre_reduce()

        # remove keys we dont care about, and return the internal data
        for field in self.remove_fields:
            try:
                # this actually removes the fields from the dict!
                self.reduced.pop(field)
            except:
                pass
        return self.reduced

class AbstractShrinker(object):

    fields = None

    def __init__(self, data):
        self.data = data
        self.shrinked = None

    def shrink(self):
        """ return shrunk data """
        self.shrinked = self.data.copy()
        for old_field, new_field in self.fields.items():
            try:
                val = self.shrinked.pop(old_field)
            except KeyError:
                #print('old_field popped: %s' % str(old_field))
                continue # old_field didnt exist. dont hold it against them
            #print('field: %s, val: %s' % (str(old_field), str(val)))
            if val is None:
                continue # dont add a random default value if the field doesnt exist
            self.shrinked[new_field] = val
        #
        return self.shrinked

class AtBatReducer(Reducer):

    remove_fields = [
        '_id',
        'errors__list',
        'parent_api__id',
        'pitchs',
        'game__id',
        'id',
        'created_at',
        'updated_at',
        'runners__list',
        'count__list',
        'flags__list',
        'fielders__list',
        'status',
        'pitcher',
        'hit_location',
        'hit_type',
    ]

class AtBatShrinker(Shrinker):

    fields = {
        'at_bat__id' : 'srid',
        'dd_updated__id' : 'ts',
        'hitter_id' : 'srid_hitter',
        'outcome_id' : 'oid',
        'description' : 'oid_description',
    }

class AtBatManager(AbstractManager):

    reducer_class = AtBatReducer
    shrinker_class = AtBatShrinker

class ZonePitchReducer(AbstractStatReducer):

    remove_fields = [
        '_id',
        'parent_api__id',
        'game__id',
        'id',
        'at_bat__id',
        'pitch__id',
        'dd_updated__id',
        'hitter_hand',
        'pitcher_hand',
        'pitch_count',   # we add our own thing -- this is overall pitch count anyways
    ]

class ZonePitchShrinker(AbstractShrinker):
    """ reduce() then shrink the fields of a ZonePitch """

    fields = {
        'pitch_count'           : 'tpc',
        'at_bat_pitch_count'    : 'pc',
        'pitch_speed'           : 'mph',
        'pitch_type'            : 't',
        'pitch_zone'            : 'z',
    }

class ZonePitchSorter(object):
    """
    this object will sort the zone pitches.

    it will also remove earlier duplicates (and use the most recent/updated pitch).
    """

    at_bat_pitch_count = 'at_bat_pitch_count'

    def __init__(self, zone_pitches, at_bat):
        self.zone_pitches = zone_pitches
        self.at_bat = at_bat
        #self.pitchs = self.at_bat.get('pitchs', None)
        self.srid_pitchs = None
        self.pitchs = self.at_bat.get('pitchs', None)
        if self.pitchs is None:
            # the at bat must have a pitch in it (the 1st one, thats not in a list yet!)
            found_pitch_srid = self.at_bat.get('pitch')
            if found_pitch_srid is None:
                err_msg = 'ZonePitchSorter didnt expect found_pitch_srid (a single one in the at, not in a list) to be None!'
                print(err_msg)
                raise Exception(err_msg)
            self.srid_pitchs = [ found_pitch_srid ]
        else:
            # pitchs was not none, and we can get the srids
            self.srid_pitchs = [ v.get('pitch') for v in self.pitchs ]
        # self.srid_pitchs shouldnt be None here now:
        if self.srid_pitchs is None:
            err_msg = 'ZonePitchSorter self.srid_pitchs was None at end of __init__  (thats bad)'
            print(err_msg)
            raise Exception(err_msg)

    def sort(self):
        """ reduce, sort, and shrink the zone_pitches and return a list """
        pitch_order_map = {}
        #for i, pitch_dict in enumerate(self.pitchs):
        for i, pitch_srid in enumerate(self.srid_pitchs):
            # pitch_srid = pitch_dict.get('pitch')
            pitch_order_map[pitch_srid] = i + 1   # map of srid -> atbat pitch index
        #print('pitch_order_map:', str(pitch_order_map))
        # we will remove pitch__ids we've used from this.
        # if there are pitch srids remaining at the end, those are ones we missed, and we should make note!
        unused_pitches = list(pitch_order_map.keys())
        # now using the pitch_order_map - adding the pitches in order
        # will have hte effect of taking the most recent zone pitch
        # which should leave us with no duplicates.
        indexed_pitch_map = {}
        for zone_pitch in self.zone_pitches:
            try:
                #print('    zone_pitch:', str(zone_pitch))
                retrieve_zp_id = zone_pitch.get('pitch__id', None)
                if retrieve_zp_id is None:
                    #print('        it didnt have one')
                    continue # not having a pitch__id could mean it was simply a pickoff attempt
                at_bat_idx = pitch_order_map[retrieve_zp_id] # TODO - this raises exception sometimes

                # remove the references to pitches srids we used
                while True:
                    try:
                        unused_pitches.remove(retrieve_zp_id)
                    except ValueError:
                        break # all copies of that srid are gone

            except KeyError:
                #print("known Exception KeyError! on at_bat_idx = pitch_order_map[zone_pitch.get('pitch__id')]")
                #raise Exception('')
                #print('at_bat:', str(self.at_bat))
                #print('pitchs:', str(self.pitchs))
                #print('zone_pitches:', str(self.zone_pitches))
                pass

            zone_pitch[self.at_bat_pitch_count] = at_bat_idx     # setting at_bat_idx here doesnt get pushed back into cache!
            indexed_pitch_map[at_bat_idx] = zone_pitch
            # TODO i need to add the at bat index to the zone_pitch json!

        #
        ordered_zps = OrderedDict(sorted(indexed_pitch_map.items()))
        #print('leftover unused_pitches:', str(unused_pitches))
        return [ zp for zp in ordered_zps.values() ]

class ZonePitchManager(AbstractManager):
    """
    note: this class does not inherit AbstractManager.

    sort, reduce, and shrink the zone pitches and return a list of them
    """

    def __init__(self, zone_pitches, at_bat):
        self.zone_pitches = zone_pitches
        self.at_bat = at_bat

    def get_data(self, additional_data=None):
        """ override parent get_data() to perform on all the list items """
        sorter = ZonePitchSorter(self.zone_pitches, self.at_bat)
        sorted_zone_pitches = sorter.sort()

        reduced_and_shrunk_zone_pitches = []
        for zp in sorted_zone_pitches:
            reducer = ZonePitchReducer(zp)
            reduced_zp = reducer.reduce()
            shrinker = ZonePitchShrinker(reduced_zp)
            shrunk_zp = shrinker.shrink()
            reduced_and_shrunk_zone_pitches.append(shrunk_zp)
            for rszp in reduced_and_shrunk_zone_pitches:
                self.add_data(rszp, additional_data)
        return reduced_and_shrunk_zone_pitches

class RunnerReducer(AbstractStatReducer):

    remove_fields = [
        '_id',
        'at_bat__id',
        'dd_updated__id',
        'first_name',
        'game__id',
        'jersey_number',
        'parent_api__id',
        'parent_list__id',
        'pitch__id',
    ]

    field_out = 'out'

    def pre_reduce(self):
        d = self.get_internal_data()
        out_as_str = d.get(self.field_out, None)
        #print('out_as_str:', str(out_as_str))
        d[self.field_out] = self.str2bool(out_as_str)
        #print('d:', str(d))
        self.data = d

        super().pre_reduce()

class RunnerShrinker(AbstractShrinker):

    fields = {
        'id'                : 'srid',
        'starting_base'     : 'start',
        'ending_base'       : 'end',
        'outcome_id'        : 'oid',
        'preferred_name'    : 'fn',
        'last_name'         : 'ln',
    }

class RunnerManager(AbstractManager):

    def __init__(self, runners):
        self.runners = runners

    def get_data(self, additional_data=None):
        reduced_and_shrunk_runners = []
        for runner in self.runners:
            rr = RunnerReducer(runner)
            reduced_runner = rr.reduce()
            rs = RunnerShrinker(reduced_runner)
            shrunk_runner = rs.shrink()
            reduced_and_shrunk_runners.append(shrunk_runner)
            for rsr in reduced_and_shrunk_runners:
                self.add_data(rsr, additional_data)
        return reduced_and_shrunk_runners

class PitchPbpReducer(AbstractStatReducer):

    class FlagsReducer(AbstractStatReducer):
        """
        parent class is only used for its 'pre_reduce' method
        so we can cast the string booleans to actual JSON booleans
        """
        key = 'flags__list'

        def pre_reduce(self):
            # before we start popping off keys we dont care about get the stats we do care about
            flags = self.get_internal_data()

            # loop thru all fields, and convert "true" to True, and "false" to False
            # so when we convert it to JSON the real booleans go out
            for k,v in flags.items():
                flags[k] = self.str2bool(v)

            # add onbase_list stats back in
            self.reduced = flags

            # make sure to call super at the end
            super().pre_reduce()

    remove_fields = [
        '_id',
        'errors__list',
        'created_at',
        'updated_at',
        'fielders__list',
        'runners__list',    # leave runners_list in there for debugging
        'hit_location',
        'hit_type',
        'parent_api__id',
        'status',
    ]

    def reduce(self):
        #print('in here')
        d = self.get_internal_data()
        flags = d.get(self.FlagsReducer.key, None)
        if flags is not None:
            flags_reducer = self.FlagsReducer(flags)
            #print('flags:', str(flags))
            d[self.FlagsReducer.key] = flags_reducer.reduce()
            #print('d:', str(d))
        return super().reduce()

class PitchPbpShrinker(AbstractShrinker):
    """ reduce() then shrink the fields of a ZonePitch """

    class CountShrinker(AbstractShrinker):

        key = 'count'

        fields = {
            'strikes'       : 'k',
            'balls'         : 'b',
            'pitch_count'   : 'pc',
        }

    fields = {
        'dd_updated__id'    : 'ts',
        'id'                : 'srid',
        'at_bat__id'        : 'srid_at_bat',
        'count__list'       : 'count',
        'flags__list'       : 'flags',
        'game__id'          : 'srid_game',
        'pitcher'           : 'srid_pitcher',
        'outcome_id'        : 'oid',
    }

    def shrink(self):
        data = super().shrink()
        k = self.CountShrinker.key
        if k in data.keys():
            data[k] = self.CountShrinker(data[k]).shrink()
        return data

class PitchPbpManager(AbstractManager):

    reducer_class = PitchPbpReducer
    shrinker_class = PitchPbpShrinker

class HittingListToStr(object):
    """
    format a string based on the 'hitting__list' in dataden player hitter stats object
    into something like:

        "1 for 3 (HR, B)"

    """

    DESCRIPTION_NO_AT_BATS = '0 for 0'

    def __init__(self, hitting_list):
        #         "hitting__list" : {
        #             "ab" : 3,
        #             "abhr" : 0,
        #             "abk" : 0,
        #             "ap" : 4,
        #             "avg" : 0.667,
        #             "babip" : 0.667,
        #             "bbk" : 0,
        #             "bbpa" : 0.25,
        #             "bip" : 3,
        #             "gofo" : 0,
        #             "iso" : 0.333,
        #             "lob" : 0,
        #             "obp" : 0.75,
        #             "ops" : 1.75,
        #             "pitch_count" : 14,
        #             "rbi" : 1,
        #             "seca" : 0.667,
        #             "slg" : 1,
        #             "xbh" : 1,
        #             "onbase__list" : {
        #                 "bb" : 1,
        #                 "d" : 1,
        #                 "fc" : 0,
        #                 "h" : 2,
        #                 "hbp" : 0,
        #                 "hr" : 0,
        #                 "ibb" : 0,
        #                 "roe" : 0,
        #                 "s" : 1,
        #                 "t" : 0,
        #                 "tb" : 3
        #             },
        #             "runs__list" : {
        #                 "earned" : 1,
        #                 "total" : 1,
        #                 "unearned" : 0
        #             },
        #             "outcome__list" : {
        #                 "ball" : 6,
        #                 "dirtball" : 1,
        #                 "foul" : 0,
        #                 "iball" : 0,
        #                 "klook" : 2,
        #                 "kswing" : 2,
        #                 "ktotal" : 4
        #             },
        #             "outs__list" : {
        #                 "fidp" : 0,
        #                 "fo" : 0,
        #                 "gidp" : 0,
        #                 "go" : 1,
        #                 "klook" : 0,
        #                 "kswing" : 0,
        #                 "ktotal" : 0,
        #                 "lidp" : 0,
        #                 "lo" : 0,
        #                 "po" : 0,
        #                 "sacfly" : 0,
        #                 "sachit" : 0
        #             },
        #             "steal__list" : {
        #                 "caught" : 0,
        #                 "pct" : 0,
        #                 "stolen" : 0
        #             },
        #             "games__list" : {
        #                 "complete" : 0,
        #                 "finish" : 0,
        #                 "play" : 0,
        #                 "start" : 0
        #             }
        #         },
        self.data = hitting_list

    def get_description(self):
        if self.data is None or self.data == {}:
            return self.DESCRIPTION_NO_AT_BATS
        # ab, h, R, RBI, B, HBP, HR, 2B, 3B, SB
        stat_desc_list = []
        onbase_list = self.data.get('onbase__list', {})
        runs_list = self.data.get('runs__list', {})
        steal_list = self.data.get('steal__list', {})
        at_bats = self.data.get('ab')
        hits = onbase_list.get('h')
        stat_desc_list.append( self.format_stat( 'R', runs_list.get('total') ) )
        stat_desc_list.append( self.format_stat( 'RBI', self.data.get('rbi') ) )
        stat_desc_list.append( self.format_stat( 'B', onbase_list.get('bb') ) )
        stat_desc_list.append( self.format_stat( 'HBP', onbase_list.get('hbp') ) )
        stat_desc_list.append( self.format_stat( 'HR',  onbase_list.get('hr') ) )
        stat_desc_list.append( self.format_stat( '2B', onbase_list.get('d') ) )
        stat_desc_list.append( self.format_stat( '3B', onbase_list.get('t') ) )
        stat_desc_list.append( self.format_stat( 'SB', steal_list.get('stolen') ) )

        # generaet the return string
        desc = '%s for %s' % (hits, at_bats)

        stats_list = [x for x in stat_desc_list if x != '']
        if len(stats_list) > 0:
            suffix = ' (%s)' % ','.join(stats_list)
            desc += suffix
        return desc

    def format_stat(self, name, value):
        if value is None or value == 0:
            return ''
        elif value == 1:
            return name

        return '%s %s' % (int(value), name)

class PlayerStatsToStr(HittingListToStr):

    def __init__(self, player_stats_instance):
        super().__init__(player_stats_instance)

    def get_description(self):
        if self.data is None or self.data == {}:
            return self.DESCRIPTION_NO_AT_BATS

        # ab, h, R, RBI, B, HBP, HR, 2B, 3B, SB
        stat_desc_list = []
        singles = self.data.s
        doubles = self.data.d
        triples = self.data.t
        homers  = self.data.hr
        at_bats = self.data.ab
        hits = singles + doubles + triples + homers
        stat_desc_list.append( self.format_stat( 'R',   self.data.r ) )
        stat_desc_list.append( self.format_stat( 'RBI', self.data.rbi ) )
        stat_desc_list.append( self.format_stat( 'B',   self.data.bb ) )
        stat_desc_list.append( self.format_stat( 'HBP', self.data.hbp ) )
        stat_desc_list.append( self.format_stat( 'HR',  homers ) )
        stat_desc_list.append( self.format_stat( '2B',  doubles ) )
        stat_desc_list.append( self.format_stat( '3B',  triples ) )
        stat_desc_list.append( self.format_stat( 'SB',  self.data.sb ) )

        # generaet the return string
        desc = '%s for %s' % (hits, at_bats)

        stats_list = [x for x in stat_desc_list if x != '']
        if len(stats_list) > 0:
            suffix = ' (%s)' % ','.join(stats_list)
            desc += suffix
        return desc

class QuickCache(object):
    """
    uniquely caches objects if they have an
    identifier field and a unix timestamp.

    Redis cache is used by default
    """

    class BytesIsNoneException(Exception): pass

    name = 'QuickCache'
    timeout_seconds = 60 * 5

    extra_key = '--%s--'
    # key_prefix_pattern = name + '--%s--'            # ex: 'QuickCache--%s--'
    # scan_pattern = key_prefix_pattern + '*'         # ex: 'QuickCache--%s--*'
    # key_pattern = key_prefix_pattern + '%s'         # ex: 'QuickCache--%s--%s'

    field_id = 'id'
    field_timestamp = 'dd_updated__id'

    def __init__(self, data=None, stash_now=True, override_cache=None):
        #self.key_prefix_pattern = self.name + '--%s--'            # ex: 'QuickCache--%s--'
        self.key_prefix_pattern = self.name + self.extra_key
        self.scan_pattern = self.key_prefix_pattern + '*'         # ex: 'QuickCache--%s--*'
        self.key_pattern = self.key_prefix_pattern + '%s'         # ex: 'QuickCache--%s--%s'

        self.cache = override_cache
        if self.cache is None:
            # default: use django default cache
            # TODO fix this hack

            self.cache = get_redis_instance()

        # immediately cache it based on 'stash_now' bool
        if data is not None and stash_now == True:
            self.stash(data)

    def get_key(self, ts, gid):
        key = self.key_pattern % (ts, gid)
        return key

    def scan(self, ts):
        """ return the keys for objects matching the same cache and timestamp 'ts' """

        #redis = Redis()
        redis = get_redis_instance()

        keys = []
        pattern = self.scan_pattern % ts
        print('scan pattern:', pattern)
        for k in redis.scan_iter(pattern):
            keys.append(k)
        return keys

    def add_to_cache_method(self, k, data):
        return self.cache.set(k, data, self.timeout_seconds)

    def bytes_2_dict(self, bytes):
        if bytes is None:
            err_msg = 'bytes_2_dict(): bytes is None!'
            raise self.BytesIsNoneException(err_msg)
        return literal_eval(bytes.decode())

    def validate_stashable(self, data):
        if not isinstance(data, dict):
            err_msg = 'data must be an instance of dict'
            raise Exception(err_msg)

    #@timeit
    def fetch(self, ts, gid):
        k = self.get_key(ts, gid)
        ret_val = None
        try:
            ret_val = self.bytes_2_dict(self.cache.get(k))
        except self.BytesIsNoneException:
            pass
        return ret_val

    #@timeit
    def stash(self, data):
        #
        self.validate_stashable(data)

        #
        ts = data.get('dd_updated__id')
        gid = data.get('id')
        k = self.get_key(ts, gid)

        #
        ret_val = self.add_to_cache_method(k, data)
        #print('stashed: key', str(k), ':', str(data))
        return ret_val

class QuickCacheList(QuickCache):
    """
    this class adds dict() instances to a redis key
    whose value is actually a list (ie: not a single object).
    """

    name = 'QuickCacheList'

    # this is a sneaky (weird) way to inherit
    # the parent class with minimal changes
    extra_key = '--'

    # we will likely  want to override this field
    # in inheriting classes, but dont do it here
    #field_id = 'id'

    def add_to_cache_method(self, k, data):
        """
        :param k: redis key
        :param data: add this dict to the redis list
        :return: number of total dicts in the list after we add this one
        """
        return self.cache.rpush(k, data)

    #@timeit
    def stash(self, data):
        """ adds the data to its corresponding list in the cache """
        self.validate_stashable(data)

        #
        gid = data.get(self.field_id)
        k = self.get_key(gid)

        #
        ret_val = self.add_to_cache_method(k, data)
        #print('stashed: key', str(k), ':', str(data))
        return ret_val

    def get_key(self, gid):
        key = self.key_pattern % gid
        return key

    #@timeit
    def fetch(self, gid):
        # get a list of dicts from the key
        k = self.get_key(gid)
        l = self.cache.lrange(k, 0, -1) # start with 0, get thru last!
        return [ self.bytes_2_dict(dict_bytes) for dict_bytes in l ]

class PitchPbp(DataDenPbpDescription):
    """
    given an object whose namespace, parent api is a target like:
     ('mlb.pitch','pbp') this object is capable of emitting
     the play by play information with send()
    """

    # exceptions
    class AtBatNotFoundException(Exception): pass
    class MultipleAtBatObjectsFoundException(Exception): pass
    class MissingCachedObjectException(Exception): pass

    # the primary objects of a linked object are cached with these classes:
    class AtBatCache(QuickCache):
        name = 'AtBat'
        # at_bat will be cached by the at bat srid

    class PitchCache(QuickCache):
        name = 'Pitch'
        # pitch will be cached by the pitch srid

    class ZonePitchCacheList(QuickCacheList):
        name = 'ZonePitches'
        field_id = 'at_bat__id' # cache zone pitches by at_bat srid

    class RunnerCacheList(QuickCacheList):
        name = 'Runners'
        field_id = 'pitch__id'  # cache runners based on pitch srid

    cache_classes = [AtBatCache, PitchCache, ZonePitchCacheList, RunnerCacheList]

    game_model              = Game
    pbp_model               = Pbp
    portion_model           = GamePortion
    pbp_description_model   = PbpDescription
    #
    player_stats_model      = sports.mlb.models.PlayerStatsPitcher
    pusher_sport_pbp        = push.classes.PUSHER_MLB_PBP
    pusher_sport_stats      = push.classes.PUSHER_MLB_STATS

    at_bat_srid_field       = 'at_bat__id'

    # field name of the pitch when it goes out as linked pbp data
    pitch_pbp       = 'pbp'

    # fields of the reconstructed data
    pitch           = 'pitch'
    at_bat          = 'at_bat'
    at_bat_stats    = 'at_bat_stats'
    zone_pitches    = 'zone_pitches'
    runners         = 'runners'
    stats           = 'stats'

    def __init__(self, raw=False):
        """
        :param raw: False by default. set to True for testing/debugging to see the un-reduced, un-shrunk data.
                    *warning* setting raw=True also bypasses the send() method. (calling send() will have no effect).
        :return:
        """
        super().__init__()
        self.player_stats_pitcher_model  = sports.mlb.models.PlayerStatsPitcher      # mlb pitcher stats
        self.player_stats_hitter_model   = sports.mlb.models.PlayerStatsHitter       # mlb hitter stats

        self.at_bat_object = None

        # updated when an object is parsed
        self.srid_pitch = None
        self.srid_at_bat = None
        self.ts = None

        # False by default.
        # True will disable reducers, shrinkers, and send() method
        self.raw = raw

        # the dict used for the reconstruction.
        self.data = {
            self.pitch : None,
            self.at_bat : None,
            self.at_bat_stats : None,
            self.zone_pitches : None,
            self.runners : None,
            self.stats : None,
        }

    def send(self):
        #
        # TODO - take care of caching i think so we dont double send but im not sure...
        # from dataden.util.hsh import Hashable
        # In [1]: h = Hashable({})
        # In [2]: h.hsh()
        # In [3]: h.hsh()
        # Out[3]: '191fa51276db527e432472e94a1433f3ced3b85ffbb01e73c44888d642cc4ac8'

        # skip send() method entirely if 'raw' is True!
        if self.raw == True:
            return

        if self.ts is None:
            err_msg = 'send() self.ts is None. make sure parse_xxxx() methods set it!'
            raise Exception(err_msg)

        raw_requirements = None
        try:
            if self.srid_pitch is None and self.srid_at_bat is None:
                # this should simply return out of the method without doing anything
                # because weve tried to call send() without a
                # one of the two necessary objects required to
                # attempt to send the mlb linked data
                part1 = 'send() self.srid_pitch and self.srid_at_bat are both None!'
                part2 = ' one of the two objects are required at a minimum.'
                err_msg = '%s %s' % (part1, part2)
                print(err_msg)
                #raise Exception(err_msg)
                return

            elif self.srid_pitch is not None:
                raw_requirements = self.reconstruct_from_pitch(self.ts, self.srid_pitch)

            else:
                raw_requirements = self.reconstruct_from_at_bat(self.ts, self.srid_at_bat)

        except self.MissingCachedObjectException as e:
            #print('dont have complete object yet', str(e))
            return None

        print('')
        print('')
        print('raw_requirements:', str(raw_requirements))
        print('')
        linked_pbp = self.build_linked_pbp_stats_data(raw_requirements)

        hashable = Hashable(raw_requirements)                       # these 4 lines are from super().send()
        primary_object_hash = hashable.hsh()                        # 2
        # self.delete_cache_tokens(player_stats)                    # 3
        # data = self.build_linked_pbp_stats_data( player_stats )   # 4

        # TODO right about here is where we need to check the cache to see if we can send this linked object!
        r = get_redis_instance()
        pitch = raw_requirements.get('pitch')
        ts = pitch.get('dd_updated__id')
        id = pitch.get('id')
        send_hsh = 'mlblinkedpbp-%s-%s' % (ts, id)
        print('send_hsh:', str(send_hsh))
        if r.get(send_hsh) is not None:
            print('already sent linked object')
            pass
        else:
            # if the cached hash value doesnt exist, we need to send it
            print('sending')
            r.set(send_hsh, True, 60*60*12)
            push.classes.DataDenPush( self.pusher_sport_pbp, 'linked', hash=send_hsh ).send( linked_pbp )

            #debug
            print('')
            print('linked_pbp:', str(linked_pbp))
            print('')
            print('')

    def reconstruct_from_pitch(self, ts, srid_pitch):
        return self.reconstruct(ts, srid_pitch)

    def reconstruct_from_at_bat(self, ts, srid_at_bat):
        at_bat = self.AtBatCache().fetch(ts, srid_at_bat)
        if at_bat is None:
            err_msg = 'reconstruct_from_at_bat() - ts, srid_at_bat: %s, %s' % (ts, srid_at_bat)
            raise self.MissingCachedObjectException(err_msg)
        # get the srid of the last pitch in the pitchs list
        srid_pitch = None
        try:
            pitchs = at_bat.get('pitchs', [])
            srid_pitch = pitchs[-1].get('pitch')
        except IndexError:
            srid_pitch = at_bat.get('pitch')

        return self.reconstruct(ts, srid_pitch)

    @timeit
    def reconstruct(self, ts, srid_pitch):
        # zeroes out the internal constructed data
        for k in self.data.keys():
            self.data[k] = None

        # now get the pitch (although if its None, we definitely dont have everything yet
        found_pitch = self.PitchCache().fetch(ts, srid_pitch)
        if found_pitch is None:
            raise self.MissingCachedObjectException('pitch')

        pid = found_pitch.get('id')
        abid = found_pitch.get('at_bat__id')
        zps = self.ZonePitchCacheList().fetch(abid) # get zone pitches for the at bat
        # if zps == []:
        #     raise Exception('ZonePitchCacheList zone_pitches is empty! This means we dont have the zone_pitch for the pitch(pbp) object! go no further')
        rnrs = self.RunnerCacheList().fetch(pid)    # get runners for the pitch

        # a) get the at_bat, using the srid from the pitch
        found_ab = self.AtBatCache().fetch(ts, abid) # could also use pitch.get() and extract ts
        if found_ab is None:
            raise self.MissingCachedObjectException('at_bat')

        # b) find the zone pitches
        pitchs = found_ab.get('pitchs', None)
        if pitchs is None:
            # the at bat must have a pitch in it (the 1st one, thats not in a list yet!)
            found_pitch_srid = found_ab.get('pitch')
            if found_pitch_srid is None:
                err_msg = 'didnt expect found_pitch_srid (a single one in the at, not in a list) to be None!'
                print(err_msg)
                raise Exception(err_msg)
            srid_pitchs = [ found_pitch_srid ]
        else:
            # pitchs was not none, and we can get the srids
            srid_pitchs = [ v.get('pitch') for v in pitchs ]

        # raises MissingCachedObjectException
        found_zone_pitches = self.get_all_newest(srid_pitchs, zps, 'pitch__id', 'dd_updated__id')
        # print("found_zone_pitches = self.get_all_newest(srid_pitchs, zps, 'pitch__id', 'dd_updated__id')")
        print('found_zone_pitches:', str(found_zone_pitches))
        if len(found_zone_pitches) == 0:
            raise self.MissingCachedObjectException('[found_]zone_pitches was 0!')

        # c) find the runners
        rlist = found_pitch.get('runners__list', [])
        if isinstance(rlist, dict):
            rlist = [rlist] # convert from dict to list if it was a single item
        srid_runners = [ r.get('runner') for r in rlist ]
        # raises MissingCachedObjectException
        found_runners = self.get_all_newest(srid_runners, rnrs, 'id', 'dd_updated__id', match_ts=ts)

        # ok ... i think if we have everything, we have everthing!
        # data = {
        #     'pitch'         : found_pitch,
        #     'at_bat'        : found_ab,
        #     'zone_pitches'  : found_zone_pitches,
        #     'runners'       : found_runners,
        # }
        self.data[self.pitch]           = found_pitch
        self.data[self.at_bat]          = found_ab
        self.data[self.zone_pitches]    = found_zone_pitches
        self.data[self.runners]         = found_runners
        return self.data

    def get_all_newest(self, known_srids, cached_objects, field_srid, field_ts, match_ts=None):
        found_objects = []
        for srid in known_srids:
            found_object = None
            for obj in cached_objects:
                srids_match = srid == obj.get(field_srid)
                obj_ts = obj.get(field_ts)
                found_object_ts = 0
                if found_object is not None:
                    found_object_ts = found_object.get(field_ts)
                is_newer_ts = obj_ts >= found_object_ts
                # if the param 'match_ts' is not None, disallow
                # matches with different timestamps altogether
                if match_ts is not None and obj_ts != match_ts:
                    continue
                # in our search of the whole list,
                # lets use the newest one based on dd timestamp
                if srids_match and is_newer_ts:
                    found_object = obj
            # if we found it, append to the list
            if found_object is not None:
                found_objects.append(found_object)
            else:
                err_msg = 'known_srids had %s but our cached object list didnt (yet)' % srid
                print(err_msg)
                raise self.MissingCachedObjectException(err_msg)
        return found_objects

    def stash_at_bat(self, at_bat):
        return self.AtBatCache(at_bat)

    def stash_pitch(self, pitch):
        self.srid_pitch = pitch.get('id') # TODO the other stash_xxx() methods will update srid_pitch different ways!
        return self.PitchCache(pitch)

    def stash_zone_pitch(self, zone_pitch):

        return self.ZonePitchCacheList(zone_pitch)

    def stash_runner(self, runner):
        return self.RunnerCacheList(runner)

    def __update_sendability(self, obj, target):

        if target == ('mlb.pitch','pbp'):       # TODO consolidate the targets into DataDenMlb parser!
            self.stash_pitch(self.o)
            # set the pitch srid
            self.srid_pitch = self.o.get('id')

        elif target == ('mlb.at_bat','pbp'):
            self.stash_at_bat(self.o)
            # set the at bats srid
            self.srid_at_bat = self.o.get('id')

        elif target == ('mlb.pitcher','pbp'):
            self.stash_zone_pitch(self.o)
            # set the internal at bat id from the zone pitch data,
            # since they are grouped by at bat
            self.srid_at_bat = self.o.get('at_bat__id')

        elif target == ('mlb.runner','pbp'):
            self.stash_runner(self.o)
            # pitch srid comes from 'pitch__id' field of a runner,
            # since runners are grouped by pitch
            self.srid_pitch = self.o.get('pitch__id')

        else:
            err_msg = 'unknown target %s in __update_sendability()' % str(target)
            raise Exception(err_msg)

        # set the internal timestamp field so we can link this object to others
        self.ts = obj.get('dd_updated__id')

    def parse(self, obj, target): # =None):
        """
        the object must first be parsed before send() can be called

        :param obj: a dataden.watcher.OpLogObj object
        :param target: required, the trigger of the obj
        """

        self.original_obj = obj
        self.srid_finder = SridFinder(obj.get_o()) # get the data from the oplogobj
        self.o = obj.get_o() # we didnt call super so we should do this

        # check if we have all the necessary things to build the object!
        self.__update_sendability(self.o, target)

        #
        self.send()

    def build_linked_pbp_stats_data(self, requirements):
        """
        override default method from parent to add the linked objects
        """
        additional_pitch_data = {'oid_fp':1.7} # TODO for testing
        pitch = requirements.get(self.pitch)
        srid_pitcher = pitch.get('pitcher')
        at_bat = requirements.get(self.at_bat)
        srid_game = at_bat.get('game__id')
        srid_at_bat_hitter = at_bat.get('hitter_id')
        zone_pitches = requirements.get(self.zone_pitches)
        runners = requirements.get(self.runners)
        additional_runner_data = {'oid_fp':3.7} # TODO for testing
        srid_runners = [ r.get('id') for r in runners ] # not pulled from original data, but i think its fine
        # player_stats
        player_stats = self.find_player_stats(srid_game, srid_pitcher, srid_at_bat_hitter, srid_runners)
        # at_bat_stats
        at_bat_player_stats_hitter = self.find_at_bat_hitter_player_stats(srid_game, srid_at_bat_hitter)
        additional_hitter_data = {
            'fn' : at_bat_player_stats_hitter.player.first_name,
            'ln' : at_bat_player_stats_hitter.player.last_name,
            'srid_team' : at_bat_player_stats_hitter.player.team.srid,
            'oid_fp' : 2.7, # TODO - arbitrary for testing
        }

        at_bat_stats_str = PlayerStatsToStr(at_bat_player_stats_hitter).get_description()

        # get reduce/shrink manager instances
        pbp = {
            self.pitch_pbp : PitchPbpManager(pitch).get_data(additional_pitch_data),
            self.at_bat : AtBatManager(pitch).get_data(additional_hitter_data),
            self.zone_pitches : ZonePitchManager(zone_pitches, at_bat).get_data(),
            self.runners : RunnerManager(runners).get_data(additional_runner_data),
            self.at_bat_stats : at_bat_stats_str,
            self.stats : [ ps.to_json() for ps in player_stats ],
        }

        # return the linked data
        return pbp

    def __find_player_stats(self, player_stats_class, srid_game, srid_players=[]):
        return player_stats_class.objects.filter( srid_game=srid_game, srid_player__in=srid_players)

    def find_at_bat_hitter_player_stats(self, game, hitter):
        """ get the PlayerStatsHitter instance for the current at bat player """
        player_stats = self.__find_player_stats(self.player_stats_hitter_model, game, [hitter])

        count = player_stats.count()
        if count == 1:
            return player_stats[0]

        elif count < 1:
            return None

        # otherwise something bad is happening
        err_msg = '%s PlayerStatsHitter object(s) found for game[%s]-player[%s]' % (str(count),game, hitter)
        raise Exception(err_msg)

    def find_player_stats(self, game, pitcher, hitter, runners=[]):
        """ all arguments are srids, runners is a list of srids """
        player_stats = []

        # append the (single) instance for the hitter playerstats
        player_stats.append(self.find_at_bat_hitter_player_stats(game, hitter))

        # extend the list of playerstats for the remaining srids
        player_stats.extend(self.__find_player_stats(self.player_stats_pitcher_model, game, [pitcher]))
        player_stats.extend(self.__find_player_stats(self.player_stats_hitter_model, game, runners))
        player_srids = []
        player_stats_no_duplicates = []
        for ps in player_stats:
            if ps.srid_player not in player_srids:
                player_srids.append(ps.srid_player) # add to list of srids weve seen
                player_stats_no_duplicates.append(ps) # add to return list

        # return the list that ensures no duplicates
        return player_stats_no_duplicates

# class ZonePitchPbp(PitchPbp):
#     """
#     parse a single pitch from the target: ('mlb.pitcher','pbp').
#     ... yes thats right its in the pitcher collection unfortunately.
#
#     the purpose of this class is simply to allow us to call send()
#     without trying to link to a stats object or do any additional
#     mongo queries behind the scenes in the way that PitchPbp does.
#     """
#
#     # override default value from DataDenPbpDescription
#     pusher_sport_pbp_event  = 'zonepitch'
#
#     def __init__(self):
#         """ call parent constructor """
#         super().__init__()
#
#     def parse(self, obj, target=None):
#         """
#         the object must first be parsed before send() can be called
#
#         :param obj: a dataden.watcher.OpLogObj object
#         """
#         self.original_obj = obj
#         # we dont really need to set the SridFinder
#         # self.srid_finder = SridFinder(obj.get_o()) # get the data from the oplogobj
#         self.o = obj.get_o() # we didnt call super so we should do this
#
#         # so we can retrieve the list of zonepitches from the cache
#         zonepitch = self.o
#         try:
#             zpid = zonepitch.pop('_id') # remove it. its a lot of unnecessary characters
#         except KeyError:
#             # if the replayer is sending this object,
#             # the mongo object id with the key: '_id'
#             # will likely not exist, but thats fine.
#             pass
#         at_bat_id = zonepitch.get('at_bat__id')
#         cache_list = CacheList(cache=cache)
#         cache_list.add(at_bat_id, zonepitch)
#
#     def find_player_stats(self):
#         """ override - return an emtpy list, dont look for stats objects for zone pitches """
#         return []

# class RunnerPbp(PitchPbp):
#     """
#     parse a single runner event from the target: ('mlb.runner','pbp').
#
#     If it does not have a 'pitch__id', that indicates it was an event
#     independent of any pitches -- it was likely a steal.
#
#     NOTE: if it was a steal, it still have a 'steal__id' field,
#     but typical runner objects will not have this field!
#
#     NOTE 2: if it has a 'steal__id' field, but the starting and
#     ending base is the same, (the outcome will be 'CK') this
#     likely means the pitcher checked the runner with some kind
#     of pickoff attempt.
#
#     we are going to model Runner pbp objects after ZonePitchPbp
#     objects because we also want to add them to a cache to
#     be able to fetch a list of the recent ones per-at bat in real-time.
#     """
#
#     debug = True
#
#     # override default value from DataDenPbpDescription
#     pusher_sport_pbp_event  = 'runner'
#
#     # stolen base outcomes
#     stolen_base_outcomes = ['SB2','SB3','SB4']
#
#     def __init__(self):
#         """ call parent constructor """
#         super().__init__()
#
#     def parse(self, obj, target=None):
#         """
#         the object must first be parsed before send() can be called
#
#         :param obj: a dataden.watcher.OpLogObj object
#         """
#
#         if self.debug:
#             print('[%s] %s' % (self.__class__.__name__, str(obj)))
#
#         self.original_obj = obj
#         # we dont really need to set the SridFinder
#         # self.srid_finder = SridFinder(obj.get_o()) # get the data from the oplogobj
#         self.o = obj.get_o() # we didnt call super so we should do this
#
#         # so we can retrieve the list of zonepitches from the cache
#         runner = self.o
#         try:
#             runner_obj_id = runner.pop('_id') # remove it. its a lot of unnecessary characters
#         except KeyError:
#             # if the replayer is sending this object,
#             # the mongo object id with the key: '_id'
#             # will likely not exist, but thats fine.
#             pass
#
#         # get the pitch srid, but if it doesnt exist, do nothing (dont add to CacheList)
#         pitch_srid = runner.get('pitch__id', None)
#         if pitch_srid is None:
#             if self.debug:
#                 print('no "pitch__id" for runner obj/self.o: %s' % str(self.o))
#         else:
#             cache_list = CacheList(cache=cache)
#             cache_list.add(pitch_srid, runner)
#             if self.debug:
#                 print('     runnerPbp cache for pitch_srid[%s]' % pitch_srid, str(cache_list.get(pitch_srid)))
#
#     def send(self):
#         """
#         if the runner object is a stolen base, send it as its own pusher object,
#         but make sure to call super().send() to ensure the linked object goes out as necessary
#         """
#
#         # {'outcome_id': 'SB2', 'pitch__id': '669a6752-1149-4a72-8370-c055950d3646',
#         # 'parent_list__id': 'runners__list', 'description': 'Brett Lawrie steals second.',
#         # 'last_name': 'Lawrie', 'ending_base': 2.0, 'starting_base': 1.0,
#         # 'id': '6ac6fa53-ea9b-467d-87aa-6429a6bcb90c',
#         # 'game__id': '24791492-42dd-4162-a57f-cc0e4a62729c', 'jersey_number': 15.0,
#         # 'at_bat__id': '049d9d3b-033c-492f-826e-5a78ffaf87e4',
#         # 'preferred_name': 'Brett', 'out': 'false', 'first_name': 'Brett',
#         # 'parent_api__id': 'pbp', 'dd_updated__id': 1464041840497}
#         if self.o.get('outcome_id','') in self.stolen_base_outcomes:
#             # its a stolen base, which is kind of unique, so send it out.
#             # super().send() will take care of adding it to the sent cache!
#             push.classes.DataDenPush( push.classes.PUSHER_MLB_PBP, 'runner' ).send( self.o )
#
#         # send it normally...
#         super().send()
#
#     def find_player_stats(self):
#         """ override - return an emtpy list, dont look for stats objects for runner objects """
#         return []

class GamePbp(DataDenPbpDescription):

    game_model              = Game
    pbp_model               = Pbp
    portion_model           = GamePortion
    pbp_description_model   = PbpDescription

    def __init__(self):
        super().__init__()

    def parse(self, obj, target=None):
        super().parse( obj, target )

        # self.game & self.pbp are setup by super().parse()

        #print('srid game', self.o.get('id'))
        innings = self.o.get('innings', {})
        overall_idx = 0
        inning_half_idx = 0
        for inning_json in innings:
            inning = inning_json.get('inning', {})
            inning_sequence = inning.get('sequence', None)
            if inning_sequence == 0:
                print('skipping inning sequence 0 - its just lineup information')
                continue

            if inning_sequence is None:
                raise Exception('inning sequence is None! what the!?')

            inning_halfs = inning.get('inning_halfs', [])
            for half_json in inning_halfs:
                half = half_json.get('inning_half')
                half_type = half.get('type', None)
                if half_type is None:
                    raise Exception('half type is None! what the!?')

                #
                # get the game portion object
                game_portion = self.get_game_portion( 'inning_half', inning_half_idx )
                inning_half_idx += 1

                #
                # all pbp decriptions are associated with an
                # inning (integer) & inning_half (T or B).
                # get the hitter id too
                at_bats = half.get('at_bats', [])
                half_idx = 0
                for at_bat_json in at_bats:
                    at_bat = at_bat_json.get('at_bat')
                    srid_hitter = at_bat.get('hitter_id', '')
                    desc = at_bat.get('description', None)
                    if desc is None:
                        continue

                    half_idx += 1
                    overall_idx += 1

                    # print( str(overall_idx), str(half_idx),
                    #         'inning:%s' % str(inning_sequence),
                    #        'half:%s' % str(half_type),
                    #        'hitter:%s' % srid_hitter, desc )

                    pbp_desc = self.get_pbp_description(game_portion, overall_idx, desc)

class Injury(DataDenInjury):
    """
    MLB injuries dont have sports radar global ids (srids).
    We just use the status, 'DL15', 'DTD'.

    To conform to the way the other three major sports injuries work,
    we use the 'updated' and 'id' fields to generate an iid for mlb players!

    """
    player_model = Player
    injury_model = sports.mlb.models.Injury

    key_iid     = 'UNUSED' # the name of the field in the obj

    def __init__(self, wrapped=True):
        super().__init__(wrapped)

        self.srid_player_key = 'id'
        self.NON_INJURY_STATUSES = ['A']

    def get_custom_iid(self, status, updated, srid_player):
        """
        DO NOT CHANGE THIS FUNCTION or it will break the injury_cleaup method.

        :param srid_player:
        :param updated:
        :param status:
        :return:
        """
        return '%s-%s-%s' % (status, updated, srid_player)

    def parse(self, obj, target=None):
        super().parse(obj, target)

        if self.player is None: # ignore injury, because were going to get it manually below
            return

        # "full_name" : "Dioner Navarro",
        # "id" : "cbfa52c5-ef2e-4d7c-8e28-0ec6a63c6c6f",
        # "mlbam_id" : 425900,
        # "status" : "D15",
        # "updated" : "2015-04-23T15:59:54+00:00",

        #
        # extract the information from self.o
        status  = self.o.get('status', None)
        if status is None:
            raise Exception('mlb Injury.parse() error - "status" cant be None!')
        # IGNORE CERTAIN STATUSES WHICH ARENT INJURY RELATED
        if status in self.NON_INJURY_STATUSES:
            return
        updated = self.o.get('updated', None)
        if updated is None:
            raise Exception('mlb Injury.parse() error - "updated" cant be None because get_custom_iid() will break!')

        #
        # get the custom "iid" and look it up with that
        iid = self.get_custom_iid(status, updated, self.player.srid)
        try:
            self.injury = self.injury_model.objects.get(iid=iid)
        except self.injury_model.DoesNotExist:
            self.injury         = self.injury_model()
            self.injury.iid     = iid
            self.injury.player  = self.player

        self.injury.comment     = ''
        self.injury.status      = status
        self.injury.description = ''
        self.injury.save()

        #
        # connect the player object to the injury object
        self.player.injury = self.injury
        self.player.save()

class ProbablePitcherParser(AbstractDataDenParseable):

    probable_pitcher_type = 'pp'

    model = ProbablePitcher

    def __init__(self):
        super().__init__()

    def parse(self, obj, target=None):
        super().parse(obj, target)

        # {'parent_api__id': 'daily_summary',
        # 'away__id': '27a59d3b-ff7c-48ea-b016-4798f560f5e1',
        # 'league__id': '2fa448bc-fc17-4d3d-be03-e60e080fdc26',
        # 'preferred_name': 'Zach',
        # 'id': '169b7765-2519-4f2f-a67f-2e010c0d361e',
        # 'last_name': 'Neal', 'win': 0.0,
        # 'loss': 0.0,
        # 'jersey_number': 58.0, 'first_name':
        # 'Zachary', 'parent_list__id': 'games__list',
        # 'era': 9.0, 'game__id': '090a0fda-7842-4b31-b6cb-65f84971754a',
        # 'dd_updated__id': 1464125707339}=

        srid_game = self.o.get('game__id')
        srid_team = self.o.get('away__id',None)
        srid_player = self.o.get('id')

        if srid_team is None:
            srid_team = self.o.get('home__id',None)
        try:
            pp = self.model.objects.get(srid_game=srid_game, srid_team=srid_team)

        # except self.model.MultipleObjectsReturned:
        #     self.model.objects.filter(srid_game=srid_game, srid_team=srid_team).delete()
        #     return

        except self.model.DoesNotExist:

            pp = self.model()
            pp.srid_game        = srid_game
            pp.srid_team        = srid_team

        if pp.srid_player != srid_player:
            pp.srid_player = srid_player
            pp.save()

        # add the proabable pitcher using the GameUpdateManager
        # which will ensure the information gets pushed into
        # the draftgroup information
        gum = GameUpdateManager('mlb', srid_game)
        gum.add_probable_pitcher(srid_team, srid_player)

class DataDenMlb(AbstractDataDenParser):

    def __init__(self):
        self.game_model = sports.mlb.models.Game
        self.sport = 'mlb'

    def parse(self, obj):
        super().parse( obj ) # setup self.ns, self.parent_api

        #
        # game
        if self.target in [ ('mlb.season_schedule','schedule_pre'),
                            ('mlb.season_schedule','schedule_reg'),
                            ('mlb.season_schedule','schedule_pst') ]:
            #print( str(obj) )
            SeasonSchedule().parse( obj )
        elif self.target == ('mlb.game','schedule_reg'):
            #print( str(obj) )
            GameSchedule().parse( obj )
        elif self.target == ('mlb.game','schedule_pre'):
            #print( str(obj) )
            GameSchedule().parse( obj )
        elif self.target == ('mlb.game','schedule_pst'):
            #print( str(obj) )
            GameSchedule().parse( obj )

        # save the atbats (even in realtime) so we dont
        # have to query mongo for them (which is slower than a django query)
        elif self.target == (self.sport + '.at_bat','pbp'):
            # potentially build the main (linked) mlb pbp object
            pitch_pbp = PitchPbp()
            pitch_pbp.parse(obj, self.target)

        # the primary source of information about a particular thrown ball
        elif self.target == ('mlb.pitch','pbp'):
            # potentially build the main (linked) mlb pbp object
            pitch_pbp = PitchPbp()
            pitch_pbp.parse(obj, self.target)

            # pitch_pbp = PitchPbp()
            # pitch_pbp.parse( obj )
            # pitch_pbp.send()
            self.add_pbp( obj )

        # the pitch zone information
        elif self.target == ('mlb.pitcher','pbp'):
            # potentially build the main (linked) mlb pbp object
            pitch_pbp = PitchPbp()
            pitch_pbp.parse(obj, self.target)

            self.add_pbp( obj )

        #
        elif self.target == ('mlb.game','boxscores'):
            GameBoxscores().parse( obj )  # top level boxscore info
            push.classes.DataDenPush( push.classes.PUSHER_BOXSCORES, 'game' ).send( obj, async=settings.DATADEN_ASYNC_UPDATES )

        # runner objects (from pbp)
        elif self.target == ('mlb.runner','pbp'):
            # potentially build the main (linked) mlb pbp object
            pitch_pbp = PitchPbp()
            pitch_pbp.parse(obj, self.target)

            # cache it/save it/do django and/or postgres related things
            # TODO - we still might need to send base stealers
            # runner_pbp = RunnerPbp()
            # runner_pbp.parse( obj )
            # runner_pbp.send()

            # add it to a list of objects we've sent (helps us not double-send later on)
            self.add_pbp( obj )

        elif self.target == ('mlb.home','summary'): HomeAwaySummary().parse( obj )  # home team of boxscore
        elif self.target == ('mlb.away','summary'): HomeAwaySummary().parse( obj )  # away team of boxscore
        #
        # team
        elif self.target == ('mlb.team','hierarchy'): TeamHierarchy().parse( obj ) # parse each team
        #
        # player
        elif self.target == ('mlb.player','team_profile'): PlayerTeamProfile().parse( obj ) # ie: rosters
        elif self.target == ('mlb.player','summary'):
            PlayerStats().parse( obj ) # stats from games
        #
        # probable_pitcher
        elif self.target == ('mlb.probable_pitcher','daily_summary'):
            ppparser = ProbablePitcherParser()
            ppparser.parse(obj)
        #
        # default case, print this message for now

        #
        # mlb.content - the master object with list of ids to the content items
        elif self.target == ('mlb.content', 'content'):
            #
            # get an instance of TsxContentParser( sport ) to parse
            # the Sports Xchange content
            TsxContentParser(self.sport).parse( obj )

        else: self.unimplemented( self.target[0], self.target[1] )

    def cleanup_injuries(self):
        """


        :return:
        """
        #
        # get an instance of DataDen - ie: a connection to mongo db with all the stats
        dd = DataDen()

        #
        # injury process:
        # 1) get all the updates (ie: get the most recent dd_updated__id, and get all objects with that value)
        injury_objects = list( dd.find_recent('mlb','player','rostersfull') )
        #print(str(len(injury_objects)), 'recent injury updates (for mlb its from the rostersfull parent api')

        # 2) get all the existing players with injuries
        # players = list( Player.objects.filter( injury_type__isnull=False,
        #                                        injury_id__isnull=False ) )
        all_players = list( Player.objects.all() )

        # 3) for each updated injury, remove the player from the all-players list
        for inj in injury_objects:
            #
            # wrapped=False just means the obj isnt wrapped by the oplogwrapper
            i = Injury(wrapped=False)
            i.parse( inj )
            try:
                all_players.remove( i.get_player() )
            except ValueError:
                pass # thrown if player not in the list.

        # 5) with the leftover existing players,
        #    remove their injury since theres no current injury for them
        ctr_removed = 0
        for player in all_players:
            if player.remove_injury():
                ctr_removed += 1
        print(str(ctr_removed), 'leftover/stale injuries removed')

    @atomic
    def cleanup_rosters(self):
        """
        give the parent method the Team, Player classes,
        and rosters parent api so it can flag players
        who are no long on the teams roster on_active_roster = False
        """
        super().cleanup_rosters(self.sport,                         # datadeb sport db, ie: 'nba'
                                sports.mlb.models.Team,             # model class for the Team
                                sports.mlb.models.Player,           # model class for the Player
                                parent_api='team_profile')               # parent api where the roster players found
