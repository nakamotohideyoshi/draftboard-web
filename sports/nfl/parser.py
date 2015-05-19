#
# sports/nfl/parser.py

import sports.nfl.models
from sports.sport.base_parser import AbstractDataDenParser, AbstractDataDenParseable, \
                                        DataDenTeamHierachy, DataDenGameSchedule

from dataden.util.timestamp import Parse as DataDenDatetime
import json

class TeamHierarchy(DataDenTeamHierachy):
    """
    TeamHierarchy simply needs to set the right Team model internally.
    """
    team_model = sports.nfl.models.Team

    def __init__(self):
        super().__init__()

class GameSchedule(DataDenGameSchedule):
    """
    GameSchedule simply needs to set the right Team & Game model internally
    """
    team_model = sports.nfl.models.Team
    game_model = sports.nfl.models.Game

    def __init__(self):
        super().__init__()

class DataDenNfl(AbstractDataDenParser):

    def __init__(self):
        self.game_model = sports.nfl.models.Game # unused

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
        # TODO ...
        #
        # default case, print this message for now
        else: self.unimplemented( self.target[0], self.target[1] )
