#
# sports/models.py

from django.db import models

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

#
#########################################################################
# abstract models for each sport to inherit as use as they wish
#########################################################################

# class Sport( models.Model ):
#     created     = models.DateTimeField(auto_now_add=True, null=False)
#     updated     = models.DateTimeField(auto_now=True)
#
#     #
#     # the generic foreign key to
#     content_type    = models.ForeignKey(ContentType)
#     object_id       = models.PositiveIntegerField()
#     content_object  = GenericForeignKey()   # 'content_object', 'object_id'  are only necessary if custom
#
#     class Meta:
#         abstract = True

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

# class GameBoxscore(models.Model):
#     pass
#
# class Player(models.Model):
#     pass
#
# class Team(models.Model):
#     pass
#
# class PlayerStats(models.Model):
#     pass
#
# class PlayerStatsSeason(models.Model):
#     pass
#
# class Injury(models.Model):
#     pass
#
# class RosterPlayer(models.Model):
#     pass
#
# class Venue(models.Model):
#     pass