from django.db import models
import sports.models
import scoring.classes
import push.classes
from sports.tasks import countdown_send_player_stats_data, COUNTDOWN


class Season(sports.models.Season):
    """

    """

    class Meta:
        abstract = False


class Team(sports.models.Team):
    # db.team.findOne({'parent_api__id':'hierarchy'})
    # {
    #     "_id" : "cGFyZW50X2FwaV9faWRoaWVyYXJjaHlsZWFndWVfX2lkNDM1MzEzOGQtNGMyMi00Mzk2LTk1ZDgtNWY1ODdkMmRmMjVjY
    #               29uZmVyZW5jZV9faWQzOTYwY2ZhYy03MzYxLTRiMzAtYmMyNS04ZDM5M2RlNmY2MmZkaXZpc2lvbl9faWQ1NGRjNzM0O
    #               C1jMWQyLTQwZDgtODhiMy1jNGMwMTM4ZTA4NWRpZDU4M2VjZWE2LWZiNDYtMTFlMS04MmNiLWY0Y2U0Njg0ZWE0Yw==",
    #     "alias" : "MIA",
    #     "id" : "583ecea6-fb46-11e1-82cb-f4ce4684ea4c",
    #     "market" : "Miami",
    #     "name" : "Heat",
    #     "parent_api__id" : "hierarchy",
    #     "dd_updated__id" : NumberLong("1431472829579"),
    #     "league__id" : "4353138d-4c22-4396-95d8-5f587d2df25c",
    #     "conference__id" : "3960cfac-7361-4b30-bc25-8d393de6f62f",
    #     "division__id" : "54dc7348-c1d2-40d8-88b3-c4c0138e085d",
    #     "venue" : "b67d5f09-28b2-5bc6-9097-af312007d2f4"
    # }

    srid_league = models.CharField(max_length=64, null=False,
                                   help_text='league sportsradar id')
    srid_conference = models.CharField(max_length=64, null=False,
                                       help_text='conference sportsradar id')
    srid_division = models.CharField(max_length=64, null=False,
                                     help_text='division sportsradar id')
    market = models.CharField(max_length=64)

    class Meta:
        abstract = False


class Game(sports.models.Game):
    """
    all we get from the inherited model is: 'start' and 'status'
    """

    season = models.ForeignKey(Season, null=False)

    home = models.ForeignKey(Team, null=False, related_name='game_hometeam')
    srid_home = models.CharField(max_length=64, null=False,
                                 help_text='home team sportsradar global id')

    away = models.ForeignKey(Team, null=False, related_name='game_awayteam')
    srid_away = models.CharField(max_length=64, null=False,
                                 help_text='away team sportsradar global id')
    title = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        abstract = False


class GameBoxscore(sports.models.GameBoxscore):
    # srid_home   = models.CharField(max_length=64, null=False)
    # home        = models.ForeignKey(Team, null=False, related_name='gameboxscore_home')
    # away        = models.ForeignKey(Team, null=False, related_name='gameboxscore_away')
    # srid_away   = models.CharField(max_length=64, null=False)
    #
    # attendance  = models.IntegerField(default=0, null=False)
    clock = models.CharField(max_length=16, null=False, default='')
    # coverage    = models.CharField(max_length=16, null=False, default='')
    duration = models.CharField(max_length=16, null=False, default='')
    lead_changes = models.IntegerField(default=0, null=False)
    quarter = models.CharField(max_length=16, null=False, default='')
    # status      = models.CharField(max_length=64, null=False, default='')
    times_tied = models.IntegerField(default=0, null=False)

    class Meta:
        abstract = False


class Player(sports.models.Player):
    """
    inherited: 'srid', 'first_name', 'last_name'
    """
    team = models.ForeignKey(Team, null=False)
    srid_team = models.CharField(max_length=64, null=False, blank=True, default='')
    birth_place = models.CharField(max_length=64, null=False, blank=True, default='')
    birthdate = models.CharField(max_length=64, null=False, blank=True, default='')
    college = models.CharField(max_length=64, null=False, blank=True, default='')
    experience = models.FloatField(default=0.0, null=False, blank=True)
    height = models.FloatField(default=0.0, null=False, blank=True, help_text='inches')
    weight = models.FloatField(default=0.0, null=False, blank=True, help_text='lbs')
    jersey_number = models.CharField(max_length=64, null=False, blank=True, default='')

    # primary_position = models.CharField(max_length=64, null=False, default='')

    status = models.CharField(
        max_length=64,
        null=False,
        default='',
        blank=True,
        help_text=('roster status - ie: "ACT" means they are ON the roster. Not particularly active as in not-injured!')
    )

    draft_pick = models.CharField(max_length=64, null=False, blank=True, default='')
    draft_round = models.CharField(max_length=64, null=False, blank=True, default='')
    draft_year = models.CharField(max_length=64, null=False, blank=True, default='')
    srid_draft_team = models.CharField(max_length=64, null=False, blank=True, default='')

    class Meta:
        abstract = False
        verbose_name = "NBA Player"


class PlayerLineupName(Player):
    class Meta:
        proxy = True


