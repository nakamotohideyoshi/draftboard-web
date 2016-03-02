#
# sports/mlb/models.py

from django.db import models
import sports.models
import scoring.classes
import push.classes
from django.conf import settings

class Season( sports.models.Season ):
    class Meta:
        abstract = False

class Team( sports.models.Team ):
    # db.team.findOne({'parent_api__id':'hierarchy'})
    # {
    #     "_id" : "cGFyZW50X2FwaV9faWRoaWVyYXJjaHlsZWFndWVfX2lkMmVhNmVmZTctMmUyMS00ZjI5LTgwYTItMGEyNGFkMWY1Zjg1ZGl2aXNpb25fX2lkMWQ3NGU4ZTktN2ZhZi00Y2RiLWI2MTMtMzk0NGZhNWFhNzM5aWQxZDY3ODQ0MC1iNGIxLTQ5NTQtOWIzOS03MGFmYjNlYmJjZmE=",
    #     "abbr" : "TOR",
    #     "id" : "1d678440-b4b1-4954-9b39-70afb3ebbcfa",
    #     "market" : "Toronto",
    #     "name" : "Blue Jays",
    #     "parent_api__id" : "hierarchy",
    #     "dd_updated__id" : NumberLong("1431469575341"),
    #     "league__id" : "2ea6efe7-2e21-4f29-80a2-0a24ad1f5f85",
    #     "division__id" : "1d74e8e9-7faf-4cdb-b613-3944fa5aa739",
    #     "venue" : "84d72338-2173-4a90-9d25-99adc6c86f4b"
    # }

    srid_league     = models.CharField(max_length=64, null=False,
                            help_text='league sportsradar id')
    srid_division   = models.CharField(max_length=64, null=False,
                            help_text='division sportsradar id')
    market          = models.CharField(max_length=64)

    class Meta:
        abstract = False

class Game( sports.models.Game ):
    """
    all we get from the inherited model is: 'start' and 'status'
    """

    season      = models.ForeignKey(Season, null=False)

    home = models.ForeignKey( Team, null=False, related_name='game_hometeam')
    srid_home   = models.CharField(max_length=64, null=False,
                                help_text='home team sportsradar global id')

    away = models.ForeignKey( Team, null=False, related_name='game_awayteam')
    srid_away   = models.CharField(max_length=64, null=False,
                                help_text='away team sportsradar global id')
    title       = models.CharField(max_length=128, null=True)

    attendance = models.IntegerField(default=0, null=False)
    day_night   = models.CharField(max_length=8, null=False, default='')
    game_number = models.IntegerField(default=0, null=False)

    class Meta:
        abstract = False


class GameBoxscore( sports.models.GameBoxscore ):

    day_night       = models.CharField(max_length=8, null=False, default='')
    game_number     = models.IntegerField(default=1, null=False)
    inning          = models.CharField(max_length=16, null=False, default='')
    inning_half     = models.CharField(max_length=16, null=False, default='')

    srid_home_pp = models.CharField(max_length=64, null=True,
                                help_text='srid of the HOME probable pitcher set before the game starts')
    srid_home_sp = models.CharField(max_length=64, null=True,
                                help_text='srid of the HOME starting pitcher')
    srid_away_pp = models.CharField(max_length=64, null=True,
                                help_text='srid of the AWAY probable pitcher set before the game starts')
    srid_away_sp = models.CharField(max_length=64, null=True,
                                help_text='srid of the AWAY starting pitcher')
    srid_win        = models.CharField(max_length=64, null=True,
                                help_text='')
    srid_loss       = models.CharField(max_length=64, null=True,
                                help_text='')
    # srid_hold       = models.CharField(max_length=64, null=True,
    #                             help_text='')
    #srid_save       = models.CharField(max_length=64, null=True,
    #                            help_text='')
    #srid_blown_save  = models.CharField(max_length=64, null=True,
    #                            help_text='')

    #
    home_errors     = models.IntegerField(default=0, null=False)
    home_hits       = models.IntegerField(default=0, null=False)
    #
    away_errors     = models.IntegerField(default=0, null=False)
    away_hits       = models.IntegerField(default=0, null=False)

    class Meta:
        abstract = False


