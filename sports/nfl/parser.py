#
# sports/nfl/parser.py

import sports.nfl.models
from sports.nfl.models import Team, Game, Player, PlayerStats, \
                                GameBoxscore, GamePortion, Pbp, PbpDescription

from sports.sport.base_parser import AbstractDataDenParser, \
                        DataDenTeamHierarchy, DataDenGameSchedule, DataDenPlayerRosters, \
                        DataDenPlayerStats, DataDenGameBoxscores, DataDenTeamBoxscores, \
                        DataDenPbpDescription, DataDenInjury
import json
from dataden.classes import DataDen

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

class GameSchedule(DataDenGameSchedule):
    """
    GameSchedule simply needs to set the right Team & Game model internally
    """
    team_model = Team
    game_model = Game

    def __init__(self):
        super().__init__()

    def parse(self, obj):
        # {
        #     "_id" : "cGFyZW50X2FwaV9faWRzY2hlZHVsZXNlYXNvbl9faWRodHRwOi8vYXBpLnNwb3J0c2RhdGFsbGMub3JnL25mbC10MS8yMDE0L1JFRy9zY2hlZHVsZS54bWxpZDNjNDJmNGVhLWU0YjMtNDQ5ZC04MmQ1LTM2ODUwMTQ0YWRkOQ==",
        #     "away" : "GB",
        #     "away_rotation" : "",
        #     "home" : "SEA",
        #     "home_rotation" : "",
        #     "id" : "3c42f4ea-e4b3-449d-82d5-36850144add9",
        #     "scheduled" : "2014-09-05T00:30:00+00:00",
        #     "status" : "closed",
        #     "parent_api__id" : "schedule",
        #     "dd_updated__id" : NumberLong("1432057846849"),
        #     "season__id" : "http://api.sportsdatallc.org/nfl-t1/2014/REG/schedule.xml",
        #     "venue" : "c6b9e5df-c9e4-434c-b3e6-83928f11cbda",
        #     "weather__list" : {
        #         "condition" : "Sunny",
        #         "humidity" : 50,
        #         "temperature" : 73,
        #         "wind__list" : {
        #             "direction" : "WNW",
        #             "speed" : 11
        #         }
        #     },
        #     "broadcast__list" : {
        #         "cable" : "",
        #         "internet" : "",
        #         "network" : "NBC",
        #         "satellite" : ""
        #     },
        #     "links__list" : [
        #         {
        #             "link" : {
        #                 "href" : "/2014/REG/1/GB/SEA/statistics.xml",
        #                 "rel" : "statistics",
        #                 "type" : "application/xml"
        #             }
        #         },
        #         {
        #             "link" : {
        #                 "href" : "/2014/REG/1/GB/SEA/summary.xml",
        #                 "rel" : "summary",
        #                 "type" : "application/xml"
        #             }
        #         },
        #         {
        #             "link" : {
        #                 "href" : "/2014/REG/1/GB/SEA/pbp.xml",
        #                 "rel" : "pbp",
        #                 "type" : "application/xml"
        #             }
        #         },
        #         {
        #             "link" : {
        #                 "href" : "/2014/REG/1/GB/SEA/boxscore.xml",
        #                 "rel" : "boxscore",
        #                 "type" : "application/xml"
        #             }
        #         },
        #         {
        #             "link" : {
        #                 "href" : "/2014/REG/1/GB/SEA/roster.xml",
        #                 "rel" : "roster",
        #                 "type" : "application/xml"
        #             }
        #         },
        #         {
        #             "link" : {
        #                 "href" : "/2014/REG/1/GB/SEA/injuries.xml",
        #                 "rel" : "injuries",
        #                 "type" : "application/xml"
        #             }
        #         },
        #         {
        #             "link" : {
        #                 "href" : "/2014/REG/1/GB/SEA/depthchart.xml",
        #                 "rel" : "depthchart",
        #                 "type" : "application/xml"
        #             }
        #         }
        #     ]
        # }
        super().parse(obj)
        o = obj.get_o()

        # super sets these fields (start is pulled from 'scheduled')
        #   ['srid','home','away','start','status','srid_home','srid_away','title']]
        weather_info            = o.get('weather__list', {})
        self.game.weather_json  = json.loads( json.dumps( weather_info ) )
        self.game.save()

