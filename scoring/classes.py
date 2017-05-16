import sports.mlb.models
import sports.nba.models
import sports.nfl.models
import sports.nhl.models
from scoring.cache import ScoreSystemCache
from scoring.models import ScoreSystem, StatPoint


class AbstractScoreSystem(object):
    class MustOverrideMethodException(Exception):
        pass

    class PrimaryPlayerStatsClassException(Exception):
        pass

    score_system = None
    stat_values = None

    def __init__(self, sport, validate=True):
        self.sport = sport
        self.verbose = False
        self.str_stats = None  # string

        self.stat_values_cache = ScoreSystemCache(sport)
        self.stat_values = self.get_stat_values()
        # print('stat_values', str(self.stat_values))
        if validate:
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

    def set_verbose(self, verbose):
        if verbose:
            self.str_stats = ''
            self.verbose = True
        else:
            self.verbose = False
            self.str_stats = None

    def get_stat_values(self):
        """
        TODO - the cache was taken out of this method for testing purposes
               It should be put back in for production.

        from the db, load the StatValue objects associated with this scoring system
        :return:
        """

        # temp code without cache:
        db_stat_values = StatPoint.objects.filter(score_system=self.score_system)
        # set them in the cache
        self.stat_values_cache.add_stat_values(db_stat_values)
        # return them
        return db_stat_values

    @staticmethod
    def format_stat(real_stat, stat_value):
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
        # print( str(self.stat_values), stat_name)
        stat_value = self.stat_values.get(stat=stat_name)
        return stat_value.value

    def get_primary_player_stats_class_for_player(self, player):
        """
        this method will get the primary PlayerStats model class
        for which to score a players fantasy points for contests.

        given a sports.<sport>.models.Player object, uses the
        player's position to disambiguate which PlayerStats model
        to return in the case there are more than one.

        for most sports, this method always the same PlayerStats object
        for all players, but for MLB, for example, this returns
        the PlayerStats class based on players position. (ie: we
        need to return PlayerStatsHitter for hitters, and PlayerStatsPitcher
        for players whose main position is in the list of pitching positions.

        by default this method returns the first class found
        in the SiteSportManager.get_player_stats_class() return list.

        note: inheriting classes of sports with more than one PlayerStats
        model must consider overriding this method so player's fantasy points
        are scored properly!
        """

        err_msg = 'object inheriting AbstractScoreSystem for sport [%s] must override method ' \
                  'get_primary_player_stats_class_for_player()' % self.sport
        raise self.PrimaryPlayerStatsClassException(err_msg)

    def get_outcome_fantasy_points(self, outcome_id):
        """
        originally the term 'outcome_id' (or 'oid' its called sometimes,
        was originally a baseball term for the type of pbp "event".

        we should create our own outcomes if necessary so that all sports
        can use this generic method for their particular scoring system.
        """
        err_msg = '%s.get_outcome_fantasy_points(outcome_id)' % self.__class__.__name__
        raise self.MustOverrideMethodException(err_msg)


class NbaSalaryScoreSystem(AbstractScoreSystem):
    """
    defines the NBA Salary Draft scoring metrics
    """
    THE_SPORT = 'nba'

    POINT = 'point'  # points scored (fgs, foul shots, whatever)
    THREE_PM = 'three_pm'  # three-point shot made
    REBOUND = 'rebound'  # any rebound
    ASSIST = 'assist'  # assists
    STEAL = 'steal'  # steals
    BLOCK = 'block'  # blocked shot successful
    TURNOVER = 'turnover'  # turnovers are worth negative points
    DBL_DBL = 'dbl-dbl'  # two 10+ categories from (points, rebs, asts, blks, steals)
    TRIPLE_DBL = 'triple-dbl'  # three 10+ categories from (points, rebs, asts, blks, steals)

    def __init__(self):
        self.score_system = ScoreSystem.objects.get(sport=self.THE_SPORT, name='salary')

        #
        # call super last - it will perform validation and ensure proper setup
        super().__init__(self.THE_SPORT)

    def get_primary_player_stats_class_for_player(self, player):
        """
        override
        """
        return sports.nba.models.PlayerStats

    def score_player(self, player_stats, verbose=True):
        """
        return the fantasy points accrued by this nba PlayerStats object
        """
        self.set_verbose(verbose)

        total = 0
        total += self.points(player_stats.points)
        total += self.three_pms(player_stats.three_points_made)
        total += self.rebounds(player_stats.rebounds)
        total += self.assists(player_stats.assists)
        total += self.steals(player_stats.steals)
        total += self.blocks(player_stats.blocks)
        total += self.turnovers(player_stats.turnovers)
        # you can get the triple dbl
        total += self.triple_double(self.get_tpl_dbl(player_stats))
        # as well as the dbl dbl bonus .. they stack
        total += self.double_double(self.get_dbl_dbl(player_stats))
        return total

    def points(self, value):
        if self.verbose:
            self.str_stats += '%s Pts ' % value
        return value * self.get_value_of(self.POINT)

    def three_pms(self, value):
        if self.verbose:
            self.str_stats += '%s ThreePm ' % value
        return value * self.get_value_of(self.THREE_PM)

    def rebounds(self, value):
        if self.verbose:
            self.str_stats += '%s Reb ' % value
        return value * self.get_value_of(self.REBOUND)

    def assists(self, value):
        if self.verbose:
            self.str_stats += '%s Ast ' % value
        return value * self.get_value_of(self.ASSIST)

    def steals(self, value):
        if self.verbose:
            self.str_stats += '%s Stl ' % value
        return value * self.get_value_of(self.STEAL)

    def blocks(self, value):
        if self.verbose:
            self.str_stats += '%s Blk ' % value
        return value * self.get_value_of(self.BLOCK)

    def turnovers(self, value):
        if self.verbose:
            self.str_stats += '%s TO ' % value
        return value * self.get_value_of(self.TURNOVER)

    def double_double(self, value):
        if self.verbose:
            self.str_stats += '%s DblDbl ' % value
        return value * self.get_value_of(self.DBL_DBL)

    def triple_double(self, value):
        if self.verbose:
            self.str_stats += '%s TrpDbl ' % value
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

    @staticmethod
    def __double_digits_count(player_stats):
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
        return sum([1 if x >= 10.0 else 0 for x in l])


