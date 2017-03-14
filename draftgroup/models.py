from django.utils import timezone
from django.db import models
import salary.models
import draftgroup.classes
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
import contest.models


class DraftGroup(models.Model):
    """
    The "master" id table for a group of draftable players on a day.
    """

    #
    # DEFAULT_CATEGORY is the default name of the draft group -- just empty string for now.
    # it may end up being something like "Early", "Late", "All Day", etc... for partial-day groups
    DEFAULT_CATEGORY = ''

    # dt_format   = "%a, %d @ %I:%M%p" # strftime("%A, %d. %B %Y %I:%M%p")
    created = models.DateTimeField(auto_now_add=True)

    salary_pool = models.ForeignKey(
        salary.models.Pool,
        verbose_name='the Salary Pool is the set of active player salaries for a sport')

    start = models.DateTimeField(
        null=False,
        help_text='the DateTime for the earliest possible players in the group.')

    end = models.DateTimeField(
        null=False,
        help_text='the DateTime on, or after which no players from games are included')

    num_games = models.IntegerField(
        null=False,
        default=0,
        help_text="the number of live games this draft group spans")

    category = models.CharField(
        max_length=32,
        null=True,
        help_text='currently unused - originally intended as a grouping like "Early", "Late", or '
                  '"Turbo"')

    closed = models.DateTimeField(
        blank=True,
        null=True,
        help_text='the time at which all live games in the draft group were closed out and stats '
                  'were finalized by the provider')

    fantasy_points_finalized = models.DateTimeField(
        blank=True,
        null=True,
        help_text='if set, this is the time the "final_fantasy_points" for each draftgroup player '
                  'was updated')

    def get_games(self):
        """
        return the underlying sport.<sport>.Game objects this draft group was created with
        """
        dgm = draftgroup.classes.DraftGroupManager()
        return dgm.get_games(self)

    def is_started(self):
        """
        :return: True if the system time is past the start time for the draftgroup
        """
        return timezone.now() >= self.start

    def __str__(self):
        return '<DraftGroup: id: %s | sport: %s | start: %s | end: %s | # games: %s>' % (
            self.pk, self.salary_pool.site_sport.name, self.start, self.end, self.num_games)

    def __format_dt(self, dt):
        return dt.strftime(self.dt_format)


class UpcomingDraftGroup(DraftGroup):
    """
    PROXY model for Upcoming DraftGroups ... and rest API use.
    """

    class UpcomingDraftGroupManager(models.Manager):
        def get_queryset(self):
            # get the distinct DraftGroup(s) only upcoming contests
            distinct_contest_draft_groups = contest.models.UpcomingContestPool.objects.filter(
                draft_group__isnull=False).distinct('draft_group')
            # build a list of the (distinct) draft_group.pk's
            draft_group_ids = [c.draft_group.pk for c in distinct_contest_draft_groups]
            return super().get_queryset().filter(pk__in=draft_group_ids)

    objects = UpcomingDraftGroupManager()

    class Meta:
        proxy = True


class CurrentDraftGroup(DraftGroup):
    """
    PROXY model for Upcoming & Live DraftGroups ... and rest API use.
    """

    class CurrentDraftGroupManager(models.Manager):
        # just get the draftgroups from the LobbyContests which has Live and Upcoming contests

        def get_queryset(self):
            # get the distinct DraftGroup(s) associated with contest currently in the lobby
            distinct_contest_draft_groups = contest.models.CurrentContest.objects.filter(
                draft_group__isnull=False).distinct('draft_group')
            # build a list of the (distinct) draft_group.pk's
            draft_group_ids = []
            for c in distinct_contest_draft_groups:
                draft_group = c.draft_group
                if draft_group is not None:
                    draft_group_ids.append(draft_group.pk)

            return super().get_queryset().filter(pk__in=draft_group_ids)

    objects = CurrentDraftGroupManager()

    class Meta:
        proxy = True


class GameTeam(models.Model):
    """
    Keep track of the Teams in the Games from which we've
    created the draft group.

    Most just a historical thing , or potentially for debugging later on
    """
    created = models.DateTimeField(auto_now_add=True, null=False)
    draft_group = models.ForeignKey(DraftGroup, null=False)
    # the start time of the game when the draftgroup was created!
    start = models.DateTimeField(null=False)
    game_srid = models.CharField(max_length=64, null=False)
    team_srid = models.CharField(max_length=64, null=False)
    alias = models.CharField(max_length=64, null=False)


