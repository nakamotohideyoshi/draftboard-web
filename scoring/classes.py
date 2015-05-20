#
# scoring/classes.py

from scoring.models import ScoreSystem, StatPoint

class AbstractScoreSystem(object):

    score_system    = None
    stat_values     = None

    def __init__(self):
        self.stat_values = self.get_stat_values()
        print('stat_values', str(self.stat_values))
        self.__validate()

    def __validate(self):
        """

        :return:
        """
        if self.score_system is None:
            raise Exception('"score_system" cant be None')
        if self.stat_values is None:
            raise Exception('"stat_values" cant be None')
        if len(self.stat_values) == 0:
            raise Exception('"stat_values" list cant be empty')

    def get_stat_values(self):
        """
        from the db, load the StatValue objects associated with this scoring system
        :return:
        """
        return StatPoint.objects.filter(score_system=self.score_system)

    def format_stat(self, real_stat, stat_value):
        """
        format real_stat to a string in the format the stat_value defines for it.

        ie: format the models "home_run" field value to "2HR"  -- just an example
        """
        return 'format_stat() unimplemented for: real_stat[%s] stat_value[%s]' % \
                                                    (str(real_stat), str(stat_value))

    def get_value_of(self, stat_name):
        """
        internal helper method

        return the value for the stat based on on the scoring system
        """
        stat_value = self.stat_values.get(stat=stat_name)
        return stat_value.value

class NbaSalaryScoreSystem(AbstractScoreSystem):
    """
    defines the NBA Salary Draft scoring metrics
    """

    POINT       = 'point'            # points scored (fgs, foul shots, whatever)
    THREE_PM    = 'three_pm'         # three-point shot made
    REBOUND     = 'rebound'          # any rebound
    ASSIST      = 'assist'           # assists
    STEAL       = 'steal'            # steals
    BLOCK       = 'block'            # blocked shot successful
    TURNOVER    = 'turnover'         # turnovers are worth negative points
    DBL_DBL     = 'dbl-dbl'          # two 10+ categories from (points, rebs, asts, blks, steals)
    TRIPLE_DBL  = 'triple-dbl'       # three 10+ categories from (points, rebs, asts, blks, steals)

    def __init__(self):
        self.score_system = ScoreSystem.objects.get(sport='nba', name='salary')

        #
        # call super last - it will perform validation and ensure proper setup
        super().__init__()

    def score_player(self, player_stats):
        """
        return the fantasy points accrued by this nba PlayerStats object
        """
        total = 0
        total += self.points(player_stats.points)
        total += self.three_pms(player_stats.three_points_made)
        total += self.rebounds(player_stats.rebounds)
        total += self.assists(player_stats.assists)
        total += self.steals(player_stats.steals)
        total += self.blocks(player_stats.blocks)
        total += self.turnovers(player_stats.turnovers)

        #
        # to determined a dbl-dbl or triple-dbl, we have to pass the whole object
        if self.get_tpl_dbl(player_stats):
            total += self.triple_double( self.get_tpl_dbl(player_stats) )
        else:
            total += self.double_double( self.get_dbl_dbl(player_stats) )
        return total

    def points(self, value):
        return value * self.get_value_of(self.POINT)

    def three_pms(self, value):
        return value * self.get_value_of(self.THREE_PM)

    def rebounds(self, value):
        return value * self.get_value_of(self.REBOUND)

    def assists(self, value):
        return value * self.get_value_of(self.ASSIST)

    def steals(self, value):
        return value * self.get_value_of(self.STEAL)

    def blocks(self, value):
        return value * self.get_value_of(self.BLOCK)

    def turnovers(self, value):
        return value * self.get_value_of(self.TURNOVER)

    def double_double(self, value):
        return value * self.get_value_of(self.DBL_DBL)

    def triple_double(self, value):
        return value * self.get_value_of(self.TRIPLE_DBL)

    # return int(1) if player_stats have a double double.
    # a double-double is TWO or more categories from
    # the list with at least a value of 10:
    #           [points, rebs, asts, blks, steals]
    def get_dbl_dbl(self, player_stats):
        return int(self.__double_digits_count(player_stats) >= 2)

    # return int(1) if player_stats have a triple double.
    # a triple double is THREE or more categories from
    # the list with at least a value of 10:
    #           [points, rebs, asts, blks, steals]
    def get_tpl_dbl(self, player_stats):
        return int(self.__double_digits_count(player_stats) >= 3)

    def __double_digits_count(self, player_stats):
        l = [
            player_stats.points,
            player_stats.rebounds,
            player_stats.assists,
            player_stats.blocks,
            player_stats.steals
        ]
        #
        # create a list where we have replaced 10.0+ with int(1),
        # and lesss than 10.0 with int(0).  then sum the list
        # and return that value - thats how many "doubles" we have
        return sum( [ 1 if x >= 10.0 else 0 for x in l ] )