class Player( sports.models.Player ):
    """
    inherited: 'srid', 'first_name', 'last_name'
    """
    team        = models.ForeignKey(Team, null=False)
    srid_team   = models.CharField(max_length=64, null=False, default='')

    preferred_name = models.CharField(max_length=64, null=False, default='')

    birthcity = models.CharField(max_length=64, null=False, default='')
    birthcountry = models.CharField(max_length=64, null=False, default='')
    birthdate   = models.CharField(max_length=64, null=False, default='')

    height      = models.FloatField(default=0.0, null=False, help_text='inches')
    weight      = models.FloatField(default=0.0, null=False, help_text='lbs')
    jersey_number = models.CharField(max_length=64, null=False, default='')

    #primary_position = models.CharField(max_length=64, null=False, default='')

    status = models.CharField(max_length=64, null=False, default='',
                help_text='roster status - ie: "A" means they are ON the roster. Not particularly active as in not-injured!')

    pro_debut = models.CharField(max_length=64, null=False, default='')
    throw_hand = models.CharField(max_length=8, null=False, default='')
    bat_hand = models.CharField(max_length=8, null=False, default='')

    class Meta:
        abstract = False

class PlayerLineupName( Player ):

    class Meta:
        proxy = True

class PlayerStats( sports.models.PlayerStats ):

    # player  = models.ForeignKey(Player, null=False)
    # game    = models.ForeignKey(Game, null=False)

    play    = models.BooleanField(default=False, null=False) # indicates they PLAYED in the game
    start   = models.BooleanField(default=False, null=False) # indicates they STARTED the game

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # perform score update
        scorer = scoring.classes.MlbSalaryScoreSystem()
        self.fantasy_points = scorer.score_player( self )

        #
        # send the pusher obj for fantasy points with scoring
        self.set_cache_token()
        push.classes.DataDenPush( push.classes.PUSHER_MLB_STATS, 'player').send( self.to_json(), async=settings.DATADEN_ASYNC_UPDATES )

        super().save(*args, **kwargs)

class PlayerStatsHitter(PlayerStats):

    SCORING_FIELDS = [
        's',
        'd',
        't',
        'hr',
        'rbi',
        'r',
        'bb',
        'hbp',
        'sb',
        'cs',
    ]

    bb  = models.IntegerField(default=0, null=False) # walks
    s   = models.IntegerField(default=0, null=False) # singles
    d   = models.IntegerField(default=0, null=False) # doubles
    t   = models.IntegerField(default=0, null=False) # triples
    hr  = models.IntegerField(default=0, null=False) # home runs!
    rbi = models.IntegerField(default=0, null=False) # runs batted in
    r   = models.IntegerField(default=0, null=False) # runs
    hbp = models.IntegerField(default=0, null=False) # hit by pitch
    sb  = models.IntegerField(default=0, null=False) # stolen bases
    cs  = models.IntegerField(default=0, null=False) # caught stealing

    ktotal  = models.IntegerField(default=0, null=False) # total strikeouts

    ab  = models.IntegerField(default=0, null=False) # at-bats
    ap  = models.IntegerField(default=0, null=False) # appearances
    lob = models.IntegerField(default=0, null=False) # left on base
    xbh = models.IntegerField(default=0, null=False) # extra base hits

class PlayerStatsPitcher(PlayerStats):

    SCORING_FIELDS = [
        'ip_1',
        'ktotal',
        'win',
        'er',
        'h',
        'bb',
        'cg',
        'cgso',
        'nono',
    ]

    ip_1    = models.FloatField(default=0.0, null=False) # outs, basically
    ip_2    = models.FloatField(default=0.0, null=False) # 1 == one inning pitched
    ktotal  = models.IntegerField(default=0, null=False)
    win     = models.BooleanField(default=False, null=False)
    loss    = models.BooleanField(default=False, null=False)
    qstart  = models.BooleanField(default=False, null=False)
    er      = models.IntegerField(default=0, null=False) # earned runs allowed
    r_total = models.IntegerField(default=0, null=False) # total runs allowed
    h       = models.IntegerField(default=0, null=False) # hits against
    bb      = models.IntegerField(default=0, null=False) # walks against
    hbp     = models.IntegerField(default=0, null=False) # hit batsmen
    cg      = models.BooleanField(default=False, null=False) # complete game
    cgso    = models.BooleanField(default=False, null=False) # complete game shut out
    nono    = models.BooleanField(default=False, null=False) # no hitter (cg and no hits)

class PlayerStatsSeason( sports.models.PlayerStatsSeason ):
    class Meta:
        abstract = True # TODO

class Injury( sports.models.Injury ):
    class Meta:
        abstract = False

class RosterPlayer( sports.models.RosterPlayer ):
    class Meta:
        abstract = True # TODO

class Venue( sports.models.Venue ):
    class Meta:
        abstract = True # TODO

class GamePortion(sports.models.GamePortion):
    class Meta:
        abstract = False

class PbpDescription(sports.models.PbpDescription):
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
