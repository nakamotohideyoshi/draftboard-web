#
# models.py

from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from draftgroup.models import (
    # AbstractPlayerLookup,
    AbstractNflPlayerLookup,
)

class PlayerLookup(AbstractNflPlayerLookup):
    """
    the admin will be able to set up a draftboard Player and their STATS.com api's id
    so that we can map the swish player to the draftboard player.
    """

    class Meta:
        abstract = False

        ordering = ('last_name', 'first_name', 'created')
