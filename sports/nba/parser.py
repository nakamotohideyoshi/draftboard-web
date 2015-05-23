#
# sports/nba/models.py
import sports.nba.models
from sports.nba.models import Team, Game, Player, PlayerStats, \
                                GameBoxscore, Pbp, PbpDescription, GamePortion

from sports.sport.base_parser import AbstractDataDenParser, \
                        DataDenTeamHierarchy, DataDenGameSchedule, DataDenPlayerRosters, \
                        DataDenPlayerStats, DataDenGameBoxscores, DataDenTeamBoxscores, \
                        DataDenPbpDescription

import json

class TeamBoxscores(DataDenTeamBoxscores):

    gameboxscore_model = GameBoxscore

    def __init__(self):
        super().__init__()

    def parse(self, obj, target=None):
        super().parse( obj, target )
        # super() does all the work !

class GameBoxscores(DataDenGameBoxscores):
    """
    Updates most boxscore information, BUT:
    Does not update the score of each team, that is handled by TeamBoxscores
    """
    gameboxscore_model  = GameBoxscore
    team_model          = Team

    def __init__(self):
        super().__init__()

    def parse(self, obj, target=None):
        super().parse( obj, target )

        if self.boxscore is None:
            return

        self.boxscore.attendance    = self.o.get('attendance', 0)
        self.boxscore.duration      = self.o.get('duration', '')
        self.boxscore.lead_changes  = self.o.get('lead_changes', 0)
        self.boxscore.quarter       = self.o.get('quarter', '')
        self.boxscore.times_tied    = self.o.get('times_tied', 0)

        self.boxscore.save()

class PlayerRosters(DataDenPlayerRosters):

    team_model      = Team
    player_model    = Player

    def __init__(self):
        super().__init__()

    def parse(self, obj, target=None):
        super().parse( obj, target )

        if self.player is None:
            return

        college         = self.o.get('college', '')
        draft_pick      = self.o.get('draft__list.pick', '')
        draft_round     = self.o.get('draft__list.round', '')
        draft_year      = self.o.get('draft__list.year', '')
        srid_draft_team = self.o.get('draft__list.team_id', '')

        self.player.college          = college
        self.player.draft_pick       = draft_pick
        self.player.draft_round      = draft_round
        self.player.draft_year       = draft_year
        self.player.srid_draft_team  = srid_draft_team

        self.player.save() # commit to db

class TeamHierarchy(DataDenTeamHierarchy):
    """
    Parse an object from which represents a Team for this sport into the db.
    """

    team_model = Team

    def __init__(self):
        super().__init__()

    def parse(self, obj, target=None):
        super().parse( obj, target )

        if self.team is None:
            return

        self.team.save()

class GameSchedule(DataDenGameSchedule):

    team_model  = Team
    game_model  = Game

    def __init__(self):
        super().__init__()

    def parse(self, obj, target=None):
        super().parse( obj, target )

        if self.game is None:
            return

        self.game.save()

# class GameStats(AbstractParseable):
#     def __init__(self):
#         super().__init__()

class PlayerStats(DataDenPlayerStats):

    game_model          = Game
    player_model        = Player
    player_stats_model  = sports.nba.models.PlayerStats

    def __init__(self):
        super().__init__()

    def parse(self, obj, target=None):
        super().parse( obj, target )

        if self.ps is None:
            return

        o = obj.get_o()
        o = o.get('statistics__list', {})
        #   { 'defensive_rebounds': 1.0,
        self.ps.defensive_rebounds = o.get('defensive_rebounds', 0.0)
        #         'two_points_pct': 0.6,
        self.ps.two_points_pct = o.get('two_points_pct', 0.0)
        #         'assists': 0.0,
        self.ps.assists = o.get('assists', 0.0)
        #         'free_throws_att': 2.0,
        self.ps.free_throws_att = o.get('free_throws_att', 0.0)
        #         'flagrant_fouls': 0.0,
        self.ps.flagrant_fouls = o.get('flagrant_fouls', 0.0)
        #         'offensive_rebounds': 1.0,
        self.ps.offensive_rebounds = o.get('offensive_rebounds', 0.0)
        #         'personal_fouls': 0.0,
        self.ps.personal_fouls = o.get('personal_fouls', 0.0)
        #         'field_goals_att': 5.0,
        self.ps.field_goals_att = o.get('field_goals_att', 0.0)
        #         'three_points_att': 0.0,
        self.ps.three_points_att = o.get('three_points_att', 0.0)
        #         'field_goals_pct': 60.0,
        self.ps.field_goals_pct = o.get('field_goals_pct', 0.0)
        #         'turnovers': 0.0,
        self.ps.turnovers = o.get('turnovers', 0.0)
        #         'points': 8.0,
        self.ps.points = o.get('points', 0.0)
        #         'rebounds': 2.0,
        self.ps.rebounds = o.get('rebounds', 0.0)
        #         'two_points_att': 5.0,
        self.ps.two_points_att = o.get('two_points_att', 0.0)
        #         'field_goals_made': 3.0,
        self.ps.field_goals_made = o.get('field_goals_made', 0.0)
        #         'blocked_att': 0.0,
        self.ps.blocked_att = o.get('blocked_att', 0.0)
        #         'free_throws_made': 2.0,
        self.ps.free_throws_made = o.get('free_throws_made', 0.0)
        #         'blocks': 0.0,
        self.ps.blocks = o.get('blocks', 0.0)
        #         'assists_turnover_ratio': 0.0,
        self.ps.assists_turnover_ratio = o.get('assists_turnover_ratio', 0.0)
        #         'tech_fouls': 0.0,
        self.ps.tech_fouls = o.get('tech_fouls', 0.0)
        #         'three_points_made': 0.0,
        self.ps.three_points_made = o.get('three_points_made', 0.0)
        #         'steals': 0.0,
        self.ps.steals = o.get('steals', 0.0)
        #         'two_points_made': 3.0,
        self.ps.two_points_made = o.get('two_points_made', 0.0)
        #         'free_throws_pct': 100.0,
        self.ps.free_throws_pct = o.get('free_throws_pct', 0.0)
        #         'three_points_pct': 0.0
        self.ps.three_points_pct = o.get('three_points_pct', 0.0)

        self.ps.save() # commit changes

class QuarterPbp(DataDenPbpDescription):
    """
    Parse the list of quarters.
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
        game_portion    = self.get_game_portion( 'quarter', sequence, save=False ) # defer save
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

class EventPbp(DataDenPbpDescription):

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

class DataDenNba(AbstractDataDenParser):

    def __init__(self):
        pass

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
        # nba.game
        if self.target == ('nba.game','schedule'): GameSchedule().parse( obj )
        elif self.target == ('nba.game','boxscores'): GameBoxscores().parse( obj )
        #
        # nba.team
        elif self.target == ('nba.team','hierarchy'): TeamHierarchy().parse( obj )
        elif self.target == ('nba.team','boxscores'): TeamBoxscores().parse( obj )
        #
        # nhl.period
        elif self.target == ('nba.quarter','pbp'): QuarterPbp().parse( obj )
        #
        # nhl.event
        elif self.target == ('nba.event','pbp'): EventPbp().parse( obj )
        #
        # nba.player
        elif self.target == ('nba.player','rosters'): PlayerRosters().parse( obj )
        elif self.target == ('nba.player','stats'): PlayerStats().parse( obj )
        #
        # default case, print this message for now
        else: self.unimplemented( self.target[0], self.target[1] )