class PlayerRosters(DataDenPlayerRosters):

    team_model      = Team
    player_model    = Player

    def __init__(self):
        super().__init__()

    def parse(self, obj, target=None):
        super().parse( obj )

        #
        # set the fields that arent set, and update the players name (super() grabs invalid fields)
        o = obj.get_o()
        self.player.first_name      = o.get('name_first',   None)
        self.player.last_name       = o.get('name_last',    None)
        self.player.position        = o.get('position',     None)
        self.player.primary_position = self.player.position # no "archtype" positions in nfl

        self.player.draft_pick      = o.get('draft_pick', '')
        self.player.draft_round     = o.get('draft_round', '')
        self.player.draft_year      = o.get('draft_year', '')
        self.player.srid_draft_team = o.get('draft_team', '')

        self.player.save()

class PlayerStats(DataDenPlayerStats):
    """
    nfl stats are somewhat daunting in the sheer amount of individual stats.
    coupled with that, the way they are broken down in mogno is not super intuitive.

    to sort everything out, the programmer should look at the distinct "parent_list__id"
    of the nfl.player collection. (in mongo shell:

        $> db.player.distinct('parent_list__id')
        [
            "players__list",
            "offense__list",
            "defense__list",
            "special_teams__list",
            "touchdowns__list",
            "rushing__list",
            "receiving__list",
            "punting__list",
            "punt_return__list",
            "penalty__list",
            "passing__list",
            "kickoffs__list",
            "kick_return__list",
            "fumbles__list",
            "first_downs__list",
            "field_goal__list",
            "extra_point__list",
            "two_point_conversion__list",
            "blocked_field_goal_return__list",
            "blocked_punt_return__list",
            "participants__list"
        ]
        $>

    now you can query for a category of stats for a player
    by also querying with its 'parent_list__id':

        $> db.player.findOne({'parent_api__id':'stats', 'parent_list__id':'rushing__list'})
            or
        $> db.player.findOne({'parent_api__id':'stats', 'parent_list__id':'touchdowns__list'})

    here is the "rushing__list" from the above query:

        {
            "_id" : "cGFyZW50X2FwaV9faWRzdGF0c2dhbWVfX2lkMjAwNDg5NzgtMGY0My00NzU1LWE2ZGUtZTJkNmIzYjNmY2QydGVhbV9faWRDQVJwYXJlbnRfbGlzdF9faWRydXNoaW5nX19saXN0aWRkYzJiM2UyNy0wYmMxLTRlYTctYjgwZS1mOWVmODFjYWIyYzk=",
            "att" : 1,
            "avg" : 5,
            "fd" : 1,
            "fd_pct" : 100,
            "fum" : 0,
            "id" : "dc2b3e27-0bc1-4ea7-b80e-f9ef81cab2c9",
            "jersey" : 82,
            "lg" : 5,
            "name" : "Jerricho Cotchery",
            "position" : "WR",
            "rz_att" : 0,
            "sfty" : 0,
            "td" : 0,
            "yds" : 5,
            "yds_10_pls" : 0,
            "yds_20_pls" : 0,
            "yds_30_pls" : 0,
            "yds_40_pls" : 0,
            "yds_50_pls" : 0,
            "parent_api__id" : "stats",
            "dd_updated__id" : NumberLong("1432057939467"),
            "game__id" : "20048978-0f43-4755-a6de-e2d6b3b3fcd2",
            "team__id" : "CAR",
            "parent_list__id" : "rushing__list"
        }

    note that a player can be, and probably will be if they accrued stats,
    in most of these categories for each game they've played! In this example,
    Jericho Cotchery was in 11 of the lists!

        $> db.player.find({'parent_api__id':'stats','id':'dc2b3e27-0bc1-4ea7-b80e-f9ef81cab2c9'}).count()
         11
        $>

    ***** The main point: Make sure to update stats in all categories for each player!!
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

        # nfl only has 'position' -- there is no concept of 'primary_position', so use 'position'
        self.ps.position            = self.p.position # copy the dst Player's position in here
        self.ps.primary_position    = self.p.position # copy the dst Player's position in here

        parent_list = o.get('parent_list__id', None)

        if parent_list == "touchdowns__list":
            pass # TODO
        elif parent_list == "rushing__list":
            self.ps.rush_td     = o.get('td',   0)
            self.ps.rush_yds    = o.get('yds',  0)
        elif parent_list == "receiving__list":
            self.ps.rec_td      = o.get('td',   0)
            self.ps.rec_yds     = o.get('yds',  0)
            self.ps.rec_rec     = o.get('rec',  0)
        elif parent_list == "punting__list":
            pass # TODO
        elif parent_list == "punt_return__list":
            pass # TODO
        elif parent_list == "penalty__list":
            pass # TODO
        elif parent_list == "passing__list":
            self.ps.pass_td     = o.get('td',   0)
            self.ps.pass_yds    = o.get('yds',  0)
            self.ps.pass_int    = o.get('int',  0)
        elif parent_list == "kickoffs__list":
            pass # TODO
        elif parent_list == "kick_return__list":
            pass # TODO
        elif parent_list == "fumbles__list":
            self.ps.off_fum_lost    = o.get('lost',         0)
            self.ps.off_fum_rec_td  = o.get('own_rec_td',   0)
        elif parent_list == "first_downs__list":
            pass # TODO
        elif parent_list == "field_goal__list":
            pass # TODO
        elif parent_list == "extra_point__list":
            pass # TODO
        elif parent_list == "two_point_conversion__list":
            self.ps.two_pt_conv     = o.get('pass',0) + o.get('rec',0) + o.get('rush',0)
        elif parent_list == "blocked_field_goal_return__list":
            pass # TODO
        elif parent_list == "blocked_punt_return__list":
            pass # TODO
        elif parent_list == 'field_goal_return__list':
            pass # TODO
        else:
            print( str(o) )
            print( 'obj parent_list__id was not found !')
            return

        self.ps.save()

class DstStats(DataDenPlayerStats):
    """
    Similar to PlayerStats, also inherits from DataDenPlayerStats!
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

        defense_list    = o.get('defense__list', {})

        self.ps.position            = self.p.position # copy the dst Player's position in here
        self.ps.primary_position    = self.p.position # copy the dst Player's position in here

        self.ps.sack    = defense_list.get('sack',      0)
        self.ps.ints    = defense_list.get('int',       0)
        self.ps.fum_rec = defense_list.get('fum_rec',   0)

        self.ps.sfty    = defense_list.get('sfty',      0)
        self.ps.blk_kick = defense_list.get('bk',       0)

        # defensive touchdowns can happen in a handful of ways:
        touchdowns_list             = o.get('touchdowns__list', {})
        blocked_punt_return_list    = o.get('blocked_punt_return__list', {})
        field_goal_return_list      = o.get('field_goal_return__list',  {})
        blocked_fg_return_list      = o.get('blocked_field_goal_return__list', {})
        passing_list                = o.get('passing__list', {})
        fumble_list                 = o.get('fumble__list', {})
        rushing_list                = o.get('rushing__list', {})
        punting_list                = o.get('punting__list', {})

        self.ps.ret_kick_td     = touchdowns_list.get('kick_ret', 0)
        self.ps.ret_punt_td     = touchdowns_list.get('punt_ret', 0) # will NOT include BLOCKED punt return tds!
        self.ps.ret_int_td      = touchdowns_list.get('int',      0)
        self.ps.ret_fum_td      = touchdowns_list.get('fum_ret',  0)
        self.ps.ret_blk_punt    = blocked_punt_return_list.get('td', 0)
        self.ps.ret_fg_td       = field_goal_return_list.get('td', 0)
        self.ps.ret_blk_fg_td   = blocked_fg_return_list.get('td', 0)

        self.ps.int_td_against  = passing_list.get('int_td', 0)
        self.ps.fum_td_against  = fumble_list.get('opp_rec_td', 0)

        #
        # get the safeties the offense has committed, because it wont count against DST points allowed!
        self.off_pass_sfty      = passing_list.get('sfty', 0)     # this team's OFFENSE got safetied
        self.off_rush_sfty      = rushing_list.get('sfty', 0)
        self.off_punt_sfty      = punting_list.get('sfty', 0)

        self.ps.save()

