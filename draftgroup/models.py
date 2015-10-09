#
# draftgroup/models.py

from django.utils import timezone
from django.db import models
import salary.models
import draftgroup.classes
from  django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
import contest.models

class DraftGroup( models.Model ):
    """
    The "master" id table for a group of draftable players on a day.
    """

    #
    # DEFAULT_CATEGORY is the default name of the draft group -- just empty string for now.
    # it may end up being something like "Early", "Late", "All Day", etc... for partial-day groups
    DEFAULT_CATEGORY = ''

    #dt_format   = "%a, %d @ %I:%M%p" # strftime("%A, %d. %B %Y %I:%M%p")
    created     = models.DateTimeField(auto_now_add=True)

    salary_pool = models.ForeignKey(salary.models.Pool,
                    verbose_name='the Salary Pool is the set of active player salaries for a sport')

    start       = models.DateTimeField(null=False,
                        help_text='the DateTime for the earliest possible players in the group.')
    end         = models.DateTimeField(null=False,
                        help_text='the DateTime on, or after which no players from games are included')

    num_games   = models.IntegerField(null=False, help_text="the number of live games this draft group spans")

    category    = models.CharField(max_length=32, null=True)

    def get_games(self):
        """
        return the underlying sport.<sport>.Game objects this draft group was created with
        """
        dgm = draftgroup.classes.DraftGroupManager()
        return dgm.get_games( self )

    def is_started(self):
        """
        :return: True if the system time is past the start time for the draftgroup
        """
        return timezone.now() >= self.start

    def __str__(self):
        return '%s id:%s' % (self.salary_pool.site_sport.name, str(self.pk))

    def __format_dt(self, dt):
        return dt.strftime(self.dt_format)

class UpcomingDraftGroup(DraftGroup):
    """
    PROXY model for Upcoming DraftGroups ... and rest API use.

    """
    class UpcomingDraftGroupManager(models.Manager):

        def get_queryset(self):
            # get the distinct DraftGroup(s) associated with contest currently in the lobby
            distinct_contest_draft_groups = contest.models.LobbyContest.objects.filter().distinct('draft_group')
            # build a list of the (distinct) draft_group.pk's
            draft_group_ids = [c.draft_group.pk for c in distinct_contest_draft_groups ]
            return super().get_queryset().filter(pk__in=draft_group_ids)

    objects = UpcomingDraftGroupManager()

    class Meta:
        proxy = True

class GameTeam( models.Model ):
    """
    Keep track of the Teams in the Games from which we've
    created the draft group.

    Most just a historical thing , or potentially for debugging later on
    """
    created     = models.DateTimeField(auto_now_add=True, null=False)

    draft_group = models.ForeignKey( DraftGroup, null=False )

    # the start time of the game when the draftgroup was created!
    start  = models.DateTimeField(null=False)
    game_srid   = models.CharField(max_length=64, null=False)
    team_srid   = models.CharField(max_length=64, null=False)
    alias       = models.CharField(max_length=64, null=False)

class Player( models.Model ):
    """
    A player is associated with a DraftGroup and a salary.models.Salary
    """
    created     = models.DateTimeField(auto_now_add=True, null=False)
    draft_group = models.ForeignKey( DraftGroup, null=False,
                    verbose_name='the DraftGroup this player is a member of', related_name='players')

    salary_player = models.ForeignKey(salary.models.Salary, null=False,
                    verbose_name='points to the player salary object, which has fantasy salary information')

    salary      = models.FloatField(default=0, null=False,
                    help_text='the amount of salary for the player at the this draft group was created')
    start = models.DateTimeField(null=False)

    def __str__(self):
        return '%s $%.2f' % (str(self.player), self.salary)

    # we need to create the draft group player associated with a certain team
    game_team = models.ForeignKey(GameTeam, null=False)

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
        return '%s %s' % (self.salary_player.player.first_name, self.salary_player.player.last_name)

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
        unique_together = ('draft_group','salary_player')
