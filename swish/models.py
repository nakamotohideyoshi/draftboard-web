#
# models.py

from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from draftgroup.models import (
    AbstractPlayerLookup,
)

class History(models.Model):

    created = models.DateTimeField(auto_now_add=True)

    http_status = models.IntegerField(null=False)

    data = JSONField()

class PlayerLookup(AbstractPlayerLookup):
    """
    the admin will be able to set up a draftboard Player and their swish api's id
    so that we can map the draftboard player to the players third party id (their 'pid')
    """
    #
    # created = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True)
    #
    # # the GFK to the sports.<SPORT>.Player instance
    # player_type = models.ForeignKey(ContentType)
    # player_id = models.PositiveIntegerField()
    # player = GenericForeignKey('player_type', 'player_id')
    #
    # # the third-party service's id for this player
    # pid = models.CharField(max_length=255, null=False)

    class Meta:
        abstract = False