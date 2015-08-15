from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from roster.models import RosterSpot
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


class Player(models.Model):
    """
    Connects a :class:`lineup.models.Lineup` model to a :class:`sports.model.Player`
    """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    player_type = models.ForeignKey(ContentType,
                                    null=False,
                                    related_name='%(app_label)s_%(class)s_player')
    player_id = models.PositiveIntegerField(null=False)
    player = GenericForeignKey('player_type',
                               'player_id')

    lineup = models.ForeignKey(Lineup,
                               null=False)

    roster_spot = models.ForeignKey(RosterSpot)

    #
    # Actual layout not per position from 0-X
    idx = models.PositiveIntegerField(default=0, null=False)

    @property
    def full_name(self):
        return '%s %s' % (self.player.first_name, self.player.last_name)