class GameBoxscores(DataDenGameBoxscores):

    gameboxscore_model  = GameBoxscore
    team_model          = Team

    def __init__(self):
        super().__init__()

        self.HOME       = 'home' # override parent field name for HOME
        self.AWAY       = 'away' # override parent field name for AWAY

    def parse(self, obj):
        """
        :param obj:
        :return:
        """

        # "_id" : "cGFyZW50X2FwaV9faWRib3hzY29yZXNpZDIwMDQ4OTc4LTBmNDMtNDc1NS1hNmRlLWUyZDZiM2IzZmNkMg==",
        # "away" : "ARI",
        #X "clock" : ":00",
        # "completed" : "2015-01-04T00:54:36+00:00",
        # "home" : "CAR",
        # "id" : "20048978-0f43-4755-a6de-e2d6b3b3fcd2",
        # "quarter" : 4,
        # "scheduled" : "2015-01-03T21:20:00+00:00",
        #X "status" : "closed",
        # "xmlns" : "http://feed.elasticstats.com/schema/nfl/boxscore-v1.0.xsd",
        # "parent_api__id" : "boxscores",
        # "dd_updated__id" : NumberLong("1432078858338"),
        # "teams" : [
        #     {
        #         "team" : "CAR"
        #     },
        #     {
        #         "team" : "ARI"
        #     }
        # ],
        super().parse( obj )

        o = obj.get_o()
        self.boxscore.clock     = o.get('clock',    '')
        self.boxscore.quarter   = o.get('quarter',  '')
        self.completed          = o.get('completed', '')

        self.boxscore.save()