class MlbSalaryScoreSystem(AbstractScoreSystem):
    """
    defines the MLB Salary draft scoring metrics
    """

    THE_SPORT = 'mlb'

    PITCHER_POSITIONS = ['P', 'SP', 'RP']

    SINGLE = 'single'  # hitter - singles
    DOUBLE = 'double'  # hitter - doubles
    TRIPLE = 'triple'  # hitter - triples
    HR = 'hr'  # hitter - home runs
    RBI = 'rbi'  # hitter - runs batted in
    RUN = 'run'  # hitter - runs scored
    BB = 'bb'  # hitter - walks
    IBB = 'ibb'  # hitter - intentional base on balls
    HBP = 'hbp'  # hitter - hit by pitch
    SB = 'sb'  # hitter - stolen bases
    CS = 'cs'  # hitter - # times caught stealing
    # --
    IP = 'ip'  # pitcher - inning pitched
    K = 'k'  # pitcher - strikeout
    WIN = 'win'  # pitcher - Win
    ER = 'er'  # pitcher - earned runs allowed
    HIT = 'hit'  # pitcher - hits against
    HIT_BATSMAN = 'hit-batsman'  # pitcher - hit batter with pitch
    WALK = 'walk'  # pitcher - walked batters
    IWALK = 'iwalk'  # pitcher - intentionally walked batters
    CG = 'cg'  # pitcher - complete game
    CGSO = 'cgso'  # pitcher - complete game AND shutout
    NO_HITTER = 'no-hitter'  # pitcher - complete game AND no hits allowed

    # the mlb outcomes, unsullied by our guesses as to what is worth how-many fantasy points.
    OUTCOMES = {
        'AD1': (0.0, 'Advance 1st'),
        'AD2': (0.0, 'Advance 2nd'),
        'AD3': (0.0, 'Advance 3rd'),
        'CK': (0.0, 'Checked'),
        'CS2': (0.0, 'Caught Stealing 2nd'),
        'CS3': (0.0, 'Caught Stealing 3rd'),
        'CS4': (0.0, 'Caught Stealing Home'),
        'DI2': (0.0, 'Indifference to 2nd'),
        'DI3': (0.0, 'Indifference to 3rd'),
        'DO1': (0.0, 'Doubled off 1st'),
        'DO2': (0.0, 'Doubled off 2nd'),
        'DO3': (0.0, 'Doubled off 3rd'),
        'ERN': (0.0, 'Earned Run/RBI'),
        'FO1': (0.0, 'Force out 1st'),
        'FO2': (0.0, 'Force out 2nd'),
        'FO3': (0.0, 'Force out 3rd'),
        'FO4': (0.0, 'Force out Home'),
        'HBB': (0.0, 'Hit by Batted Ball'),
        'OBP': (0.0, 'Out of Base Path'),
        'OOA': (0.0, 'Out on Appeal'),
        'PO': (0.0, 'Pickoff'),
        'POCS2': (0.0, 'Pickoff/Caught Stealing 2nd'),
        'POCS3': (0.0, 'Pickoff/Caught Stealing 3rd'),
        'POCS4': (0.0, 'Pickoff/Caught Stealing Home'),
        'RI': (0.0, 'Runner Interference'),
        'SB2': (0.0, 'Stole 2nd'),
        'SB2E3': (0.0, 'Stole 2nd, error to 3rd'),
        'SB2E4': (0.0, 'Stole 2nd, error to Home'),
        'SB3': (0.0, 'Stole 3rd'),
        'SB3E4': (0.0, 'Stole 3rd, error to Home'),
        'SB4': (0.0, 'Stole Home'),
        'TO2': (0.0, 'Tag out 2nd'),
        'TO3': (0.0, 'Tag out 3rd'),
        'TO4': (0.0, 'Tag out Home'),
        'URN': (0.0, 'Unearned Run/RBI'),
        'aBK': (0.0, 'Balk'),
        'aCI': (0.0, 'Catcher Interference'),
        'aD': (0.0, 'Double'),
        'aDAD3': (0.0, 'Double - Adv 3rd'),
        'aDAD4': (0.0, 'Double - Adv Home'),
        'aFCAD2': (0.0, 'Fielders Choice - Adv 2nd'),
        'aFCAD3': (0.0, 'Fielders Choice - Adv 3rd'),
        'aFCAD4': (0.0, 'Fielders Choice - Adv Home'),
        'aHBP': (0.0, 'Hit By Pitch'),
        'aHR': (0.0, 'Homerun'),
        'aKLAD1': (0.0, 'Strike Looking - Adv 1st'),
        'aKLAD2': (0.0, 'Strike Looking - Adv 2nd'),
        'aKLAD3': (0.0, 'Strike Looking - Adv 3rd'),
        'aKLAD4': (0.0, 'Strike Looking - Adv Home'),
        'aKSAD1': (0.0, 'Strike Swinging - Adv 1st'),
        'aKSAD2': (0.0, 'Strike Swinging - Adv 2nd'),
        'aKSAD3': (0.0, 'Strike Swinging - Adv 3rd'),
        'aKSAD4': (0.0, 'Strike Swinging - Adv Home'),
        'aROE': (0.0, 'Reached On Error'),
        'aROEAD2': (0.0, 'Reached On Error - Adv 2nd'),
        'aROEAD3': (0.0, 'Reached On Error - Adv 3rd'),
        'aROEAD4': (0.0, 'Reached On Error - Adv Home'),
        'aS': (0.0, 'Single'),
        'aSAD2': (0.0, 'Single - Adv 2nd'),
        'aSAD3': (0.0, 'Single - Adv 3rd'),
        'aSAD4': (0.0, 'Single - Adv Home'),
        'aSBAD1': (0.0, 'Sacrifice Bunt - Adv 1st'),
        'aSBAD2': (0.0, 'Sacrifice Bunt - Adv 2nd'),
        'aSBAD3': (0.0, 'Sacrifice Bunt - Adv 3rd'),
        'aSBAD4': (0.0, 'Sacrifice Bunt - Adv Home'),
        'aSFAD1': (0.0, 'Sacrifice Fly - Adv 1st'),
        'aSFAD2': (0.0, 'Sacrifice Fly - Adv 2nd'),
        'aSFAD3': (0.0, 'Sacrifice Fly - Adv 3rd'),
        'aSFAD4': (0.0, 'Sacrifice Fly - Adv Home'),
        'aT': (0.0, 'Triple'),
        'aTAD4': (0.0, 'Triple - Adv Home'),
        'bB': (0.0, 'Ball'),
        'bDB': (0.0, 'Dirt Ball'),
        'bIB': (0.0, 'iBall'),
        'bPO': (0.0, 'Pitchout'),
        'eRN': (0.0, 'Earned Run/No RBI'),
        'kF': (0.0, 'Foul Ball'),
        'kFT': (0.0, 'Foul Tip'),
        'kKL': (0.0, 'Strike Looking'),
        'kKS': (0.0, 'Strike Swinging'),
        'oBI': (0.0, 'Batter Interference'),
        'oDT3': (0.0, 'Double - Out at 3rd'),
        'oDT4': (0.0, 'Double - Out at Home'),
        'oFC': (0.0, 'Fielders Choice'),
        'oFCT2': (0.0, 'Fielders Choice - Out at 2nd'),
        'oFCT3': (0.0, 'Fielders Choice - Out at 3rd'),
        'oFCT4': (0.0, 'Fielders Choice - Out at Home'),
        'oFO': (0.0, 'Fly Out'),
        'oGO': (0.0, 'Ground Out'),
        'oKLT1': (0.0, 'Strike Looking - Out at 1st'),
        'oKLT2': (0.0, 'Strike Looking - Out at 2nd'),
        'oKLT3': (0.0, 'Strike Looking - Out at 3rd'),
        'oKLT4': (0.0, 'Strike Looking - Out at Home'),
        'oKST1': (0.0, 'Strike Swinging - Out at 1st'),
        'oKST2': (0.0, 'Strike Swinging - Out at 2nd'),
        'oKST3': (0.0, 'Strike Swinging - Out at 3rd'),
        'oKST4': (0.0, 'Strike Swinging - Out at Home'),
        'oLO': (0.0, 'Line Out'),
        'oOBB': (0.0, 'Out of Batters Box'),
        'oOP': (0.0, 'Out on Appeal'),
        'oPO': (0.0, 'Pop Out'),
        'oROET2': (0.0, 'Reached On Error - Out at 2nd'),
        'oROET3': (0.0, 'Reached On Error - Out at 3rd'),
        'oROET4': (0.0, 'Reached On Error - Out at Home'),
        'oSB': (0.0, 'Sacrifice Bunt'),
        'oSBT2': (0.0, 'Sacrifice Bunt - Out at 2nd'),
        'oSBT3': (0.0, 'Sacrifice Bunt - Out at 3rd'),
        'oSBT4': (0.0, 'Sacrifice Bunt - Out at Home'),
        'oSF': (0.0, 'Sacrifice Fly'),
        'oSFT2': (0.0, 'Sacrifice Fly - Out at 2nd'),
        'oSFT3': (0.0, 'Sacrifice Fly - Out at 3rd'),
        'oSFT4': (0.0, 'Sacrifice Fly - Out at Home'),
        'oST2': (0.0, 'Single - Out at 2nd'),
        'oST3': (0.0, 'Single - Out at 3rd'),
        'oST4': (0.0, 'Single - Out at Home'),
        'oTT4': (0.0, 'Triple - Out at Home'),
        'uRN': (0.0, 'Unearned Run/No RBI'),
    }

    def __init__(self):
        self.score_system = ScoreSystem.objects.get(sport=self.THE_SPORT, name='salary')

        # call super last - ensures you have class variables setup
        super().__init__(self.THE_SPORT)

        # the mlb outcomes:
        self.outcomes = {

            # runner outcomes - 1st character is Upper case!
            'AD1': (self.get_value_of(self.SINGLE), 'Advance 1st'),  # or BB, or HBP?
            'AD2': (0.0, 'Advance 2nd'),
            'AD3': (0.0, 'Advance 3rd'),
            'CK': (0.0, 'Checked'),
            'CS2': (self.get_value_of(self.CS), 'Caught Stealing 2nd'),
            'CS3': (self.get_value_of(self.CS), 'Caught Stealing 3rd'),
            'CS4': (self.get_value_of(self.CS), 'Caught Stealing Home'),
            'DI2': (0.0, 'Indifference to 2nd'),
            'DI3': (0.0, 'Indifference to 3rd'),
            'DO1': (0.0, 'Doubled off 1st'),
            'DO2': (0.0, 'Doubled off 2nd'),
            'DO3': (0.0, 'Doubled off 3rd'),
            'ERN': (self.get_value_of(self.RUN), 'Earned Run/RBI'),
            'FO1': (0.0, 'Force out 1st'),
            'FO2': (0.0, 'Force out 2nd'),
            'FO3': (0.0, 'Force out 3rd'),
            'FO4': (0.0, 'Force out Home'),
            'HBB': (0.0, 'Hit by Batted Ball'),
            'OBP': (0.0, 'Out of Base Path'),
            'OOA': (0.0, 'Out on Appeal'),
            'PO': (0.0, 'Pickoff'),
            'POCS2': (self.get_value_of(self.CS), 'Pickoff/Caught Stealing 2nd'),
            'POCS3': (self.get_value_of(self.CS), 'Pickoff/Caught Stealing 3rd'),
            'POCS4': (self.get_value_of(self.CS), 'Pickoff/Caught Stealing Home'),
            'RI': (0.0, 'Runner Interference'),
            'SB2': (self.get_value_of(self.SB), 'Stole 2nd'),
            'SB2E3': (self.get_value_of(self.SB), 'Stole 2nd, error to 3rd'),
            'SB2E4': (self.get_value_of(self.SB), 'Stole 2nd, error to Home'),  # +RUN?
            'SB3': (self.get_value_of(self.SB), 'Stole 3rd'),
            'SB3E4': (self.get_value_of(self.SB), 'Stole 3rd, error to Home'),  # +RUN?
            'SB4': (self.get_value_of(self.SB), 'Stole Home'),  # +RUN?
            'TO2': (0.0, 'Tag out 2nd'),
            'TO3': (0.0, 'Tag out 3rd'),
            'TO4': (0.0, 'Tag out Home'),
            'URN': (self.get_value_of(self.RUN), 'Unearned Run/RBI'),

            # hitter outcomes - 1st character is lower case!
            'aBK': (0.0, 'Balk'),
            'aCI': (0.0, 'Catcher Interference'),
            'aD': (self.get_value_of(self.DOUBLE), 'Double'),
            'aDAD3': (self.get_value_of(self.DOUBLE), 'Double - Adv 3rd'),
            'aDAD4': (self.get_value_of(self.DOUBLE), 'Double - Adv Home'),  # +RUN?
            'aFCAD2': (0.0, 'Fielders Choice - Adv 2nd'),
            'aFCAD3': (0.0, 'Fielders Choice - Adv 3rd'),
            'aFCAD4': (0.0, 'Fielders Choice - Adv Home'),  # +RUN?
            'aHBP': (self.get_value_of(self.HBP), 'Hit By Pitch'),
            'aHR': (self.get_value_of(self.HR), 'Homerun'),
            'aKLAD1': (0.0, 'Strike Looking - Adv 1st'),  # dropped 3rd strike?
            'aKLAD2': (0.0, 'Strike Looking - Adv 2nd'),  # dropped 3rd strike?
            'aKLAD3': (0.0, 'Strike Looking - Adv 3rd'),  # dropped 3rd strike?
            'aKLAD4': (0.0, 'Strike Looking - Adv Home'),  # dropped 3rd strike?   # +RUN?
            'aKSAD1': (0.0, 'Strike Swinging - Adv 1st'),  # dropped 3rd strike?
            'aKSAD2': (0.0, 'Strike Swinging - Adv 2nd'),  # dropped 3rd strike?
            'aKSAD3': (0.0, 'Strike Swinging - Adv 3rd'),  # dropped 3rd strike?
            'aKSAD4': (0.0, 'Strike Swinging - Adv Home'),  # dropped 3rd strike?   # +RUN?
            'aROE': (0.0, 'Reached On Error'),
            'aROEAD2': (0.0, 'Reached On Error - Adv 2nd'),
            'aROEAD3': (0.0, 'Reached On Error - Adv 3rd'),
            'aROEAD4': (0.0, 'Reached On Error - Adv Home'),  # +RUN?
            'aS': (self.get_value_of(self.SINGLE), 'Single'),
            'aSAD2': (self.get_value_of(self.SINGLE), 'Single - Adv 2nd'),
            'aSAD3': (self.get_value_of(self.SINGLE), 'Single - Adv 3rd'),
            'aSAD4': (self.get_value_of(self.SINGLE), 'Single - Adv Home'),  # +RUN?
            'aSBAD1': (0.0, 'Sacrifice Bunt - Adv 1st'),
            'aSBAD2': (0.0, 'Sacrifice Bunt - Adv 2nd'),
            'aSBAD3': (0.0, 'Sacrifice Bunt - Adv 3rd'),
            'aSBAD4': (0.0, 'Sacrifice Bunt - Adv Home'),  # +RUN?
            'aSFAD1': (0.0, 'Sacrifice Fly - Adv 1st'),
            'aSFAD2': (0.0, 'Sacrifice Fly - Adv 2nd'),
            'aSFAD3': (0.0, 'Sacrifice Fly - Adv 3rd'),
            'aSFAD4': (0.0, 'Sacrifice Fly - Adv Home'),  # +RUN?
            'aT': (self.get_value_of(self.TRIPLE), 'Triple'),
            'aTAD4': (self.get_value_of(self.TRIPLE), 'Triple - Adv Home'),  # +RUN?
            'bB': (0.0, 'Ball'),
            'bDB': (0.0, 'Dirt Ball'),
            'bIB': (0.0, 'iBall'),
            'bPO': (0.0, 'Pitchout'),
            'eRN': (0.0, 'Earned Run/No RBI'),
            'kF': (0.0, 'Foul Ball'),
            'kFT': (0.0, 'Foul Tip'),
            'kKL': (0.0, 'Strike Looking'),
            'kKS': (0.0, 'Strike Swinging'),
            'oBI': (0.0, 'Batter Interference'),
            'oDT3': (self.get_value_of(self.DOUBLE), 'Double - Out at 3rd'),
            'oDT4': (self.get_value_of(self.DOUBLE), 'Double - Out at Home'),
            'oFC': (0.0, 'Fielders Choice'),
            'oFCT2': (0.0, 'Fielders Choice - Out at 2nd'),
            'oFCT3': (0.0, 'Fielders Choice - Out at 3rd'),
            'oFCT4': (0.0, 'Fielders Choice - Out at Home'),
            'oFO': (0.0, 'Fly Out'),
            'oGO': (0.0, 'Ground Out'),
            'oKLT1': (0.0, 'Strike Looking - Out at 1st'),  # dropped 3rd strike?
            'oKLT2': (0.0, 'Strike Looking - Out at 2nd'),  # dropped 3rd strike?
            'oKLT3': (0.0, 'Strike Looking - Out at 3rd'),  # dropped 3rd strike?
            'oKLT4': (0.0, 'Strike Looking - Out at Home'),  # dropped 3rd strike?
            'oKST1': (0.0, 'Strike Swinging - Out at 1st'),  # dropped 3rd strike?
            'oKST2': (0.0, 'Strike Swinging - Out at 2nd'),  # dropped 3rd strike?
            'oKST3': (0.0, 'Strike Swinging - Out at 3rd'),  # dropped 3rd strike?
            'oKST4': (0.0, 'Strike Swinging - Out at Home'),  # dropped 3rd strike?
            'oLO': (0.0, 'Line Out'),
            'oOBB': (0.0, 'Out of Batters Box'),
            'oOP': (0.0, 'Out on Appeal'),
            'oPO': (0.0, 'Pop Out'),
            'oROET2': (0.0, 'Reached On Error - Out at 2nd'),
            'oROET3': (0.0, 'Reached On Error - Out at 3rd'),
            'oROET4': (0.0, 'Reached On Error - Out at Home'),
            'oSB': (0.0, 'Sacrifice Bunt'),
            'oSBT2': (0.0, 'Sacrifice Bunt - Out at 2nd'),
            'oSBT3': (0.0, 'Sacrifice Bunt - Out at 3rd'),
            'oSBT4': (0.0, 'Sacrifice Bunt - Out at Home'),
            'oSF': (0.0, 'Sacrifice Fly'),
            'oSFT2': (0.0, 'Sacrifice Fly - Out at 2nd'),
            'oSFT3': (0.0, 'Sacrifice Fly - Out at 3rd'),
            'oSFT4': (0.0, 'Sacrifice Fly - Out at Home'),
            'oST2': (self.get_value_of(self.SINGLE), 'Single - Out at 2nd'),
            'oST3': (self.get_value_of(self.SINGLE), 'Single - Out at 3rd'),
            'oST4': (self.get_value_of(self.SINGLE), 'Single - Out at Home'),
            'oTT4': (self.get_value_of(self.TRIPLE), 'Triple - Out at Home'),
            'uRN': (0.0, 'Unearned Run/No RBI'),
        }

    def get_outcome_fantasy_points(self, outcome_id):
        """
        :param outcome_id: the mlb outcome id of the pbp event
        :return: a tuple of (float, str)
        """
        return self.outcomes[outcome_id]

    def get_primary_player_stats_class_for_player(self, player):
        """
        override
        """
        try:
            if player.position.get_matchname() in MlbSalaryScoreSystem.PITCHER_POSITIONS:
                # pitching PlayerStats class
                return sports.mlb.models.PlayerStatsPitcher
            else:
                # hitting PlayerStats class
                return sports.mlb.models.PlayerStatsHitter
        except:
            # print(str(player), 'instance of class:', str(type(player)))
            # print('player.position.get_matchname():', str(player.position.get_matchname()))

            raise Exception('get_primary_player_stats_class_for_player problem')

    def score_player(self, player_stats, verbose=True):
        """
        determines whether the player_stats object represents a hitter or a pitcher,
        and scores it accordingly.

        :param player_stats:
        :param verbose:
        :return:
        """
        self.set_verbose(verbose)

        if player_stats.player.position.get_matchname() in self.PITCHER_POSITIONS:
            return self.__score_pitcher(player_stats)
        else:
            return self.__score_hitter(player_stats)

    def __score_hitter(self, player_stats_hitter):
        """
        return the fantasy points accrued by this mlb PlayerStatsHitter instance
        :param player_stats_hitter:
        :return:
        """
        total = 0.0
        total += self.singles(player_stats_hitter.s)
        total += self.doubles(player_stats_hitter.d)
        total += self.triples(player_stats_hitter.t)
        total += self.home_runs(player_stats_hitter.hr)
        total += self.rbis(player_stats_hitter.rbi)
        total += self.runs(player_stats_hitter.r)
        total += self.bbs(player_stats_hitter.bb)
        total += self.ibbs(player_stats_hitter.ibb)
        total += self.hit_by_pitch(player_stats_hitter.hbp)
        total += self.stolen_bases(player_stats_hitter.sb)
        total += self.caught_stealing(player_stats_hitter.cs)
        return total

    def singles(self, value):
        if self.verbose:
            self.str_stats += '%s Sgl ' % value
        return value * self.get_value_of(self.SINGLE)

    def doubles(self, value):
        if self.verbose:
            self.str_stats += '%s Dbl ' % value
        return value * self.get_value_of(self.DOUBLE)

    def triples(self, value):
        if self.verbose:
            self.str_stats += '%s Trpl ' % value
        return value * self.get_value_of(self.TRIPLE)

    def home_runs(self, value):
        if self.verbose:
            self.str_stats += '%s HR ' % value
        return value * self.get_value_of(self.HR)

    def rbis(self, value):
        if self.verbose:
            self.str_stats += '%s RBI ' % value
        return value * self.get_value_of(self.RBI)

    def runs(self, value):
        if self.verbose:
            self.str_stats += '%s Run ' % value
        return value * self.get_value_of(self.RUN)

    def bbs(self, value):
        if self.verbose:
            self.str_stats += '%s BB ' % value
        return value * self.get_value_of(self.BB)

    def ibbs(self, value):
        if self.verbose:
            self.str_stats += '%s IBB ' % value
        return value * self.get_value_of(self.IBB)

    def hit_by_pitch(self, value):
        if self.verbose:
            self.str_stats += '%s HBP ' % value
        return value * self.get_value_of(self.HBP)

    def stolen_bases(self, value):
        if self.verbose:
            self.str_stats += '%s SB ' % value
        return value * self.get_value_of(self.SB)

    def caught_stealing(self, value):
        if self.verbose:
            self.str_stats += '%s CS ' % value
        return value * self.get_value_of(self.CS)

    def __score_pitcher(self, player_stats_pitcher):
        """
        return the fantasy points accrued by this mlb PlayerStatsPitcher instance
        :param player_stats_pitcher:
        :return:
        """
        total = 0.0
        # ip_1 is thirds of an inning
        total += self.innings_pitched(float(player_stats_pitcher.ip_1) / 3.0)
        total += self.strikeouts(player_stats_pitcher.ktotal)
        # int(True) == 1, else 0
        total += self.wins(int(player_stats_pitcher.win))
        total += self.earned_runs(player_stats_pitcher.er)
        total += self.hits_against(player_stats_pitcher.h)
        # in the context of a pitcher, 'hbp' means 'hit_batsman'
        total += self.hit_batsman(player_stats_pitcher.hbp)
        total += self.walks_against(player_stats_pitcher.bb)  # pitcher has bb property
        total += self.intentional_walks_against(player_stats_pitcher.ibb)
        total += self.complete_game(int(player_stats_pitcher.cg))
        total += self.complete_game_shutout(int(player_stats_pitcher.cgso))
        total += self.no_hitter(int(player_stats_pitcher.nono))
        return total

    def innings_pitched(self, value):
        if self.verbose: self.str_stats += '%s IP ' % value
        return value * self.get_value_of(self.IP)

    def strikeouts(self, value):
        if self.verbose: self.str_stats += '%s K ' % value
        return value * self.get_value_of(self.K)

    def wins(self, value):
        if self.verbose: self.str_stats += '%s Win ' % value
        return value * self.get_value_of(self.WIN)

    def earned_runs(self, value):
        if self.verbose: self.str_stats += '%s ER ' % value
        return value * self.get_value_of(self.ER)

    def hits_against(self, value):
        if self.verbose: self.str_stats += '%s Hit ' % value
        return value * self.get_value_of(self.HIT)

    def hit_batsman(self, value):
        if self.verbose: self.str_stats += '%s HitBatsman ' % value
        return value * self.get_value_of(self.HIT_BATSMAN)

    def walks_against(self, value):
        if self.verbose: self.str_stats += '%s Walk ' % value
        return value * self.get_value_of(self.WALK)

    def intentional_walks_against(self, value):
        if self.verbose: self.str_stats += '%s Intentional Walk ' % value
        return value * self.get_value_of(self.IWALK)

    def complete_game(self, value):
        if self.verbose: self.str_stats += '%s CG ' % value
        return value * self.get_value_of(self.CG)

    def complete_game_shutout(self, value):
        if self.verbose: self.str_stats += '%s CGSO ' % value
        return value * self.get_value_of(self.CGSO)

    def no_hitter(self, value):
        if self.verbose: self.str_stats += '%s NoHitter ' % value
        return value * self.get_value_of(self.NO_HITTER)