class MlbSalaryScoreSystem(AbstractScoreSystem):
    """
    defines the MLB Salary draft scoring metrics
    """

    SINGLE  = 'single'           # hitter - singles
    DOUBLE  = 'double'           # hitter - doubles
    TRIPLE  = 'triple'           # hitter - triples
    HR      = 'hr'               # hitter - home runs
    RBI     = 'rbi'              # hitter - runs batted in
    RUN     = 'run'              # hitter - runs scored
    BB      = 'bb'               # hitter - walks
    HBP     = 'hbp'              # hitter - hit by pitch
    SB      = 'sb'               # hitter - stolen bases
    CS      = 'cs'               # hitter - # times caught stealing
    # --
    IP      = 'ip'               # pitcher - inning pitched
    K       = 'k'                # pitcher - strikeout
    WIN     = 'win'              # pitcher - Win
    ER      = 'er'               # pitcher - earned runs allowed
    HIT     = 'hit'              # pitcher - hits against
    WALK    = 'walk'             # pitcher - walked batters
    CG      = 'cg'               # pitcher - complete game
    CGSO    = 'cgso'             # pitcher - complete game AND shutout
    NO_HITTER = 'no-hitter'      # pitcher - complete game AND no hits allowed

    def __init__(self):
        self.score_system = ScoreSystem.objects.get(sport='mlb', name='salary')

        # call super last - ensures you have class variables setup
        super().__init__()

    def score_player(self, player_stats):
        """
        determines whether the player_stats object represents a hitter or a pitcher,
        and scores it accordingly.

        :param player_stats:
        :return:
        """
        if player_stats.player.position == 'P':
            return self.__score_pitcher( player_stats )
        else:
            return self.__score_hitter( player_stats )

    def __score_hitter(self, player_stats_hitter):
        """
        return the fantasy points accrued by this mlb PlayerStatsHitter instance
        :param player_stats_hitter:
        :return:
        """
        total = 0.0
        total += self.singles( player_stats_hitter.s )
        total += self.doubles( player_stats_hitter.d )
        total += self.triples( player_stats_hitter.t )
        total += self.home_runs( player_stats_hitter.hr )
        total += self.rbis( player_stats_hitter.rbi )
        total += self.runs( player_stats_hitter.r )
        total += self.bbs( player_stats_hitter.bb )
        total += self.hit_by_pitch( player_stats_hitter.hbp )
        total += self.stolen_bases( player_stats_hitter.sb )
        total += self.caught_stealing( player_stats_hitter.cs )
        return total

    def singles(self, value):
        return value * self.get_value_of(self.SINGLE)
    def doubles(self, value):
        return value * self.get_value_of(self.DOUBLE)
    def triples(self, value):
        return value * self.get_value_of(self.TRIPLE)
    def home_runs(self, value):
        return value * self.get_value_of(self.HR)
    def rbis(self, value):
        return value * self.get_value_of(self.RBI)
    def runs(self, value):
        return value * self.get_value_of(self.RUN)
    def bbs(self, value):
        return value * self.get_value_of(self.BB)
    def hit_by_pitch(self, value):
        return value * self.get_value_of(self.HBP)
    def stolen_bases(self, value):
        return value * self.get_value_of(self.SB)
    def caught_stealing(self, value):
        return value * self.get_value_of(self.CS)

    def __score_pitcher(self, player_stats_pitcher):
        """
        return the fantasy points accrued by this mlb PlayerStatsPitcher instance
        :param player_stats_pitcher:
        :return:
        """
        total = 0.0
        total += self.innings_pitched( float(player_stats_pitcher.ip_1) / 3.0 ) # ip_1 is thirds of an inning
        total += self.strikeouts( player_stats_pitcher.ktotal )
        total += self.wins( int( player_stats_pitcher.win ) ) # int(True) == 1, else 0
        total += self.earned_runs( player_stats_pitcher.er )
        total += self.hits_against( player_stats_pitcher.h )
        total += self.walks_against( player_stats_pitcher.bb ) # pitcher has bb property
        total += self.complete_game( int(player_stats_pitcher.cg) )
        total += self.complete_game_shutout( int( player_stats_pitcher.cgso ) )
        total += self.no_hitter( int( player_stats_pitcher.nono ) )
        return total

    def innings_pitched(self, value):
        return value * self.get_value_of(self.IP)
    def strikeouts(self, value):
        return value * self.get_value_of(self.K)
    def wins(self, value):
        return value * self.get_value_of(self.WIN)
    def earned_runs(self, value):
        return value * self.get_value_of(self.ER)
    def hits_against(self, value):
        return value * self.get_value_of(self.HIT)
    def walks_against(self, value):
        return value * self.get_value_of(self.WALK)
    def complete_game(self, value):
        return value * self.get_value_of(self.CG)
    def complete_game_shutout(self, value):
        return value * self.get_value_of(self.CGSO)
    def no_hitter(self, value):
        return value * self.get_value_of(self.NO_HITTER)

