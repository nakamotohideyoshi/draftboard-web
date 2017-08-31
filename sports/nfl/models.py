from logging import getLogger

import django.core.exceptions
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save

import push.classes
import scoring.classes
import sports.models

logger = getLogger('sports.nfl.models')

DST_PLAYER_LAST_NAME = 'DST'  # dst Player objects last_name
DST_POSITION = 'DST'  # dont change this


class Season(sports.models.Season):
    class Meta:
        abstract = False


class Team(sports.models.Team):
    """

    !!!!
    NOTE: there is a special signal hooked up to the post_save of
            this model. that signal creates the "dst player" that
            is related to this team. (we dont get DST's by default!)


    """

    # db.team.findOne({'parent_api__id':'hierarchy'})
    # {
    #     "_id" : "cGFyZW50X2FwaV9faWRoaWVyYXJjaHlsZWFndWVfX2lkNDM1MzEzOGQtNGMyMi00Mzk2LTk1ZDgtNWY1ODdkMmRmMjVjY29uZmVy
    #           ZW5jZV9faWQzOTYwY2ZhYy03MzYxLTRiMzAtYmMyNS04ZDM5M2RlNmY2MmZkaXZpc2lvbl9faWQ1NGRjNzM0OC1jMWQyLTQwZDgtODh
    #            iMy1jNGMwMTM4ZTA4NWRpZDU4M2VjZWE2LWZiNDYtMTFlMS04MmNiLWY0Y2U0Njg0ZWE0Yw==",
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

    weather_json = models.CharField(max_length=512, null=False, blank=True)

    class Meta:
        abstract = False

    def save(self, *args, **kwargs):
        from .classes import NflRecentGamePlayerStats

        """
        override save so we can signal certain changes
        to this object after the "real" save()
        """

        # cache the changed fields before save() called because it will reset them
        try:
            changed_fields = self.get_dirty_fields()
        except django.core.exceptions.ValidationError:
            changed_fields = {}

        # If the game was just changed to 'closed', sync all player stats from our Dataden
        # MongoDB objects.
        # (NOTE: This is only for NFL games - others sports shouldn't need this)
        # See: https://github.com/runitoncedevs/dfs/wiki/Syncing-our-local-player-stats-with-
        # what-is-in-MongoDB

        # `status` field was changed, and now it is 'closed'.
        if changed_fields.get('status', False) and self.status == self.STATUS_CLOSED:
            logger.info(
                'NFL game has been completed, kicking off final stat sync. game: %s' % self.srid)
            nfl_recent_stats = NflRecentGamePlayerStats()
            nfl_recent_stats.update(self.srid)

        # Call the "real" save() method.
        super().save(*args, **kwargs)


class GameBoxscore(sports.models.GameBoxscore):
    clock = models.CharField(max_length=16, null=False, default='')
    completed = models.CharField(max_length=64, null=False, default='')
    quarter = models.CharField(max_length=16, null=False, default='')

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

    # A01 – Active
    # NWT – Not with team
    # P01 – Practice squad
    status = models.CharField(
        max_length=64,
        null=False,
        default='',
        blank=True,
        help_text='roster status - ie: "A01" means they are ON the roster. Not particularly active as in not-injured!'
    )
    draft_pick = models.CharField(max_length=64, null=False, blank=True, default='')
    draft_round = models.CharField(max_length=64, null=False, blank=True, default='')
    draft_year = models.CharField(max_length=64, null=False, blank=True, default='')
    srid_draft_team = models.CharField(max_length=64, null=False, blank=True, default='')

    class Meta:
        abstract = False
        ordering = ('first_name',)
        verbose_name = "NFL Player"


class PlayerLineupName(Player):
    class Meta:
        proxy = True