class TeamBoxscores(DataDenTeamBoxscores):

    gameboxscore_model  = GameBoxscore

    def __init__(self):
        super().__init__()

    def parse(self, obj):
        """
        :param obj:
        :return:
        """
        # "_id" : "cGFyZW50X2FwaV9faWRib3hzY29yZXNnYW1lX19pZDIwMDQ4OTc4LTBmNDMtNDc1NS1hNmRlLWUyZDZiM2IzZmNkMmlkQ0FS",
        # "id" : "CAR",
        # "market" : "Carolina",
        # "name" : "Panthers",
        # "remaining_challenges" : 2,
        # "remaining_timeouts" : 2,
        # "parent_api__id" : "boxscores",
        # "dd_updated__id" : NumberLong("1432078858338"),
        # "game__id" : "20048978-0f43-4755-a6de-e2d6b3b3fcd2",
        # "scoring__list" : {
        #     "points" : 27,
        #     "quarters" : [
        #         {
        #             "quarter" : {
        #                 "number" : 1,
        #                 "points" : 10
        #             }
        #         },
        #         {
        #             "quarter" : {
        #                 "number" : 2,
        #                 "points" : 3
        #             }
        #         },
        #         {
        #             "quarter" : {
        #                 "number" : 3,
        #                 "points" : 14
        #             }
        #         },
        #         {
        #             "quarter" : {
        #                 "number" : 4,
        #                 "points" : 0
        #             }
        #         }
        #     ]
        # }

        super().parse( obj )

        o = obj.get_o()

        srid_team           = o.get('id', None)
        scoring_list        = o.get('scoring__list', {})
        points              = scoring_list.get('points', 0)
        scoring_list_json   = json.loads( json.dumps( scoring_list ) )

        if srid_team == self.boxscore.srid_home:
            self.boxscore.home_score = points
            self.boxscore.home_scoring_json = scoring_list_json
        elif srid_team == self.boxscore.srid_away:
            self.boxscore.away_score = points
            self.boxscore.away_scoring_json = scoring_list_json
        else:
            print( str(o) )
            print( 'TeamBoxscores srid_team[%s] did not match either home or away team!' % srid_team)
            return

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

        # self.game & self.pbp are setup by super().parse()
        #
        # "quarters" : [
		# {
		# 	"quarter" : {
		# 		"number" : 1,
		# 		"event__list" : {
		# 			"clock" : "15:00",
		# 			"sequence" : 1,
		# 			"type" : "cointoss",
		# 			"updated" : "2015-01-03T21:36:00+00:00",
		# 			"winner" : "ARI",
		# 			"summary" : "ARI wins coin toss, elects to receive."
		# 		},
		# 		"drives" : [
		# 			{
		# 				"drive" : {
		# 					"clock" : "15:00",
		# 					"team" : "ARI",
		# 					"plays" : [
		# 						{
		# 							"play" : "5974dc8d-692e-4f26-b6ff-8341d8a02a31"
		# 						},
		# 						{ play }, ..., { play },

        print('srid game', self.o.get('id'))
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

    def __init__(self):
        super().__init__()

    def parse(self, obj, target=None):
        #
        # dont need to call super for EventPbp - just get the event by srid.
        # if it doesnt exist dont do anything, else set the description
        #super().parse( obj, target )
        self.o = obj.get_o() # we didnt call super so we should do thisv
        srid_pbp_desc = self.o.get('id', None)
        pbp_desc = self.get_pbp_description_by_srid( srid_pbp_desc )
        if pbp_desc:
            description = self.o.get('summary', None)
            if pbp_desc.description != description:
                # only save it if its changed
                pbp_desc.description = description
                pbp_desc.save()
        else:
            print( 'pbp_desc not found by srid %s' % srid_pbp_desc)

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
        self.injury.srid        = self.o.get('id',          '') # not set by parent
        self.injury.practice_status     = self.o.get('practice_status', '')
        self.injury.status      = self.o.get('game_status', '')
        self.injury.description = self.o.get('description', '')
        self.injury.save()

        #
        # connect the player object to the injury object
        self.player.injury = self.injury
        self.player.save()

