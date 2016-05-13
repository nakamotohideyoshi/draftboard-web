#
# sports/mlb/parser.py

from django.db.transaction import atomic
from django.core.cache import cache
from sports.classes import SiteSportManager
from sports.trigger import CacheList
import sports.mlb.models
from sports.mlb.models import (
    Team,
    Game,
    Player,
    PlayerStats,
    GameBoxscore,
    Pbp,
    PbpDescription,
    GamePortion,
    Season,
)
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
from django.contrib.contenttypes.models import ContentType
from dataden.classes import DataDen
import push.classes
from django.conf import settings
from sports.sport.base_parser import TsxContentParser

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
        self.cache_list.add(o.get('id'), o)

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
            #print('')
            #print( statistics )
            pitching = statistics.get('pitching__list', {})
            #print('')
            #print( pitching )
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
            #print('')
            #print( statistics )
            hitting = statistics.get('hitting__list', {}) # default will useful if it doenst exist
            #print('')
            #print( hitting )
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

class PitchPbp(DataDenPbpDescription):
    """
    given an object whose namespace, parent api is a target like:
     ('mlb.pitch','pbp') this object is capable of emitting
     the play by play information with send()
    """

    class AtBatNotFoundException(Exception): pass

    class MultipleAtBatObjectsFoundException(Exception): pass

    game_model              = Game
    pbp_model               = Pbp
    portion_model           = GamePortion
    pbp_description_model   = PbpDescription
    #
    player_stats_model      = sports.mlb.models.PlayerStatsPitcher
    pusher_sport_pbp        = push.classes.PUSHER_MLB_PBP
    pusher_sport_stats      = push.classes.PUSHER_MLB_STATS

    at_bat_srid_field       = 'at_bat__id'

    at_bat          = 'at_bat'
    at_bat_stats    = 'at_bat_stats'
    zone_pitches    = 'zone_pitches'
    runners         = 'runners'

    def __init__(self):
        super().__init__()
        self.player_stats_pitcher_model  = sports.mlb.models.PlayerStatsPitcher      # mlb pitcher stats
        self.player_stats_hitter_model   = sports.mlb.models.PlayerStatsHitter       # mlb hitter stats

        self.at_bat_object = None

    def parse(self, obj, target=None):
        """
        the object must first be parsed before send() can be called

        :param obj: a dataden.watcher.OpLogObj object
        """
        self.original_obj = obj
        self.srid_finder = SridFinder(obj.get_o()) # get the data from the oplogobj
        self.o = obj.get_o() # we didnt call super so we should do this

    def build_linked_pbp_stats_data(self, player_stats):
        """
        override parent method to also add the zone pitch list.

        be sure to call super method, and add the zonepitches to the object returned
        """

        # get the pitch pbp's srid. it uniquely identifies each discrete mlb pitch
        pitch_srid = self.o.get('id')

        data = super().build_linked_pbp_stats_data(player_stats)

        # add the zonepitch list
        zone_pitch_cache = CacheList(cache=cache)
        at_bat_srid = self.o.get(self.at_bat_srid_field)

        #
        # add the zone pitches to the data to be sent to clients
        data[self.zone_pitches] = zone_pitch_cache.get(key=at_bat_srid)
        data[self.at_bat]       = self.get_at_bat(at_bat_srid)

        # get the runners list from cache (sort of like how we get zone pitches.
        runners_cache           = CacheList(cache=cache)
        # use the pitch_srid as the key for runners list,
        # because runner objects will always be associated with an individual pitch,
        # from what i've seen anyways...
        data[self.runners]      = runners_cache.get(key=pitch_srid)

        # add the playerStats object for the hitter in the current at_bat
        player_stats_cache_list = PlayerStats.get_cache_list()[0]
        player_stats_obj_list = player_stats_cache_list.get()
        # TODO
        if len(player_stats_obj_list) > 0:
            data[self.at_bat_stats] = player_stats_obj_list[0]


        # return the linked data
        return data

    def get_at_bat(self, at_bat_srid):
        if self.at_bat_object is not None:
            return self.at_bat_object

        dd = DataDen()
        results = dd.find('mlb','at_bat','pbp', target={'id':at_bat_srid})

        if results.count() == 0:
            err_msg = 'no at_bat object found for srid %s' % (at_bat_srid)
            raise self.AtBatNotFoundException(err_msg)
        if results.count() != 1:
            err_msg = 'expected 1 at_bat object for srid %s, but found %s' % (at_bat_srid, len(results))
            raise self.MultipleAtBatObjectsFoundException(err_msg)
        #
        # return the at_bat object
        self.at_bat_object = results[0]
        return self.at_bat_object

    def get_runners(self, at_bat_srid):
        pass # TODO

    def __find_player_stats(self, player_stats_class, srid_game, srid_players=[]):
        return player_stats_class.objects.filter( srid_game=srid_game, srid_player__in=srid_players)

    def find_player_stats(self):
        """
        override parent method  -- return a list of the PlayerStats objects
        for players related to the pitch object.
        """
        player_stats    = []
        srid_game       = self.get_srid_game('game__id')
        srid_pitcher    = self.get_srids_for_field('pitcher')
        pitcher_stats   = self.__find_player_stats( self.player_stats_pitcher_model, srid_game, srid_pitcher )
        player_stats.extend(list(pitcher_stats))

        #
        # get the runners, but it does not yet include the hitter in the at bat!
        srid_runners    = self.get_srids_for_field('runner')
        runner_stats    = self.__find_player_stats( self.player_stats_hitter_model, srid_game, srid_runners )
        player_stats.extend(list(runner_stats))

        #
        # attempt to get the at_bat object which ontains the hitter (as well as the description)
        # if the play is over. we will probably want to get the glossary definition of the result.
        try:
            at_bat = self.get_at_bat(self.o.get(self.at_bat_srid_field))
        except self.AtBatNotFoundException:
            at_bat = None

        if at_bat is not None:
            finder = SridFinder(at_bat)
            srid_hitters    = finder.get_for_field('hitter_id')
            hitter_stats    = self.__find_player_stats( self.player_stats_hitter_model, srid_game, srid_hitters )
            player_stats.extend(list(hitter_stats))

        #
        # return PlayerStat objects for the pitcher, runners, and hitter
        return player_stats