class Player(models.Model):
    """
    A player is associated with a DraftGroup and a salary.models.Salary
    """

    created = models.DateTimeField(
        auto_now_add=True,
        null=False
    )
    draft_group = models.ForeignKey(
        DraftGroup,
        null=False,
        verbose_name='the DraftGroup this player is a member of', related_name='players'
    )
    salary_player = models.ForeignKey(
        salary.models.Salary,
        null=False,
        verbose_name='points to the player salary object, which has fantasy salary information',
        related_name = "draft_group_player"
    )
    salary = models.FloatField(
        default=0,
        null=False,
        help_text='the amount of salary for the player at the this draft group was created',
    )
    start = models.DateTimeField(null=False)
    final_fantasy_points = models.FloatField(
        default=0,
        null=False,
        help_text='the payout-time fantasy points of this player'
    )

    # let it be null if the info is unknown,# #
    # # and we can set it to various thing depending on whether the information
    # # is known or not
    # # unofficial_status => 'us'
    # us = models.CharField(max_length=2048, null=True)
    # # official_status => 'os'
    # os = models.CharField(max_length=2048, null=True)

    def __str__(self):
        return '<DraftGroup.Player: player: %s | salary: $%.2f | final_fp: %s>' % (
            self.player, self.salary, self.final_fantasy_points)

    # we need to create the draft group player associated with a certain team
    game_team = models.ForeignKey(GameTeam, null=False)

    @property
    def srid(self):
        return self.salary_player.player.srid

    @property
    def player(self):
        return self.salary_player.player

    @property
    def first_name(self):
        return self.salary_player.player.first_name

    @property
    def last_name(self):
        return self.salary_player.player.last_name

    @property
    def name(self):
        return ('%s %s' % (self.salary_player.player.first_name, self.salary_player.player.last_name)).replace('.', '')

    @property
    def player_id(self):
        return self.salary_player.player.pk

    @property
    def position(self):
        return self.salary_player.player.position.name

    @property
    def team_alias(self):
        return self.salary_player.player.team.alias

    @property
    def fppg(self):
        return self.salary_player.fppg

    class Meta:
        # each player should only exist once in each group!
        unique_together = ('draft_group', 'salary_player')


class AbstractPlayerLookup(models.Model):
    """
    abstract model for other apps to use to create a table that
    links a Player to a third-party 'pid' (a player id)
    """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    sport = models.CharField(
        max_length=8,
        null=True,
        blank=True,
        choices=(
            ('NBA', 'NBA'),
            ('NHL', 'NHL'),
            ('NFL', 'NFL'),
            ('MLB', 'MLB'),
        )
    )
    # Since a player lookup can only have a generic relation with a <sport>.Player model, use this to
    # limit it. This is mostly for use in the admin section.
    model_limit = models.Q(app_label='nfl', model='player') | \
        models.Q(app_label='nba', model='player') | \
        models.Q(app_label='mlb', model='player') | \
        models.Q(app_label='nhl', model='player')
    # the GFK to the sports.<SPORT>.Player instance
    player_type = models.ForeignKey(
        ContentType,
        related_name='%(app_label)s_%(class)s_player_lookup',
        null=True,
        blank=True,
        limit_choices_to=model_limit
    )
    player_id = models.PositiveIntegerField(
        null=True,
        blank=True
    )
    player = GenericForeignKey(
        'player_type',
        'player_id',
    )
    # the third-party service's id for this player
    pid = models.CharField(max_length=255, null=False)
    # first and last name can be used to know who the player is
    first_name = models.CharField(max_length=255, null=False, blank=True)
    last_name = models.CharField(max_length=255, null=False, blank=True)

    class Meta:
        abstract = True


class AbstractUpdate(models.Model):
    """
    abstract parent model for PlayerUpdate, GameUpdate
    which includes some common fields of updates
    that come from rotowire/espn/twitter/etc...
    """
    created = models.DateTimeField(auto_now_add=True)
    update_id = models.CharField(max_length=128, null=True)
    # this should be set to the time the source info claims it was posted/published
    updated_at = models.DateTimeField(null=False)
    type = models.CharField(max_length=128, null=False, default='')
    value = models.CharField(max_length=1024 * 8, null=False, default='')
    # swish status
    status = models.CharField(max_length=128, null=False, default='na')
    # a name, typically, for twitter this will be @their_twitter_name
    source_origin = models.CharField(max_length=255, null=True)
    # a url, of the original post, ie: for twitter, link straight to the tweet
    url_origin = models.CharField(max_length=255, null=True)

    class Meta:
        abstract = True


class PlayerUpdate(AbstractUpdate):
    NEWS = 'news'
    INJURY = 'injury'
    LINEUP = 'lineup'
    START = 'start'
    CATEGORIES = [
        (NEWS, 'News'),
        (INJURY, 'Injury'),
        (LINEUP, 'Lineup'),
        (START, 'Start'),
    ]

    draft_groups = models.ManyToManyField(DraftGroup)
    player_srid = models.CharField(max_length=64, null=False)
    player_id = models.IntegerField(null=False, default=0)
    category = models.CharField(max_length=64, choices=CATEGORIES, null=False, default=NEWS)
    # roster_status = models.CharField(max_length=64, null=True)
    # roster_status_description = models.CharField(max_length=255, null=True)
    # depth_chart_status = models.CharField(max_length=64, null=True)
    # player_status_probability = models.FloatField(default=0, null=True)
    # player_status_confidence = models.FloatField(default=0, null=True)
    # last_text = models.CharField(max_length=1024 * 8, null=True, default='')
    # game_id = models.IntegerField(null=False, default=0)
    sport = models.CharField(max_length=4, null=False)

    class Meta:
        abstract = False

    def __str__(self):
        return '<PlayerUpdate: pk:%s | %s | %s>' % (self.pk, self.player_srid, self.category)


class GameUpdate(AbstractUpdate):
    NEWS = 'news'
    LINEUP = 'lineup'
    CATEGORIES = [
        (NEWS, 'News'),
        (LINEUP, 'Lineup'),
    ]

    draft_groups = models.ManyToManyField(DraftGroup)
    game_srid = models.CharField(max_length=64, null=False)
    game_id = models.IntegerField(null=False, default=0)
    category = models.CharField(max_length=64, choices=CATEGORIES, null=False, default=NEWS)

    class Meta:
        abstract = False
