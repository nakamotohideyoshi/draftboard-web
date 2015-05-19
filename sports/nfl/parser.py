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
        #
        # default case, print this message for now
        else: self.unimplemented( self.target[0], self.target[1] )