class NhlSalaryScoreSystem(AbstractScoreSystem):
    """
    defines the NHL Salary draft scoring metrics
    """

    GOAL        = 'goal'          # goals scored
    ASSIST      = 'assist'        # assists
    SOG         = 'sog'           # shots on goal
    BLK         = 'blk'           # blocked shot
    SH_BONUS    = 'sh-bonus'      # bonus points for goals/assists when shorthanded
    SO_GOAL     = 'so-goal'       # goal in a shootout
    HAT         = 'hat'           # hattrick is 3 goals scored

    WIN         = 'win'           # goalie - win
    SAVE        = 'save'          # goalie - shots saved
    GA          = 'ga'            # goalie - goals allowed
    SHUTOUT     = 'shutout'       # goalie - complete game(includes OT) no goals (doesnt count shootout goals)

    def __init__(self):
        self.score_system = ScoreSystem.objects.get(sport='nhl', name='salary')

        # call super last - ensures you have class variables setup
        super().__init__()

    def score_player(self, player_stats):
        """
        scores and returns a float for the amount of fantasy points for this PlayerStats instance

        :param player_stats:
        :return:
        """
        total = 0.0

        # skater stats
        total += self.goals(player_stats.goal)
        total += self.assists(player_stats.assist)
        total += self.shots_on_goal(player_stats.sog)
        total += self.blocks( player_stats.blk )
        total += self.short_handed_bonus(player_stats.sh_goal)
        total += self.shootout_goals(player_stats.so_goal)
        total += self.hattrick(player_stats.goal) # goals minus shootout goals

        # goalie stats
        total += self.win(player_stats.w)
        total += self.saves(player_stats.saves)
        total += self.goals_allowed(player_stats.ga)
        total += self.shutout(player_stats.shutout)

        return total

    def goals(self, val):
        return val * self.get_value_of(self.GOAL)
    def assists(self, val):
        return val * self.get_value_of(self.ASSIST)
    def shots_on_goal(self, val):
        return val * self.get_value_of(self.SOG)
    def blocks(self, val):
        return val * self.get_value_of(self.BLK)
    def short_handed_bonus(self, sh_goals):
        return sh_goals * self.get_value_of(self.SH_BONUS)
    def shootout_goals(self, so_goals):
        return so_goals * self.get_value_of(self.SO_GOAL)
    def hattrick(self, tot_goals):
        return int(tot_goals >= 3) * self.get_value_of(self.HAT) # ie: 0 or 1 times the value of a hattrick
    def win(self, val):
        return int(val) * self.get_value_of(self.WIN)
    def saves(self, val):
        return val * self.get_value_of(self.SAVE)
    def goals_allowed(self, val):
        return val * self.get_value_of(self.GA)
    def shutout(self, val):
        return int(val) * self.get_value_of(self.SHUTOUT)

