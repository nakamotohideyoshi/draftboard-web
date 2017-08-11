from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from roster.models import RosterSpot


class Lineup(models.Model):
    """
    Lineup is an object which represents a user-created team.
    Lineups can be entered into Contests.
    """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    fantasy_points = models.FloatField(default=0.0, null=False, blank=True)
    user = models.ForeignKey(User, null=False)
    draft_group = models.ForeignKey('draftgroup.DraftGroup', null=False)

    name = models.CharField(max_length=64, null=False, default='')

    @property
    def sport(self):
        return self.draft_group.salary_pool.site_sport.name

    def __str__(self):
        return '<Lineup id: %s | user: %s | fp: %s | name: "%s" | draft_group: %s' % (
            self.id, self.user, self.fantasy_points, self.name, self.draft_group)


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
                               null=False, related_name="players")

    roster_spot = models.ForeignKey(RosterSpot)

    # we save the pk to the draft_group_player for easier
    # lookups later. it also allows us to know which
    # team the player played for at the time of the draftgroup
    # which is very important
    draft_group_player = models.ForeignKey('draftgroup.Player', null=False)

    #
    # Actual layout not per position from 0-X
    idx = models.PositiveIntegerField(default=0, null=False)

    @property
    def full_name(self):
        return '%s %s' % (self.player.first_name, self.player.last_name)

    def __str__(self):
        return '<Lineup.Player id: %s | full_name: %s | lineup: %s>' % (
            self.id, self.full_name, self.lineup)