class PlayerStats(sports.models.PlayerStats):
    """
    Model for all of a players statistics in a unique game.
    """

    # must override parent SCORING_FIELDS
    SCORING_FIELDS = [
        'points',
        'three_points_made',
        'rebounds',
        'assists',
        'steals',
        'blocks',
        'turnovers',
        'minutes',
    ]

    #   { 'defensive_rebounds': 1.0,
    defensive_rebounds = models.FloatField(null=False, default=0.0)
    #         'two_points_pct': 0.6,
    two_points_pct = models.FloatField(null=False, default=0.0)
    #         'assists': 0.0,
    assists = models.FloatField(null=False, default=0.0)
    #         'free_throws_att': 2.0,
    free_throws_att = models.FloatField(null=False, default=0.0)
    #         'flagrant_fouls': 0.0,
    flagrant_fouls = models.FloatField(null=False, default=0.0)
    #         'offensive_rebounds': 1.0,
    offensive_rebounds = models.FloatField(null=False, default=0.0)
    #         'personal_fouls': 0.0,
    personal_fouls = models.FloatField(null=False, default=0.0)
    #         'field_goals_att': 5.0,
    field_goals_att = models.FloatField(null=False, default=0.0)
    #         'three_points_att': 0.0,
    three_points_att = models.FloatField(null=False, default=0.0)
    #         'field_goals_pct': 60.0,
    field_goals_pct = models.FloatField(null=False, default=0.0)
    #         'turnovers': 0.0,
    turnovers = models.FloatField(null=False, default=0.0)
    #         'points': 8.0,
    points = models.FloatField(null=False, default=0.0)
    #         'rebounds': 2.0,
    rebounds = models.FloatField(null=False, default=0.0)
    #         'two_points_att': 5.0,
    two_points_att = models.FloatField(null=False, default=0.0)
    #         'field_goals_made': 3.0,
    field_goals_made = models.FloatField(null=False, default=0.0)
    #         'blocked_att': 0.0,
    blocked_att = models.FloatField(null=False, default=0.0)
    #         'free_throws_made': 2.0,
    free_throws_made = models.FloatField(null=False, default=0.0)
    #         'blocks': 0.0,
    blocks = models.FloatField(null=False, default=0.0)
    #         'assists_turnover_ratio': 0.0,
    assists_turnover_ratio = models.FloatField(null=False, default=0.0)
    #         'tech_fouls': 0.0,
    tech_fouls = models.FloatField(null=False, default=0.0)
    #         'three_points_made': 0.0,
    three_points_made = models.FloatField(null=False, default=0.0)
    #         'steals': 0.0,
    steals = models.FloatField(null=False, default=0.0)
    #         'two_points_made': 3.0,
    two_points_made = models.FloatField(null=False, default=0.0)
    #         'free_throws_pct': 100.0,
    free_throws_pct = models.FloatField(null=False, default=0.0)
    #         'three_points_pct': 0.0
    three_points_pct = models.FloatField(null=False, default=0.0)

    # the minutes is originally a string like "20:13" -- 20 minutes, 13 seconds
    # which we parse, and truncate to get just the minutes
    minutes = models.FloatField(null=False, default=0.0)

    class Meta:
        abstract = False
        unique_together = ('srid_player', 'srid_game')

    def save(self, *args, **kwargs):
        # perform score update
        scorer = scoring.classes.NbaSalaryScoreSystem()
        self.fantasy_points = scorer.score_player(self)

        #
        # send the pusher obj for fantasy points with scoring
        if kwargs.get('bulk', False):
            # print('bulk = True skip player stats monkey business')
            pass
        else:
            args = (self.get_cache_token(), push.classes.PUSHER_NBA_STATS, 'player', self.to_json())
            self.set_cache_token()
            countdown_send_player_stats_data.apply_async(args, countdown=COUNTDOWN)

        super().save(*args, **kwargs)


class PlayerStatsSeason(sports.models.PlayerStatsSeason):
    class Meta:
        abstract = True  # TODO


class Injury(sports.models.Injury):
    #
    # nba injuries have ids
    srid = models.CharField(max_length=64, null=False, default='')
    comment = models.CharField(max_length=1024, null=False, default='')

    class Meta:
        abstract = False


class RosterPlayer(sports.models.RosterPlayer):
    class Meta:
        abstract = True  # TODO


class Venue(sports.models.Venue):
    class Meta:
        abstract = True  # TODO


class GamePortion(sports.models.GamePortion):
    #
    # this is the srid or the period or quarter
    srid = models.CharField(max_length=64, null=False, default='')

    class Meta:
        abstract = False


class PbpDescription(sports.models.PbpDescription):
    #
    # this is the srid of the event, aka specific pbp object
    srid = models.CharField(max_length=64, null=False, default='', unique=True)

    class Meta:
        abstract = False


class Pbp(sports.models.Pbp):
    class Meta:
        abstract = False


class TsxNews(sports.models.TsxNews):
    """
    inherits from sports.models.TsxXXX of the same name
    """

    # tsxplayers = GenericRelation('nba.TsxPlayer')

    class Meta:
        abstract = False


class TsxInjury(sports.models.TsxInjury):
    """
    inherits from sports.models.TsxXXX of the same name
    """

    # tsxplayers = GenericRelation('nba.TsxPlayer')

    class Meta:
        abstract = False


class TsxTransaction(sports.models.TsxTransaction):
    """
    inherits from sports.models.TsxXXX of the same name
    """

    # tsxplayers = GenericRelation('nba.TsxPlayer')

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
