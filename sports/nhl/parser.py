#
# sports/nhl/parser.py
from scoring.classes import NhlSalaryScoreSystem
from sports.nhl.models import Team, Game, Player, PlayerStats, \
                                GameBoxscore, Pbp, PbpDescription, GamePortion

from sports.sport.base_parser import AbstractDataDenParser, \
                        DataDenTeamHierarchy, DataDenGameSchedule, DataDenPlayerRosters, \
                        DataDenPlayerStats, DataDenGameBoxscores, DataDenTeamBoxscores, \
                        DataDenPbpDescription

class TeamHierarchy(DataDenTeamHierarchy):
    """
    TeamHierarchy simply needs to set the right Team model internally.
    """
    team_model = Team

    def __init__(self):
        super().__init__()

    def parse(self, obj):
        super().parse(obj)
        self.team.save()

class GameSchedule(DataDenGameSchedule):
    """
    GameSchedule simply needs to set the right Team & Game model internally
    """
    team_model = Team
    game_model = Game

    def __init__(self):
        super().__init__()

    def parse(self, obj):
        super().parse(obj)

        if self.game:
            self.game.save()

class PlayerRosters(DataDenPlayerRosters):

    team_model      = Team
    player_model    = Player

    def __init__(self):
        super().__init__()

    def parse(self, obj):
        super().parse(obj)
        self.player.save()

class PlayerStats(DataDenPlayerStats):

    game_model          = Game
    player_model        = Player
    player_stats_model  = PlayerStats

    def __init__(self):
        super().__init__()
        self.scorer = NhlSalaryScoreSystem()

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

        #
        # set the fantasy points
        self.ps.fantasy_points = self.scorer.score_player( self.ps )

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

class PeriodPbp(DataDenPbpDescription): # ADD TO PARSER SWITCH
    """
    Parse the list of periods.
    """

    game_model              = Game
    pbp_model               = Pbp
    portion_model           = GamePortion
    pbp_description_model   = PbpDescription

    def __init__(self):
        super().__init__()
        self.KEY_GAME_ID = 'game__id'

    def parse(self, obj, target=None):
        super().parse( obj, target )

        if self.game is None:
            return

        #
        # super().parse() the GamePortions for the periods
        #       so that when the pbp events are parsed
        #       the game,pbp,gameportion exists
        # get or create GamePortion for thsi period
        srid_period     = self.o.get('id', None)
        sequence        = self.o.get('sequence')
        game_portion    = self.get_game_portion( 'period', sequence, save=False ) # defer save
        game_portion.srid = srid_period
        game_portion.save() # now save that we added the srid_period

        events = self.o.get('events__list', [])

        print('events__list count: %s' % str(len(events)))

        idx = 0
        for event_json in events:
            #
            # each event is a pbp item with a description
            srid_event = event_json.get('event', None)
            pbp_desc    = self.get_pbp_description(game_portion, idx, '', save=False) # defer save
            pbp_desc.srid = srid_event # the 'event' is the PbpDescription
            pbp_desc.save()
            idx += 1

            # EventPbp will take care of saving the 'description' field

class EventPbp(DataDenPbpDescription): # ADD TO PARSER SWITCH

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

        # # game, pbp, and GamePortion should all exist.
        # # parse the PbpDescription !
        # srid_period     = self.o.get('period__id', None)
        # desc            = self.o.get('description', '')
        # game_portion    = self.get_game_portion()
        # if game_portion is None:
        #     print( str(self.o) )
        #     print('Currently, there is no existing GamePortion for period %s' % srid_period)
        #     return
        #
        # pbp_desc = self.get_pbp_description(game_portion, overall_idx, desc)
        self.o = obj.get_o() # we didnt call super so we should do this
        srid_pbp_desc = self.o.get('id', None)
        pbp_desc = self.get_pbp_description_by_srid( srid_pbp_desc )
        if pbp_desc:
            description = self.o.get('description', None)
            if pbp_desc.description != description:
                # only save it if its changed
                pbp_desc.description = description
                pbp_desc.save()
        else:
            print( 'pbp_desc not found by srid %s' % srid_pbp_desc)

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
        # nhl.period
        elif self.target == ('nhl.period','pbp'): PeriodPbp().parse( obj )
        #
        # nhl.event
        elif self.target == ('nhl.event','pbp'): EventPbp().parse( obj )
        #
        # nhl.team
        elif self.target == ('nhl.team','hierarchy'): TeamHierarchy().parse( obj )
        elif self.target == ('nhl.team','boxscores'): TeamBoxscores().parse( obj )
        #
        # nhl.player
        elif self.target == ('nhl.player','rosters'): PlayerRosters().parse( obj )
        elif self.target == ('nhl.player','stats'): PlayerStats().parse( obj )

        # elif self.target == ('nhl.event','pbp'): EventPbp().parse( obj )
        #
        # default case, print this message for now
        else: self.unimplemented( self.target[0], self.target[1] )