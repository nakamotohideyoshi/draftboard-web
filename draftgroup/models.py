#
# draftgroup/models.py

from django.db import models
import salary.models
import draftgroup.classes

class DraftGroup( models.Model ):
    """
    The "master" id table for a group of draftable players on a day.
    """
    dt_format   = "%a, %d @ %I:%M%p" # strftime("%A, %d. %B %Y %I:%M%p")
    created     = models.DateTimeField(auto_now_add=True)

    salary_pool = models.ForeignKey(salary.models.Pool,
                    verbose_name='the Salary Pool is the set of active player salaries for a sport')

    start       = models.DateTimeField(null=False,
                        help_text='the DateTime for the earliest possible players in the group.')
    end         = models.DateTimeField(null=False,
                        help_text='the DateTime on, or after which no players from games are included')

    def get_games(self):
        """
        return the underlying sport.<sport>.Game objects this draft group was created with
        """
        dgm = draftgroup.classes.DraftGroupManager()
        return dgm.get_games( self )

    def __str__(self):
        return 'pk: %s  |  %s thru %s' % (self.pk,
                                        self.__format_dt(self.start),
                                        self.__format_dt(self.end) )

    def __format_dt(self, dt):
        return dt.strftime(self.dt_format)

class Player( models.Model ):
    """
    A player is associated with a DraftGroup and a salary.models.Salary
    """
    created     = models.DateTimeField(auto_now_add=True, null=False)
    draft_group = models.ForeignKey( DraftGroup, null=False,
                    verbose_name='the DraftGroup this player is a member of')

    salary_player = models.ForeignKey(salary.models.Salary, null=False,
                    verbose_name='points to the player salary object, which has fantasy salary information')

    salary      = models.FloatField(default=0, null=False,
                    help_text='the amount of salary for the player at the this draft group was created')
    start = models.DateTimeField(null=False)

    @property
    def player(self):
        return self.salary_player.player

    class Meta:
        # each player should only exist once in each group!
        unique_together = ('draft_group','salary_player')

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