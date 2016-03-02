#
# sports/nhl/models.py

from django.db import models
import sports.models
import scoring.classes
import push.classes
from django.conf import settings

# Any classes that still have the abtract = True, just havent been migrated/implemented yet!

class Season( sports.models.Season ):
    class Meta:
        abstract = False

class Team( sports.models.Team ):

    srid_league   = models.CharField(max_length=64, null=False,
                            help_text='league sportsradar id')
    srid_conference   = models.CharField(max_length=64, null=False,
                            help_text='conference sportsradar id')
    srid_division   = models.CharField(max_length=64, null=False,
                            help_text='division sportsradar id')
    market      = models.CharField(max_length=64)

    class Meta:
        abstract = False

class Game( sports.models.Game ):
    """
    all we get from the inherited model is: 'srid', 'start' and 'status'
    """
    home = models.ForeignKey( Team, null=False, related_name='game_hometeam')
    srid_home   = models.CharField(max_length=64, null=False,
                                help_text='home team sportsradar global id')

    away = models.ForeignKey( Team, null=False, related_name='game_awayteam')
    srid_away   = models.CharField(max_length=64, null=False,
                                help_text='away team sportsradar global id')
    title       = models.CharField(max_length=128, null=True)

    class Meta:
        abstract = False

class GameBoxscore( sports.models.GameBoxscore ):

    clock       = models.CharField(max_length=16, null=False, default='')
    period     = models.CharField(max_length=16, null=False, default='')

    class Meta:
        abstract = False

class Player( sports.models.Player ):
    """
    inherited: 'srid', 'first_name', 'last_name'
    """
    team        = models.ForeignKey(Team, null=False)
    srid_team = models.CharField(max_length=64, null=False, default='')
    birth_place = models.CharField(max_length=64, null=False, default='')
    birthdate   = models.CharField(max_length=64, null=False, default='')
    college     = models.CharField(max_length=64, null=False, default='')
    experience  = models.FloatField(default=0.0, null=False)
    height      = models.FloatField(default=0.0, null=False, help_text='inches')
    weight      = models.FloatField(default=0.0, null=False, help_text='lbs')
    jersey_number = models.CharField(max_length=64, null=False, default='')

    #primary_position = models.CharField(max_length=64, null=False, default='')

    status = models.CharField(max_length=64, null=False, default='',
                help_text='roster status - ie: "ACT" means they are ON the roster. Not particularly active as in not-injured!')

    draft_pick = models.CharField(max_length=64, null=False, default='')
    draft_round = models.CharField(max_length=64, null=False, default='')
    draft_year = models.CharField(max_length=64, null=False, default='')
    srid_draft_team = models.CharField(max_length=64, null=False, default='')

    class Meta:
        abstract = False

class PlayerStats( sports.models.PlayerStats ):

    # must override parent SCORING_FIELDS
    SCORING_FIELDS = [
        # skater stats
        'goal',
        'assist',
        'sog',
        'blk',
        'sh_goal',
        'so_goal',

        # goalie stats
        #'w',
        'saves',
        'ga',
        #'shutout',
    ]

    SCORING_FIELDS_DONT_AVG = [
        'w',
        'shutout',
    ]

    # player  = models.ForeignKey(Player, null=False)
    # game    = models.ForeignKey(Game, null=False)

    # skater stats
    goal    = models.IntegerField(default=0, null=False)
    assist  = models.IntegerField(default=0, null=False)
    sog     = models.IntegerField(default=0, null=False)
    blk     = models.IntegerField(default=0, null=False)
    sh_goal = models.IntegerField(default=0, null=False)        # short-handed goal
    pp_goal = models.IntegerField(default=0, null=False)        # power play goal
    so_goal  = models.IntegerField(default=0, null=False)       # shootout goal

    # goalie stats    ... [ "win", "loss", "overtime_loss", "none" ] are the "credit" types for goalies
    w       = models.BooleanField(default=False, null=False)
    l       = models.BooleanField(default=False, null=False)
    otl     = models.BooleanField(default=False, null=False)
    saves   = models.IntegerField(default=0, null=False)        # dont name it 'save' ! django would hate that
    ga      = models.IntegerField(default=0, null=False)        # goals allowed
    shutout = models.BooleanField(default=False, null=False)    # shutout - complete game, and no goals allowed

    class Meta:
        abstract = False

    def save(self, *args, **kwargs):
        # perform score update
        scorer = scoring.classes.NhlSalaryScoreSystem()
        self.fantasy_points = scorer.score_player( self )

        #
        # pusher the fantasy points w/ stats
        push.classes.DataDenPush( push.classes.PUSHER_NHL_STATS, 'player').send( self.to_json(), async=settings.DATADEN_ASYNC_UPDATES )

        super().save(*args, **kwargs)

class PlayerStatsSeason( sports.models.PlayerStatsSeason ):
    class Meta:
        abstract = True # TODO

class Injury( sports.models.Injury ):
    #
    # nba injuries have ids
    srid = models.CharField(max_length=64, null=False, default='')
    comment = models.CharField(max_length=1024, null=False, default='')

    class Meta:
        abstract = False

class RosterPlayer( sports.models.RosterPlayer ):
    class Meta:
        abstract = True # TODO

class Venue( sports.models.Venue ):
    class Meta:
        abstract = True # TODO

class GamePortion(sports.models.GamePortion):
    #
    # this is the srid or the period or quarter
    srid = models.CharField(max_length=64, null=False, default='')

    class Meta:
        abstract = False

class PbpDescription(sports.models.PbpDescription):
    #
    # this is the srid of the event, aka specific pbp object
    srid = models.CharField(max_length=64, null=False, default='')

    class Meta:
        abstract = False

class Pbp(sports.models.Pbp):
    class Meta:
        abstract = False

class TsxNews(sports.models.TsxNews):
    """
    inherits from sports.models.TsxXXX of the same name
    """

    class Meta:
        abstract = False

class TsxInjury(sports.models.TsxInjury):
    """
    inherits from sports.models.TsxXXX of the same name
    """

    class Meta:
        abstract = False

class TsxTransaction(sports.models.TsxTransaction):
    """
    inherits from sports.models.TsxXXX of the same name
    """

    class Meta:
        abstract = False

class TsxTeam(sports.models.TsxTeam):
    """
    inherits from sports.models.TsxXXX of the same name
    """

    team = models.ForeignKey(Team, null=False)

    class Meta:
        abstract = False

class TsxPlayer(sports.models.TsxPlayer):
    """
    inherits from sports.models.TsxXXX of the same name
    """

    player = models.ForeignKey(Player, null=False)

    class Meta:
        abstract = False