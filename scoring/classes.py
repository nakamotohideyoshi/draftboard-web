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
        total += self.double_double( self.get_dbl_dbl(player_stats) )
        total += self.triple_double( self.get_tpl_dbl(player_stats) )
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
