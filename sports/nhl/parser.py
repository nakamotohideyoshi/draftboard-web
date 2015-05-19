#
# sports/nhl/parser.py

from sports.nhl.models import Team, Game, Player, PlayerStats, GameBoxscore

from sports.sport.base_parser import AbstractDataDenParser, AbstractDataDenParseable, \
                        DataDenTeamHierachy, DataDenGameSchedule, DataDenPlayerRosters, \
                        DataDenPlayerStats, DataDenGameBoxscores, DataDenTeamBoxscores

from dataden.util.timestamp import Parse as DataDenDatetime
import json

class TeamHierarchy(DataDenTeamHierachy):
    """
    TeamHierarchy simply needs to set the right Team model internally.
    """
    team_model = Team

    def __init__(self):
        super().__init__()

class GameSchedule(DataDenGameSchedule):
    """
    GameSchedule simply needs to set the right Team & Game model internally
    """
    team_model = Team
    game_model = Game

    def __init__(self):
        super().__init__()

class PlayerRosters(DataDenPlayerRosters):

    team_model      = Team
    player_model    = Player

    def __init__(self):
        super().__init__()

class PlayerStats(DataDenPlayerStats):

    game_model          = Game
    player_model        = Player
    player_stats_model  = PlayerStats

    def __init__(self):
        super().__init__()

    def parse(self, obj):

        super().parse(obj)  # setup PlayerStats instance

        if self.ps is None:
            # the PlayerStats object couldnt be created due to a previous issue,
            #  typically, either the game or player couldnt be found by its 'srid'
            return

        # self.ps is the instance of PlayerStats we need to populate with these stats.
        # skaters do not get Goalie stats. Goalies DO GET skater stats!
        o = obj.get_o()
        statistics_list     = o.get('statistics__list', {})
        skater_sh_list      = statistics_list.get('shorthanded__list', {})
        skater_pp_list      = statistics_list.get('powerplay__list', {})
        skater_so_list      = statistics_list.get('shootout__list', {})
        goaltending_list    = o.get('goaltending__list', {})

        # skater stats
        self.ps.goal        = statistics_list.get('goals', 0)
        self.ps.assist      = statistics_list.get('assists', 0)
        self.ps.sog         = statistics_list.get('shots', 0)
        self.ps.blk         = statistics_list.get('blocked_shots', 0)
        self.ps.sh_goal     = skater_sh_list.get('goals', 0)
        self.ps.pp_goal     = skater_pp_list.get('goals', 0)
        self.ps.so_goal     = skater_so_list.get('goals', 0)

        # goalie stats    ... [ "win", "loss", "overtime_loss", "none" ] are the "credit" types for goalies
        self.ps.w           = goaltending_list.get('credit', '').lower() == 'win'
        self.ps.l           = goaltending_list.get('credit', '').lower() == 'loss'
        self.ps.otl         = goaltending_list.get('credit', '').lower() == 'overtime_loss'
        self.ps.saves       = goaltending_list.get('saves', 0)
        self.ps.ga          = goaltending_list.get('goals_against', 0)
        self.ps.shutout     = goaltending_list.get('shutout', '').lower() == "true"

        self.ps.save() # commit changes

class GameBoxscores(DataDenGameBoxscores):

    gameboxscore_model  = GameBoxscore
    team_model          = Team

    def __init__(self):
        super().__init__()

    def parse(self, obj):
        super().parse(obj) # much of the generic parsing is done here, it sets self.boxscore

        if self.boxscore is None:
            return

        o = obj.get_o()
        self.boxscore.period = o.get('period', 1)
        self.boxscore.save()

class TeamBoxscores(DataDenTeamBoxscores):

    team_model          = Team
    gameboxscore_model  = GameBoxscore

    def __init__(self):
        super().__init__()

    def parse(self, obj):
        super().parse(obj) # make sure the team exists and gets the sets self.boxscore

        # self.boxscore may be None here, if you write anymore code make sure to check

class DataDenNhl(AbstractDataDenParser):

    def __init__(self):
        self.game_model = Game # current unused

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
        elif self.target == ('nhl.game','boxscores'): GameBoxscores().parse( obj )
        #
        # nhl.team
        elif self.target == ('nhl.team','hierarchy'): TeamHierarchy().parse( obj )
        elif self.target == ('nhl.team','boxscores'): TeamBoxscores().parse( obj )
        #
        # nhl.player
        elif self.target == ('nhl.player','rosters'): PlayerRosters().parse( obj )
        elif self.target == ('nhl.player','stats'): PlayerStats().parse( obj )
        #
        # default case, print this message for now
        else: self.unimplemented( self.target[0], self.target[1] )