class DataDenNfl(AbstractDataDenParser):

    def __init__(self):
        self.game_model = Game # unused

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
        # nfl.game
        if self.target == ('nfl.game','schedule'): GameSchedule().parse( obj )
        elif self.target == ('nfl.game','boxscores'): GameBoxscores().parse( obj )
        elif self.target == ('nfl.game','pbp'): GamePbp().parse( obj )
        #
        # nfl.play (events are parsed in the nfl.game | pbp feed, but the PLAYS are parsed here:
        elif self.target == ('nfl.play','pbp'): PlayPbp().parse( obj )
        #
        # nfl.team
        elif self.target == ('nfl.team','hierarchy'): TeamHierarchy().parse( obj )
        elif self.target == ('nfl.team','stats'): DstStats().parse( obj )
        elif self.target == ('nfl.team','boxscores'): TeamBoxscores().parse( obj )
        #
        # nfl.player
        elif self.target == ('nfl.player','rosters'): PlayerRosters().parse( obj )
        elif self.target == ('nfl.player','stats'): PlayerStats().parse( obj )
        # #
        # # nfl.injury
        # elif self.target == ('nfl.injury','gameroster'): Injury().parse( obj )
        #
        # default case, print this message for now
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
        injury_objects = list( dd.find_recent('nfl','injury','gameroster') )
        print(str(len(injury_objects)), 'recent injury updates')

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