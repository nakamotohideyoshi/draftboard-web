#
# sports/nfl/parser.py

from sports.nfl.models import Team, Game, Player, PlayerStats, GameBoxscore

from sports.sport.base_parser import AbstractDataDenParser, AbstractDataDenParseable, \
                        DataDenTeamHierachy, DataDenGameSchedule, DataDenPlayerRosters, \
                        DataDenPlayerStats, DataDenGameBoxscores, DataDenTeamBoxscores
import json

class TeamHierarchy(DataDenTeamHierachy):
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

    def __init__(self):
        super().__init__()

    def parse(self, obj):
        super().parse(obj)   # sets up the unsaved PlayerStats instance for us

        o = obj.get_o()


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
        #
        # nfl.team
        elif self.target == ('nfl.team','hierarchy'): TeamHierarchy().parse( obj )
        #
        # nfl.player
        elif self.target == ('nfl.player','rosters'): PlayerRosters().parse( obj )
        elif self.target == ('nfl.player','stats'): PlayerStats().parse( obj )
        #
        # default case, print this message for now
        else: self.unimplemented( self.target[0], self.target[1] )