class ZonePitchPbp(PitchPbp):
    """
    parse a single pitch from the target: ('mlb.pitcher','pbp').
    ... yes thats right its in the pitcher collection unfortunately.

    the purpose of this class is simply to allow us to call send()
    without trying to link to a stats object or do any additional
    mongo queries behind the scenes in the way that PitchPbp does.
    """

    # override default value from DataDenPbpDescription
    pusher_sport_pbp_event  = 'zonepitch'

    def __init__(self):
        """ call parent constructor """
        super().__init__()

    def parse(self, obj, target=None):
        """
        the object must first be parsed before send() can be called

        :param obj: a dataden.watcher.OpLogObj object
        """
        self.original_obj = obj
        # we dont really need to set the SridFinder
        # self.srid_finder = SridFinder(obj.get_o()) # get the data from the oplogobj
        self.o = obj.get_o() # we didnt call super so we should do this

        # so we can retrieve the list of zonepitches from the cache
        zonepitch = self.o
        try:
            zpid = zonepitch.pop('_id') # remove it. its a lot of unnecessary characters
        except KeyError:
            # if the replayer is sending this object,
            # the mongo object id with the key: '_id'
            # will likely not exist, but thats fine.
            pass
        at_bat_id = zonepitch.get('at_bat__id')
        #print('adding to cache_list, at_bat_id:', str(at_bat_id))
        #cache_list = CacheList(self.c)
        cache_list = CacheList(cache=cache)
        cache_list.add(at_bat_id, zonepitch)

    def find_player_stats(self):
        """ override - return an emtpy list, dont look for stats objects for zone pitches """
        return []

