#
# sports/nhl/parser.py

import sports.nhl.models
from sports.sport.base_parser import AbstractDataDenParser, AbstractDataDenParseable, \
                                        DataDenTeamHierachy, DataDenGameSchedule

from dataden.util.timestamp import Parse as DataDenDatetime
import json

class TeamHierarchy(DataDenTeamHierachy):
    """
    TeamHierarchy simply needs to set the right Team model internally.
    """
    team_model = sports.nhl.models.Team

    def __init__(self):
        super().__init__()

class GameSchedule(DataDenGameSchedule):
    """
    GameSchedule simply needs to set the right Team & Game model internally
    """
    team_model = sports.nhl.models.Team
    game_model = sports.nhl.models.Game

    def __init__(self):
        super().__init__()

class DataDenNhl(AbstractDataDenParser):

    def __init__(self):
        self.game_model = sports.nhl.models.Game # unused

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
        # nhl.game
        if self.target == ('nhl.game','schedule'): GameSchedule().parse( obj )
        #elif self.target == ('nhl.game','boxscores'): GameBoxscores().parse( obj )
        #
        # nhl.team
        elif self.target == ('nhl.team','hierarchy'): TeamHierarchy().parse( obj )
        #elif self.target == ('nhl.team','boxscores'): TeamBoxscores().parse( obj )
        #
        # nhl.player
        #elif self.target == ('nhl.player','rosters'): PlayerRosters().parse( obj )
        #elif self.target == ('nhl.player','stats'): PlayerStats().parse( obj )
        #elif self.target == ('nhl.player','pbp'): PlayerPbp().parse( obj )
        #
        # nhl.event
        #elif self.target == ('nhl.event','pbp'): EventPbp().parse( obj )
        #
        # default case, print this message for now
        else: self.unimplemented( self.target[0], self.target[1] )