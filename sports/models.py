#
# sports/models.py

from django.db import models

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

#
#########################################################################
# abstract models for each sport to inherit as use as they wish
#########################################################################

class Sport( models.Model ):
    created     = models.DateTimeField(auto_now_add=True, null=False)
    updated     = models.DateTimeField(auto_now=True)

    #
    # the generic foreign key to
    content_type    = models.ForeignKey(ContentType)
    object_id       = models.PositiveIntegerField()
    content_object  = GenericForeignKey()   # 'content_object', 'object_id'  are only necessary if custom

    class Meta:
        abstract = True

class Season( models.Model ):
    """
    information about the part of the season we are in
    """
    start_year      = models.CharField(max_length=100, null=False)
    season_type     = models.CharField(max_length=255, null=False)

    class Meta:
        abstract = True
        unique_together = ('start_year', 'season_type')

class Game( models.Model ):
    """
    information about the scheduled game - mainly the start, and status
    """
    start   = models.DateTimeField(null=False)
    status  = models.CharField(max_length=32, null=False)

    class Meta:
        abstract = True

class GameBoxscore(models.Model):
    class Meta:
        abstract = True

class Player(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    srid = models.CharField(max_length=64, unique=True, null=False,
                                help_text='the sportsradar global id')
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)

    class Meta:
        abstract = True

class Team(models.Model):
    class Meta:
        abstract = True

class PlayerStats(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    srid_game   = models.CharField(max_length=64, null=False,
                            help_text='the sportsradar global id for the game')
    srid_player = models.CharField(max_length=64, null=False,
                            help_text='the sportsradar global id for the player')

    class Meta:
        abstract = True
        unique_together = ('srid_game', 'srid_player')

class PlayerStatsSeason(models.Model):
    class Meta:
        abstract = True

class Injury(models.Model):
    class Meta:
        abstract = True

class RosterPlayer(models.Model):
    class Meta:
        abstract = True

class Venue(models.Model):
    class Meta:
        abstract = True