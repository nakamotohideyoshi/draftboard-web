from django.db import models
from django.contrib.auth.models import User

class Lineup(models.Model):
    """
    Lineup is an object which represents a user-created team.
    Lineups can be entered into Contests.
    """

    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)

    fantasy_points  = models.FloatField(default=0.0, null=False, blank=True)
    user            = models.ForeignKey(User, null=False)
    draftgroup      = models.ForeignKey('draftgroup.DraftGroup', null=False)
    def __str__(self):
        return '%s %s %s' % (self.user, self.fantasy_points, 'NAME_TODO')
