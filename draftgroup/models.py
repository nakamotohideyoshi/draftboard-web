#
# draftgroup/models.py

from django.db import models
import salary.models

class DraftGroup( models.Model ):
    """
    The "master" id table for a group of draftable players on a day.
    """
    created     = models.DateTimeField(auto_now_add=True)

    salary_pool = models.ForeignKey(salary.models.Pool,
                    verbose_name='the Salary Pool is the set of active player salaries for a sport')

    start_dt    = models.DateTimeField(null=False,
                        help_text='the DateTime for the earliest possible players in the group.')
    start_ts    = models.IntegerField(null=False, default=0,
                        help_text='save() converts start_dt into a unix timestamp and sets the value to this field')

    def save(self, *args, **kwargs):
        if self.start_dt:
            self.start_ts = int(self.start_dt.strftime('%s'))
        super().save(*args, **kwargs)

class Player( models.Model ):
    """
    A player is associated with a DraftGroup and a salary.models.Salary
    """
    draft_group = models.ForeignKey( DraftGroup, null=False,
                    verbose_name='the DraftGroup this player is a member of')

    salary = models.ForeignKey(salary.models.Salary, null=False,
                    verbose_name='points to the player salary object, which has fantasy salary information')

    class Meta:
        # each player should only exist once in each group!
        unique_together = ('draft_group','salary')