class RunnerPbp(PitchPbp):
    """
    parse a single pitch from the target: ('mlb.runner','pbp').

    If it does not have a 'pitch__id', that indicates it was an event
    independent of any pitches -- it was likely a steal.

    NOTE: if it was a steal, it still have a 'steal__id' field,
    but typical runner objects will not have this field!

    NOTE 2: if it has a 'steal__id' field, but the starting and
    ending base is the same, (the outcome will be 'CK') this
    likely means the pitcher checked the runner with some kind
    of pickoff attempt.

    we are going to model Runner pbp objects after ZonePitchPbp
    objects because we also want to add them to a cache to
    be able to fetch a list of the recent ones per-at bat in real-time.
    """

    # override default value from DataDenPbpDescription
    pusher_sport_pbp_event  = 'runner'

    def __init__(self):
        """ call parent constructor """
        super().__init__()

    def parse(self, obj, target=None):
        """
        the object must first be parsed before send() can be called

        :param obj: a dataden.watcher.OpLogObj object
        """
        self.original_obj = obj
        # we dont really need to set the SridFinder
        # self.srid_finder = SridFinder(obj.get_o()) # get the data from the oplogobj
        self.o = obj.get_o() # we didnt call super so we should do this

        # so we can retrieve the list of zonepitches from the cache
        runner = self.o
        try:
            runner_obj_id = runner.pop('_id') # remove it. its a lot of unnecessary characters
        except KeyError:
            # if the replayer is sending this object,
            # the mongo object id with the key: '_id'
            # will likely not exist, but thats fine.
            pass

        # get the pitch srid, but if it doesnt exist, do nothing (dont add to CacheList)
        pitch_srid = runner.get('pitch__id', None)
        if pitch_srid is not None:
            print('adding runner obj to cache_list, pitch_srid:', str(pitch_srid))
            #cache_list = CacheList(self.c)
            cache_list = CacheList(cache=cache)
            cache_list.add(pitch_srid, runner)
        else:
            print('runner obj had no pitch__id so not adding to runner list for linked obj')

    def find_player_stats(self):
        """ override - return an emtpy list, dont look for stats objects for runner objects """
        return []