class NhlSalaryScoreSystem(AbstractScoreSystem):
    """
    defines the NHL Salary draft scoring metrics
    """
    THE_SPORT = 'nhl'

    GOAL = 'goal'  # goals scored
    ASSIST = 'assist'  # assists
    SOG = 'sog'  # shots on goal
    BLK = 'blk'  # blocked shot
    BLK_ATT = 'blk_att'  # shot that was blocked (ie: a blocked attempted shot)
    MS = 'ms'  # missed_shots
    SH_BONUS = 'sh-bonus'  # bonus points for goals/assists when shorthanded
    SO_GOAL = 'so-goal'  # goal in a shootout
    HAT = 'hat'  # hattrick is 3 goals scored

    WIN = 'win'  # goalie - win
    SAVE = 'save'  # goalie - shots saved
    GA = 'ga'  # goalie - goals allowed
    SHUTOUT = 'shutout'  # goalie - complete game(includes OT) no goals (doesnt count shootout goals)

    def __init__(self):
        self.score_system = ScoreSystem.objects.get(sport=self.THE_SPORT, name='salary')

        # call super last - ensures you have class variables setup
        super().__init__(self.THE_SPORT)

    def get_primary_player_stats_class_for_player(self, player):
        """
        override
        """
        return sports.nhl.models.PlayerStats

    def score_player(self, player_stats, verbose=True):
        """
        scores and returns a float for the amount of fantasy points for this PlayerStats instance

        :param player_stats:
        :return:
        """
        self.set_verbose(verbose)

        total = 0.0

        # skater stats
        total += self.goals(player_stats.goal)
        total += self.assists(player_stats.assist)
        total += self.shots_on_goal(player_stats.sog)
        total += self.blocks(player_stats.blk)
        total += self.blocked_attempts(player_stats.blk_att)
        total += self.missed_shots(player_stats.ms)  # missed shots
        total += self.short_handed_bonus(player_stats.sh_goal)
        total += self.shootout_goals(player_stats.so_goal)
        total += self.hattrick(player_stats.goal)  # goals minus shootout goals

        # goalie stats
        total += self.win(player_stats.w)
        total += self.saves(player_stats.saves)
        total += self.goals_allowed(player_stats.ga)
        total += self.shutout(player_stats.shutout)

        return total

    def goals(self, val):
        if self.verbose: self.str_stats += '%s Goal ' % val
        return val * self.get_value_of(self.GOAL)

    def assists(self, val):
        if self.verbose: self.str_stats += '%s Ast ' % val
        return val * self.get_value_of(self.ASSIST)

    def shots_on_goal(self, val):
        if self.verbose: self.str_stats += '%s SOG ' % val
        return val * self.get_value_of(self.SOG)

    def blocks(self, val):
        if self.verbose: self.str_stats += '%s Blk ' % val
        return val * self.get_value_of(self.BLK)

    def blocked_attempts(self, val):
        if self.verbose: self.str_stats += '%s BlockedAtt ' % val
        return val * self.get_value_of(self.BLK_ATT)

    def missed_shots(self, val):
        if self.verbose: self.str_stats += '%s MissShot ' % val
        return val * self.get_value_of(self.MS)

    def short_handed_bonus(self, sh_goals):
        if self.verbose: self.str_stats += '%s SHGoals ' % sh_goals
        return sh_goals * self.get_value_of(self.SH_BONUS)

    def shootout_goals(self, so_goals):
        if self.verbose: self.str_stats += '%s SOGoals ' % so_goals
        return so_goals * self.get_value_of(self.SO_GOAL)

    def hattrick(self, tot_goals):
        if self.verbose: self.str_stats += '%s HatTrk ' % '1' if tot_goals >= 3 else '0'
        return int(tot_goals >= 3) * self.get_value_of(
            self.HAT)  # ie: 0 or 1 times the value of a hattrick

    def win(self, val):
        if self.verbose: self.str_stats += '%s Win ' % val
        return int(val) * self.get_value_of(self.WIN)

    def saves(self, val):
        if self.verbose: self.str_stats += '%s Save ' % val
        return val * self.get_value_of(self.SAVE)

    def goals_allowed(self, val):
        if self.verbose: self.str_stats += '%s GA ' % val
        return val * self.get_value_of(self.GA)

    def shutout(self, val):
        if self.verbose: self.str_stats += '%s Shutout ' % val
        return int(val) * self.get_value_of(self.SHUTOUT)


