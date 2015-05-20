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
    created = models.DateTimeField(auto_now_add=True)

    srid = models.CharField(max_length=64, unique=True, null=False,
                                help_text='the sportsradar global id')

    start   = models.DateTimeField(null=False)
    status  = models.CharField(max_length=32, null=False)

    def __str__(self):
        return '%s | %s | %s' % (self.status, self.start, self.srid)

    class Meta:
        abstract = True

class GameBoxscore(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    srid_game   = models.CharField(max_length=64, null=False, unique=True, default=None,
                            help_text='the sportsradar global id for the game')

    srid_home   = models.CharField(max_length=64, null=False)
    srid_away   = models.CharField(max_length=64, null=False)

    attendance  = models.IntegerField(default=0, null=False)
    coverage    = models.CharField(max_length=16, null=False, default='')
    status      = models.CharField(max_length=64, null=False, default='')

    home_score = models.IntegerField(default=0, null=False)
    away_score = models.IntegerField(default=0, null=False)

    title       = models.CharField(max_length=256, null=False, default='')

    # sport specific json for the scoring list,
    # if its mlb, its innings, if its nba its quarters...
    home_scoring_json   = models.CharField(max_length=2048, null=False, default = '')
    away_scoring_json   = models.CharField(max_length=2048, null=False, default = '')

    class Meta:
        abstract = True

class Player(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    srid = models.CharField(max_length=64, unique=True, null=False,
                                help_text='the sportsradar global id')
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    class Meta:
        abstract = True

class Team(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    srid = models.CharField(max_length=64, unique=True, null=False,
                                help_text='the sportsradar global id')

    srid_venue  = models.CharField(max_length=64, null=False,
                      help_text='the sportsradar global id')

    name        = models.CharField(max_length=64, null=False, default='',
                                   help_text='the team name, without the market/city. ie: "Lakers", or "Eagles"')
    alias       = models.CharField(max_length=64, null=False, default='',
                                   help_text='the abbreviation for the team, ie: for Boston Celtic alias == "BOS"')

    def __str__(self):
        return '%s | %s' % (self.name, self.alias)

    class Meta:
        abstract = True

class TeamStats(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    srid_game   = models.CharField(max_length=64, null=False,
                            help_text='the sportsradar global id for the game')
    srid_team = models.CharField(max_length=64, null=False,
                            help_text='the sportsradar global id for the team')
    class Meta:
        abstract = True
        unique_together = ('srid_game', 'srid_team')

class PlayerStats(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    srid_game   = models.CharField(max_length=64, null=False,
                            help_text='the sportsradar global id for the game')
    srid_player = models.CharField(max_length=64, null=False,
                            help_text='the sportsradar global id for the player')

    # the GFK to the Game
    game_type           = models.ForeignKey(ContentType,  related_name='%(app_label)s_%(class)s_sport_game')
    game_id             = models.PositiveIntegerField()
    game                = GenericForeignKey('game_type', 'game_id')

    # the GFK to the Player
    player_type         = models.ForeignKey(ContentType,  related_name='%(app_label)s_%(class)s_sport_player')
    player_id           = models.PositiveIntegerField()
    player              = GenericForeignKey('player_type', 'player_id')

    fantasy_points      = models.FloatField(default=0.0, null=False)
    position            = models.CharField(max_length=16, null=False, default='')
    primary_position    = models.CharField(max_length=16, null=False, default='')

    class Meta:
        abstract = True
        unique_together = ('srid_player','srid_game')


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
    created = models.DateTimeField(auto_now_add=True)

    srid = models.CharField(max_length=64, unique=True, null=False,
                                help_text='the sportsradar global id')
    class Meta:
        abstract = True