class GamePbp(DataDenPbpDescription):

    game_model              = Game
    pbp_model               = Pbp
    portion_model           = GamePortion
    pbp_description_model   = PbpDescription

    def __init__(self):
        super().__init__()

    def parse(self, obj, target=None):
        #pass
        # super().parse( obj, target )
        #
        # # self.game & self.pbp are setup by super().parse()
        #
        # print('srid game', self.o.get('id'))
        # innings = self.o.get('innings', {})
        # overall_idx = 0
        # for inning_json in innings:
        #     inning = inning_json.get('inning', {})
        #     inning_sequence = inning.get('sequence', None)
        #     if inning_sequence == 0:
        #         print('skipping inning sequence 0 - its just lineup information')
        #         continue
        #
        #     if inning_sequence is None:
        #         raise Exception('inning sequence is None! what the!?')
        #     #print( inning )
        #     #print( '' )
        #     #
        #     # each 'inning' is
        #     # inning.keys()  --> dict_keys(['scoring__list', 'sequence', 'inning_halfs', 'number'])
        #     # inning.get('inning_halfs', []) # gets() a list of dicts
        #     inning_halfs = inning.get('inning_halfs', [])
        #     for half_json in inning_halfs:
        #         half = half_json.get('inning_half')
        #         half_type = half.get('type', None)
        #         if half_type is None:
        #             raise Exception('half type is None! what the!?')
        #         #print(str(half))
        #         #print("")
        #
        #         #
        #         # all pbp decriptions are associated with an
        #         # inning (integer) & inning_half (T or B).
        #         # get the hitter id too
        #         at_bats = half.get('at_bats', [])
        #         half_idx = 0
        #         for at_bat_json in at_bats:
        #             at_bat = at_bat_json.get('at_bat')
        #             srid_hitter = at_bat.get('hitter_id', '')
        #             desc = at_bat.get('description', None)
        #             if desc is None:
        #                 continue
        #
        #             half_idx += 1
        #             overall_idx += 1
        #
        #             print( str(overall_idx), str(half_idx),
        #                     'inning:%s' % str(inning_sequence),
        #                    'half:%s' % str(half_type),
        #                    'hitter:%s' % srid_hitter,
        #                                         desc )
        #             #
        #             # we should cache this so we dont
        #             # repetetively save the same object!
        #             try:
        #                 pbp_ctype = ContentType.objects.get_for_model(self.pbp)
        #                 self.description = self.pbp_description_model.objects.get(pbp_type__pk=pbp_ctype.id,
        #                                                                 pbp_id=self.pbp.id,
        #                                                                 idx=overall_idx )
        #                 #self.description = self.pbp_description_model.objects.get(pbp=self.pbp, idx=overall_idx)
        #             except self.pbp_description_model.DoesNotExist:
        #                 self.description = self.pbp_description_model()
        #                 self.description.pbp = self.pbp
        #                 self.description.idx = overall_idx
        #             self.description.description = desc
        #             self.description.save()

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
            #print( inning )
            #print( '' )
            #
            # each 'inning' is
            # inning.keys()  --> dict_keys(['scoring__list', 'sequence', 'inning_halfs', 'number'])
            # inning.get('inning_halfs', []) # gets() a list of dicts
            inning_halfs = inning.get('inning_halfs', [])
            for half_json in inning_halfs:
                half = half_json.get('inning_half')
                half_type = half.get('type', None)
                if half_type is None:
                    raise Exception('half type is None! what the!?')
                #print(str(half))
                #print("")

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

                    print( str(overall_idx), str(half_idx),
                            'inning:%s' % str(inning_sequence),
                           'half:%s' % str(half_type),
                           'hitter:%s' % srid_hitter, desc )

                    pbp_desc = self.get_pbp_description(game_portion, overall_idx, desc)
                    # #
                    # # we should cache this so we dont
                    # # repetetively save the same object!
                    # try:
                    #     pbp_ctype = ContentType.objects.get_for_model(self.pbp)
                    #     self.description = self.pbp_description_model.objects.get(pbp_type__pk=pbp_ctype.id,
                    #                                                     pbp_id=self.pbp.id,
                    #                                                     idx=overall_idx )
                    #     #self.description = self.pbp_description_model.objects.get(pbp=self.pbp, idx=overall_idx)
                    # except self.pbp_description_model.DoesNotExist:
                    #     self.description = self.pbp_description_model()
                    #     self.description.pbp = self.pbp
                    #     self.description.idx = overall_idx
                    # self.description.description = desc
                    # self.description.save()

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
        #
        # specal case: 'pbp' where we also send the object to Pusher !
        # elif self.target == ('mlb.game','pbp'):
        #     #GamePbp().parse( obj )
        #     #push.classes.PbpDataDenPush( push.classes.PUSHER_MLB_PBP, 'game' ).send( obj, async=settings.DATADEN_ASYNC_UPDATES )
        #     pass # we dont need this
        elif self.target == ('mlb.pitch','pbp'):
            #print( obj )
            pitch_pbp = PitchPbp()
            pitch_pbp.parse( obj )
            pitch_pbp.send()
            self.add_pbp( obj )

        # the pitch zone information
        elif self.target == ('mlb.pitcher','pbp'):
            #print( obj )
            zone_pitch_pbp = ZonePitchPbp()
            zone_pitch_pbp.parse( obj )
            zone_pitch_pbp.send()
            self.add_pbp( obj )

        #
        elif self.target == ('mlb.game','boxscores'):
            GameBoxscores().parse( obj )  # top level boxscore info
            push.classes.DataDenPush( push.classes.PUSHER_BOXSCORES, 'game' ).send( obj, async=settings.DATADEN_ASYNC_UPDATES )

        # runner objects (from pbp)
        elif self.target == ('mlb.runner','pbp'):
            runner_pbp = RunnerPbp()
            runner_pbp.parse( obj )     # cache it/save it/do django and/or postgres related things
            runner_pbp.send()           # pusher it.
            self.add_pbp( obj )         # add it to a list of objects we've sent (helps us not double-send later on)

        elif self.target == ('mlb.home','summary'): HomeAwaySummary().parse( obj )  # home team of boxscore
        elif self.target == ('mlb.away','summary'): HomeAwaySummary().parse( obj )  # away team of boxscore
        #
        # team
        elif self.target == ('mlb.team','hierarchy'): TeamHierarchy().parse( obj ) # parse each team
        #
        # player
        elif self.target == ('mlb.player','team_profile'): PlayerTeamProfile().parse( obj ) # ie: rosters
        elif self.target == ('mlb.player','summary'): PlayerStats().parse( obj ) # stats from games
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