class PlayerStats(sports.models.PlayerStats):
    # must override parent SCORING_FIELDS
    SCORING_FIELDS = [
        'pass_td',
        'pass_yds',
        'pass_int',

        'rush_td',
        'rush_yds',

        'rec_td',
        'rec_yds',
        'rec_rec',

        'off_fum_lost',
        'two_pt_conv',
        'off_fum_rec_td',

        #
        # dst scoring below are valid,
        # but you may wish to split
        # off the DST historical scoring into
        # something separate...

        'sack',
        'ints',
        'fum_rec',
        'sfty',
        'blk_kick',

        'ret_kick_td',
        'ret_punt_td',
        'ret_int_td',
        'ret_fum_td',
        'ret_blk_punt_td',
        'ret_fg_td',
        'ret_blk_fg_td',
    ]

    # player  = models.ForeignKey(Player, null=False)
    # game    = models.ForeignKey(Game, null=False)

    # passing
    pass_td = models.IntegerField(default=0, null=False)
    pass_yds = models.IntegerField(default=0, null=False)
    pass_int = models.IntegerField(default=0, null=False)

    # rushing
    rush_td = models.IntegerField(default=0, null=False)
    rush_yds = models.IntegerField(default=0, null=False)

    # receiving
    rec_td = models.IntegerField(default=0, null=False)
    rec_yds = models.IntegerField(default=0, null=False)
    rec_rec = models.IntegerField(default=0, null=False)

    # (offensive) fumbles lost
    off_fum_lost = models.IntegerField(default=0, null=False)
    # (offensive) fum recovery for td
    off_fum_rec_td = models.IntegerField(default=0, null=False)

    # 2 point conversion
    two_pt_conv = models.IntegerField(default=0, null=False)

    #
    # defensive stats:
    sack = models.IntegerField(default=0, null=False)
    ints = models.IntegerField(default=0, null=False)
    fum_rec = models.IntegerField(default=0, null=False)

    # return tds
    ret_kick_td = models.IntegerField(default=0, null=False)
    ret_punt_td = models.IntegerField(default=0, null=False)
    ret_int_td = models.IntegerField(default=0, null=False)
    ret_fum_td = models.IntegerField(default=0, null=False)
    ret_blk_punt_td = models.IntegerField(default=0, null=False)
    ret_fg_td = models.IntegerField(default=0, null=False)
    ret_blk_fg_td = models.IntegerField(default=0, null=False)

    # misc
    sfty = models.IntegerField(default=0, null=False)
    blk_kick = models.IntegerField(default=0, null=False)

    # stats which factor into the DST "points allowed"
    #  ... includes safeties against the teams offense,
    #      plus interceptions and fumbles returned for TDs!
    int_td_against = models.IntegerField(default=0, null=False)
    fum_td_against = models.IntegerField(default=0, null=False)
    off_pass_sfty = models.IntegerField(default=0, null=False)
    off_rush_sfty = models.IntegerField(default=0, null=False)
    off_punt_sfty = models.IntegerField(default=0, null=False)

    class Meta:
        abstract = False
        unique_together = ('srid_player', 'srid_game')

    def save(self, *args, **kwargs):
        # perform score update
        scorer = scoring.classes.NflSalaryScoreSystem()
        # self.fantasy_points = scorer.score_player( self )

        # #
        # # pusher the fantasy points with stats
        # args = (self.get_cache_token(), push.classes.PUSHER_NFL_STATS, 'player', self.to_json())
        # self.set_cache_token()
        # countdown_send_player_stats_data.apply_async( args, countdown=COUNTDOWN )

        old_fantasy_points = self.fantasy_points
        if self.fantasy_points is None:
            self.fantasy_points = 0.0
        new_fantasy_points = scorer.score_player(self)
        self.fantasy_points = new_fantasy_points
        self.fp_change = new_fantasy_points - old_fantasy_points

        #
        # send the pusher obj for fantasy points with scoring
        # if self.fp_change != 0.0:
        # self.set_cache_token()
        # push.classes.DataDenPush   previously
        push.classes.PlayerStatsPush(push.classes.PUSHER_NFL_STATS, 'player').send(
            self.to_json(), async=settings.DATADEN_ASYNC_UPDATES)

        super().save(*args, **kwargs)


class PlayerStatsSeason(sports.models.PlayerStatsSeason):
    class Meta:
        abstract = True  # TODO


class Injury(sports.models.Injury):
    #
    # nfl injuries have ids
    srid = models.CharField(max_length=64, null=False, default='')
    practice_status = models.CharField(max_length=1024, null=False, default='')

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
    # technically, we dont need srid in nfl GamePortions - they dont have one
    # this is the srid of the quarter
    srid = models.CharField(max_length=64, null=False, default='')

    class Meta:
        abstract = False


class PbpDescription(sports.models.PbpDescription):
    #
    # this is the srid of the play, aka specific pbp object
    srid = models.CharField(max_length=64, null=False, default='')

    class Meta:
        abstract = False


class Pbp(sports.models.Pbp):
    class Meta:
        abstract = False


def create_dst_player(sender, **kwargs):
    """
    signal handler to create the DST Player object after a Team object is created.
    """
    if 'created' in kwargs:
        if kwargs['created']:
            instance = kwargs['instance']
            # ctype = ContentType.objects.get_for_model(instance)
            # entry = Player.objects.get_or_create(content_type=ctype,
            #                                         object_id=instance.id,
            #                                         pub_date=instance.pub_date)
            dst = Player()
            dst.team = instance
            dst.srid = instance.srid  #
            dst.first_name = instance.name  # ie: "Patriots"
            dst.last_name = DST_PLAYER_LAST_NAME

            #
            # get or create the custom 'dst' position for nfl
            try:
                position = sports.models.Position.objects.get(site_sport__name='nfl',
                                                              name=DST_POSITION)
            except sports.models.Position.DoesNotExist:
                position = sports.models.Position()
                position.site_sport = sports.models.SiteSport.objects.get(name='nfl')
                position.name = DST_POSITION
                position.save()

            dst.position = position

            dst.status = ''
            dst.save()  # commit changes


#
# listen for Team object save() and create its DST if it does not exist
post_save.connect(create_dst_player, sender=Team)


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