class NflSalaryScoreSystem(AbstractScoreSystem):
    """
    defines the NFL Salary draft scoring metrics
    """

    PASS_TD     = 'pass-td'         # thrown touchdowns
    PASS_YDS    = 'pass-yds'        # pts per passing yard
    PASS_BONUS  = 'pass-bonus'      # bonus for passing 300+ yards
    PASS_INT    = 'pass-int'        # passed interceptions

    RUSH_YDS    = 'rush-yds'        # rushing points per yard
    RUSH_TD     = 'rush-td'         # rushed touchdowns
    RUSH_BONUS  = 'rush-bonus'      # bonus for rushing 100+ yards

    REC_YDS     = 'rec-yds'         # receiving points per yard
    REC_TD      = 'rec-td'          # receiving touchdowns
    REC_BONUS   = 'rec-bonus'       # bonus for receiving 100+ yards

    PPR         = 'ppr'             # points per reception

    FUMBLE_LOST = 'fumble-lost'     # fumble lost (offensive player)
    TWO_PT_CONV = 'two-pt-conv'     # passed, rushed, or received succesful 2-pt conversion
    OFF_FUM_TD  = 'off-fum-td'      # offensive fumble recovered for TD (unique situation)

    # -- dst scoring --
    SACK        = 'sack'                # sacks
    INTS        = 'ints'                # interceptions
    FUM_REC     = 'fum-rec'             # fumble recoveries
    KICK_RET_TD     = 'kick-ret-td'         # kickoff returned for TD
    PUNT_RET_TD     = 'punt-ret-td'         # punt returned for TD
    INT_RET_TD      = 'int-ret-td'          # int returned for TD
    FUM_RET_TD      = 'fum-ret-td'          # fumble recovered for TD
    BLK_PUNT_RET_TD = 'blk-punt-ret-td' # blocked punt returned for TD
    FG_RET_TD       = 'fg-ret-td'           # missed FG, returned for TD
    BLK_FG_RET_TD   = 'blk-fg-ret-td'

    SAFETY      = 'safety'              # safeties
    BLK_KICK    = 'blk-kick'            # blocked kick

    PA_0        = 'pa-0'        # 0 points allowed
    PA_6        = 'pa-6'        # 6 or less points allowed
    PA_13       = 'pa-13'       # 13 or less points allowed
    PA_20       = 'pa-20'       # 20 or less points allowed
    PA_27       = 'pa-27'       # 27 or less points allowed
    PA_34       = 'pa-34'       # 34 or less points allowed
    PA_35_PLUS  = 'pa-35plus'   # 35 or MORE points allowed

    def __init__(self):
        self.score_system = ScoreSystem.objects.get(sport='nfl', name='salary')

        self.PASSING_BONUS_REQUIRED_YDS = 300
        self.RUSHING_BONUS_REQUIRED_YDS = 100
        self.RECEIVING_BONUS_REQUIRED_YDS = 100

        # call super last - ensures you have class variables setup
        super().__init__()

    def score_player(self, player_stats):
        """
        scores and returns a float for the amount of fantasy points for this PlayerStats instance

        :param player_stats:
        :return:
        """
        total = 0.0

        # passing
        total += self.passing_yds(player_stats.pass_yds)
        total += self.passing_tds(player_stats.pass_td)
        total += self.passing_bonus(int(player_stats.pass_yds >= self.PASSING_BONUS_REQUIRED_YDS))
        total += self.passing_interceptions(player_stats.pass_int)
        # rushing
        total += self.rushing_yds(player_stats.rush_yds)
        total += self.rushing_tds(player_stats.rush_td)
        total += self.rushing_bonus(int(player_stats.rush_yds >= self.RUSHING_BONUS_REQUIRED_YDS))
        # receiving
        total += self.receiving_yds(player_stats.rec_yds)
        total += self.receiving_tds(player_stats.rec_td)
        total += self.receiving_bonus(int(player_stats.rec_yds >= self.RECEIVING_BONUS_REQUIRED_YDS))
        total += self.ppr(player_stats.rec_rec)
        # misc
        total += self.fumble_lost(player_stats.off_fum_lost)
        total += self.two_pt_conversion(player_stats.two_pt_conv)
        total += self.offensive_fumble_td(player_stats.off_fum_rec_td)

        #
        # dst scoring
        total += self.sacks(player_stats.sack)
        total += self.interceptions(player_stats.ints)
        total += self.fumble_recoveries(player_stats.fum_rec)
        total += self.safeties(player_stats.sfty)
        total += self.blocked_kicks(player_stats.blk_kick)
        # dst touchdowns
        total += self.kick_return_tds(player_stats.ret_kick_td)
        total += self.punt_return_tds(player_stats.ret_punt_td)
        total += self.interception_return_tds(player_stats.ret_int_td)
        total += self.fumble_return_tds(player_stats.ret_fum_td)
        total += self.blocked_punt_return_tds(player_stats.ret_blk_punt_td)
        total += self.field_goal_return_tds(player_stats.ret_fg_td)

        dst_pa = self.get_dst_points_allowed(player_stats)
        total += self.get_dst_pa_bracket_points( dst_pa )

        return total

    # offensive scoring methods below:
    def passing_yds(self, val):
        return val * self.get_value_of(self.PASS_YDS)
    def passing_tds(self, val):
        return val * self.get_value_of(self.PASS_TD)
    def passing_bonus(self, val):
        return val * self.get_value_of(self.PASS_BONUS)
    def passing_interceptions(self, val):
        return val * self.get_value_of(self.PASS_INT)
    def rushing_yds(self, val):
        return val * self.get_value_of(self.RUSH_YDS)
    def rushing_tds(self, val):
        return val * self.get_value_of(self.RUSH_TD)
    def rushing_bonus(self, val):
        return val * self.get_value_of(self.RUSH_BONUS)
    def receiving_yds(self, val):
        return val * self.get_value_of(self.REC_YDS)
    def receiving_tds(self, val):
        return val * self.get_value_of(self.REC_TD)
    def receiving_bonus(self, val):
        return val * self.get_value_of(self.REC_BONUS)
    def ppr(self, val):
        return val * self.get_value_of(self.PPR)
    def fumble_lost(self, val):
        return val * self.get_value_of(self.FUMBLE_LOST)
    def two_pt_conversion(self, val):
        return val * self.get_value_of(self.TWO_PT_CONV)
    def offensive_fumble_td(self, val):
        return val * self.get_value_of(self.OFF_FUM_TD)

    # defensive scoring methods below:
    def sacks(self, val):
        return val * self.get_value_of(self.SACK)
    def interceptions(self, val):
        return val * self.get_value_of(self.INTS)
    def fumble_recoveries(self, val):
        return val * self.get_value_of(self.FUM_REC)
    # types of return touchdowns
    def kick_return_tds(self, val):
        return val * self.get_value_of(self.KICK_RET_TD)
    def punt_return_tds(self, val):
        return val * self.get_value_of(self.PUNT_RET_TD)
    def interception_return_tds(self, val):
        return val * self.get_value_of(self.INT_RET_TD)
    def fumble_return_tds(self, val):
        return val * self.get_value_of(self.FUM_RET_TD)
    def blocked_punt_return_tds(self, val):
        return val * self.get_value_of(self.BLK_PUNT_RET_TD)
    def field_goal_return_tds(self, val):
        return val * self.get_value_of(self.FG_RET_TD)
    def blocked_field_goal_return_tds(self, val):
        return val * self.get_value_of(self.BLK_FG_RET_TD)
    # misc dst
    def safeties(self, val): # safety
        return val * self.get_value_of(self.SAFETY)
    def blocked_kicks(self, val): # blocked kick (punts, fgs)
        return val * self.get_value_of(self.BLK_KICK)

    def get_dst_points_allowed(self, player_stats): # dst points allowed
        """
        DST fantasy scoring is based on the "points the DST has allowed".
        This does not include points the teams Offense has allowed!
        We disregard 6 points for interceptions and fumbles returned for TDs,
        as well as 2 points for safeties against the offense for which the DST plays.

        :param player_stats:
        :return:
        """
        opp_total_points = 0 # TODO - get the nominal number of points the opposing team scored
        dst_points_allowed = opp_total_points
        dst_points_allowed -= player_stats.int_td_against
        dst_points_allowed -= player_stats.fum_td_against
        dst_points_allowed -= player_stats.off_pass_sfty
        dst_points_allowed -= player_stats.off_rush_sfty
        dst_points_allowed -= player_stats.off_punt_sfty
        return dst_points_allowed

    def get_dst_pa_bracket_points(self, dst_pa):
        """
        this method returns the fantasy points bonus associated with
        how few (or a potential penalty) points the DST allowed in the game.
        The "dst_pa" is points the opposing team scored against the DST only.
        Ie: "dst_pa" does not include points which their offense gave up,
        which result from interecption/fumble return TDs and safeties.

        "dst_pa" includes, but is not limited to: extra points, field goals,
        passing/rushing/receiving/kick-return/punt-return tds.

        :param dst_pa:
        :return:
        """
        if dst_pa <= 0:
            return self.get_value_of(self.PA_0) # 0 points allowed bracket
        elif dst_pa <= 6:
            return self.get_value_of(self.PA_6)
        elif dst_pa <= 13:
            return self.get_value_of(self.PA_13)
        elif dst_pa <= 20:
            return self.get_value_of(self.PA_20)
        elif dst_pa <= 27:
            return self.get_value_of(self.PA_27)
        elif dst_pa <= 34:
            return self.get_value_of(self.PA_34)
        else:
            return self.get_value_of(self.PA_35_PLUS)