class NflSalaryScoreSystem(AbstractScoreSystem):
    """
    defines the NFL Salary draft scoring metrics
    """
    THE_SPORT = 'nfl'

    PASS_TD = 'pass-td'  # thrown touchdowns
    PASS_YDS = 'pass-yds'  # pts per passing yard
    PASS_BONUS = 'pass-bonus'  # bonus for passing 300+ yards
    PASS_INT = 'pass-int'  # passed interceptions

    RUSH_YDS = 'rush-yds'  # rushing points per yard
    RUSH_TD = 'rush-td'  # rushed touchdowns
    RUSH_BONUS = 'rush-bonus'  # bonus for rushing 100+ yards

    REC_YDS = 'rec-yds'  # receiving points per yard
    REC_TD = 'rec-td'  # receiving touchdowns
    REC_BONUS = 'rec-bonus'  # bonus for receiving 100+ yards

    PPR = 'ppr'  # points per reception

    FUMBLE_LOST = 'fumble-lost'  # fumble lost (offensive player)
    TWO_PT_CONV = 'two-pt-conv'  # passed, rushed, or received succesful 2-pt conversion
    OFF_FUM_TD = 'off-fum-td'  # offensive fumble recovered for TD (unique situation)

    # -- dst scoring --
    SACK = 'sack'  # sacks
    INTS = 'ints'  # interceptions
    FUM_REC = 'fum-rec'  # fumble recoveries
    KICK_RET_TD = 'kick-ret-td'  # kickoff returned for TD
    PUNT_RET_TD = 'punt-ret-td'  # punt returned for TD
    INT_RET_TD = 'int-ret-td'  # int returned for TD
    FUM_RET_TD = 'fum-ret-td'  # fumble recovered for TD
    BLK_PUNT_RET_TD = 'blk-punt-ret-td'  # blocked punt returned for TD
    FG_RET_TD = 'fg-ret-td'  # missed FG, returned for TD
    BLK_FG_RET_TD = 'blk-fg-ret-td'

    SAFETY = 'safety'  # safeties
    BLK_KICK = 'blk-kick'  # blocked kick

    PA_0 = 'pa-0'  # 0 points allowed
    PA_6 = 'pa-6'  # 6 or less points allowed
    PA_13 = 'pa-13'  # 13 or less points allowed
    PA_20 = 'pa-20'  # 20 or less points allowed
    PA_27 = 'pa-27'  # 27 or less points allowed
    PA_34 = 'pa-34'  # 34 or less points allowed
    PA_35_PLUS = 'pa-35plus'  # 35 or MORE points allowed

    PASSING_BONUS_REQUIRED_YDS = 300
    RUSHING_BONUS_REQUIRED_YDS = 100
    RECEIVING_BONUS_REQUIRED_YDS = 100

    def __init__(self):
        self.score_system = ScoreSystem.objects.get(sport=self.THE_SPORT, name='salary')

        # call super last - ensures you have class variables setup
        super().__init__(self.THE_SPORT)

    def get_primary_player_stats_class_for_player(self, player):
        """
        override
        """
        return sports.nfl.models.PlayerStats

    def score_player(self, player_stats, opp_score=0, verbose=True):
        """
        scores and returns a float for the amount of fantasy points for this PlayerStats instance

        :param player_stats:
        :return:
        """

        self.set_verbose(verbose)

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
        total += self.receiving_bonus(
            int(player_stats.rec_yds >= self.RECEIVING_BONUS_REQUIRED_YDS))
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
        total += self.blocked_field_goal_return_tds(player_stats.ret_blk_fg_td)

        pos = player_stats.position
        if pos.get_matchname() == 'DST':
            dst_pa = self.get_dst_points_allowed(player_stats, opp_score)
            total += self.get_dst_pa_bracket_points(dst_pa)

        return total

    def get_str_stats(self):
        return self.str_stats

    # offensive scoring methods below:
    def passing_yds(self, val):
        if self.verbose: self.str_stats += '%s PassYds ' % val
        return val * self.get_value_of(self.PASS_YDS)

    def passing_tds(self, val):
        if self.verbose: self.str_stats += '%s PassTd ' % val
        return val * self.get_value_of(self.PASS_TD)

    def passing_bonus(self, val):
        if self.verbose: self.str_stats += '%s PassBns ' % val
        return val * self.get_value_of(self.PASS_BONUS)

    def passing_interceptions(self, val):
        if self.verbose: self.str_stats += '%s PassINT ' % val
        return val * self.get_value_of(self.PASS_INT)

    def rushing_yds(self, val):
        if self.verbose: self.str_stats += '%s RushYds ' % val
        return val * self.get_value_of(self.RUSH_YDS)

    def rushing_tds(self, val):
        if self.verbose: self.str_stats += '%s RushTd ' % val
        return val * self.get_value_of(self.RUSH_TD)

    def rushing_bonus(self, val):
        if self.verbose: self.str_stats += '%s RushBns ' % val
        return val * self.get_value_of(self.RUSH_BONUS)

    def receiving_yds(self, val):
        if self.verbose: self.str_stats += '%s RecYds ' % val
        return val * self.get_value_of(self.REC_YDS)

    def receiving_tds(self, val):
        if self.verbose: self.str_stats += '%s RecTd ' % val
        return val * self.get_value_of(self.REC_TD)

    def receiving_bonus(self, val):
        if self.verbose: self.str_stats += '%s RecBns ' % val
        return val * self.get_value_of(self.REC_BONUS)

    def ppr(self, val):
        if self.verbose: self.str_stats += '%s Recs ' % val
        return val * self.get_value_of(self.PPR)

    def fumble_lost(self, val):
        if self.verbose: self.str_stats += '%s FumLost ' % val
        return val * self.get_value_of(self.FUMBLE_LOST)

    def two_pt_conversion(self, val):
        if self.verbose: self.str_stats += '%s 2PtConv ' % val
        return val * self.get_value_of(self.TWO_PT_CONV)

    def offensive_fumble_td(self, val):
        if self.verbose: self.str_stats += '%s OffFumTd ' % val
        return val * self.get_value_of(self.OFF_FUM_TD)

    # defensive scoring methods below:
    def sacks(self, val):
        if self.verbose: self.str_stats += '%s Sck ' % val
        return val * self.get_value_of(self.SACK)

    def interceptions(self, val):
        if self.verbose: self.str_stats += '%s Int ' % val
        return val * self.get_value_of(self.INTS)

    def fumble_recoveries(self, val):
        if self.verbose: self.str_stats += '%s FumRec ' % val
        return val * self.get_value_of(self.FUM_REC)

    # types of return touchdowns
    def kick_return_tds(self, val):
        if self.verbose: self.str_stats += '%s KckRetTd ' % val
        return val * self.get_value_of(self.KICK_RET_TD)

    def punt_return_tds(self, val):
        if self.verbose: self.str_stats += '%s PntRetTd ' % val
        return val * self.get_value_of(self.PUNT_RET_TD)

    def interception_return_tds(self, val):
        if self.verbose: self.str_stats += '%s IntRetTd ' % val
        return val * self.get_value_of(self.INT_RET_TD)

    def fumble_return_tds(self, val):
        if self.verbose: self.str_stats += '%s FumRetTd ' % val
        return val * self.get_value_of(self.FUM_RET_TD)

    def blocked_punt_return_tds(self, val):
        if self.verbose: self.str_stats += '%s BlkPntTd ' % val
        return val * self.get_value_of(self.BLK_PUNT_RET_TD)

    def field_goal_return_tds(self, val):
        if self.verbose: self.str_stats += '%s FgRetTd ' % val
        return val * self.get_value_of(self.FG_RET_TD)

    def blocked_field_goal_return_tds(self, val):
        if self.verbose: self.str_stats += '%s BlkFgRetTd ' % val
        return val * self.get_value_of(self.BLK_FG_RET_TD)

    # misc dst
    def safeties(self, val):  # safety
        if self.verbose: self.str_stats += '%s Sfty ' % val
        return val * self.get_value_of(self.SAFETY)

    def blocked_kicks(self, val):  # blocked kick (punts, fgs)
        if self.verbose: self.str_stats += '%s BlkKick ' % val
        return val * self.get_value_of(self.BLK_KICK)

    def get_dst_points_allowed(self, player_stats, opp_score):  # dst points allowed
        """
        DST fantasy scoring is based on the "points the DST has allowed".
        This does not include points the teams Offense has allowed!
        We disregard 6 points for interceptions and fumbles returned for TDs,
        as well as 2 points for safeties against the offense for which the DST plays.

        :param player_stats:
        :return:
        """
        dst_points_allowed = opp_score
        dst_points_allowed -= 6 * player_stats.int_td_against
        dst_points_allowed -= 6 * player_stats.fum_td_against
        dst_points_allowed -= 2 * player_stats.off_pass_sfty
        dst_points_allowed -= 2 * player_stats.off_rush_sfty
        dst_points_allowed -= 2 * player_stats.off_punt_sfty
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
        fantasy_pts = 0
        if dst_pa <= 0:
            fantasy_pts = self.get_value_of(self.PA_0)  # 0 points allowed bracket
        elif dst_pa <= 6:
            fantasy_pts = self.get_value_of(self.PA_6)
        elif dst_pa <= 13:
            fantasy_pts = self.get_value_of(self.PA_13)
        elif dst_pa <= 20:
            fantasy_pts = self.get_value_of(self.PA_20)
        elif dst_pa <= 27:
            fantasy_pts = self.get_value_of(self.PA_27)
        elif dst_pa <= 34:
            fantasy_pts = self.get_value_of(self.PA_34)
        else:
            fantasy_pts = self.get_value_of(self.PA_35_PLUS)

        if self.verbose: self.str_stats += '%s DstPts ' % fantasy_pts

        return fantasy_pts
