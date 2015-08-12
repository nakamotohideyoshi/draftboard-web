#
# sports/models.py

from django.db import models

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
import re

from django.dispatch import Signal, receiver
from django.db.models.signals import pre_save
from dirtyfields import DirtyFieldsMixin
import django.core.exceptions

class SignalNotSetupProperlyException(Exception):
    def __init__(self, class_name, variable_name):
       super().__init__('You must set "signal"')

class AbstractSportSignal(object):

    signal = None # child will have to set this

    def __init__(self):
        self.__validate()

    def __validate(self):
        if self.signal is None:
            raise SignalNotSetupProperlyException(self.__class__.__name__, 'signal')

    def send(self, **kwargs):
        # print( 'sender', str(self.__class__.__name__))
        # for k,v in kwargs.items():
        #     print( str(k), '=>', str(v) )
        #     if k == 'game':
        #         print( '... type: ', str(type(v).__name__) )
        #         print( '... srid: ', v.srid )
        self.signal.send(sender=self.__class__, **kwargs)

class GameStatusChangedSignal(AbstractSportSignal):
    """
    a signal that contains an object with stats that need to be saved
    """

    signal = Signal(providing_args=['game'])

    def __init__(self, game):
        super().__init__()
        self.game = game

    def send(self):
        """
        call parent send() with the object which has had a change to it
        """
        super().send( game=self.game )

# an object for a sport which anything can reference to identify its sport
class SiteSport(models.Model):
    created             = models.DateTimeField(auto_now_add=True, null=False)
    name                = models.CharField(max_length=128, null=False, unique=True)

    def __str__(self):
        return '%s' % (self.name )



class Position(models.Model):
    created     = models.DateTimeField(auto_now_add=True, null=False)
    name        = models.CharField(max_length=128, null=False)
    site_sport  = models.ForeignKey(SiteSport, null=False)

    class Meta:
        unique_together = ('name', 'site_sport')

    def __str__(self):
        return '%s - %s' % (self.site_sport.name, self.name )

    def get_matchname(self):
        """Returns the match name for a tag"""
        return re.sub("\W+" , "", self.name)
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

class Game( DirtyFieldsMixin, models.Model ):
    """
    information about the scheduled game - mainly the start, and status
    """

    STATUS_CLOSED = 'closed'

    created = models.DateTimeField(auto_now_add=True)

    srid = models.CharField(max_length=64, unique=True, null=False,
                                help_text='the sportsradar global id')

    start       = models.DateTimeField(null=False)
    status      = models.CharField(max_length=32, null=False)
    prev_status = models.CharField(max_length=32, null=False, default='')

    def is_closed(self):
        """
        Indicates if this game is closed (complete + all stat corrections are in).

        Return a boolean indicating if this instance's
        status field is equal to the STATUS_CLOSED value.
        """
        return self.status == self.STATUS_CLOSED

    def __str__(self):
        return '%s | %s | %s' % (self.status, self.start, self.srid)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        override save so we can signal certain changes
        to this object after the "real" save()
        """

        # cache the changed fields before save() called because it will reset them
        try:
            changed_fields = self.get_dirty_fields()
        except django.core.exceptions.ValidationError:
            print('Game model self.get_dirty_fields() threw django.core.exceptions.ValidationError because of a datetime problem... skipping it for testing purposes')
            print('debug>>>', 'game.start', str(self.start), 'game instance[', str( self ), ']' )
            changed_fields = {}

        super().save(*args, **kwargs) # Call the "real" save() method.

        # check if status had been changed, now that the save() was successful
        if changed_fields.get('status', None):
            # send signal that the Game status has changed
            #print( 'game.status changed: sending signal' )
            GameStatusChangedSignal( self ).send()
        # else:
        #     print( 'not sending signal - unchanged status')

class GameBoxscore(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    srid_game   = models.CharField(max_length=64, null=False, unique=True, default=None,
                            help_text='the sportsradar global id for the game')

    srid_home   = models.CharField(max_length=64, null=False)
    srid_away   = models.CharField(max_length=64, null=False)

    # the GFK to the home team
    home_type           = models.ForeignKey(ContentType,  related_name='%(app_label)s_%(class)s_home_team')
    home_id             = models.PositiveIntegerField()
    home                = GenericForeignKey('home_type', 'home_id')

    # the GFK to the away team
    away_type         = models.ForeignKey(ContentType,  related_name='%(app_label)s_%(class)s_away_team')
    away_id           = models.PositiveIntegerField()
    away              = GenericForeignKey('away_type', 'away_id')

    attendance  = models.IntegerField(default=0, null=False)
    coverage    = models.CharField(max_length=64, null=False, default='')
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

class Injury(models.Model):
    created     = models.DateTimeField(auto_now_add=True)

    #
    # "injury id" field:
    # for some sports this is the srid (nba/nhl), for sports like
    # mlb it is a standard injury type like "DL15". each sport
    # may use it for its own purposes, but must be consistent about its usage
    iid = models.CharField(max_length=128, unique=True, null=False,
                                    help_text='custom injury id')

    player_type           = models.ForeignKey(ContentType,  related_name='%(app_label)s_%(class)s_injured_player')
    player_id             = models.PositiveIntegerField()
    player                = GenericForeignKey('player_type', 'player_id')

    status      = models.CharField(max_length=32, default='')
    description = models.CharField(max_length=1024, default='')

    class Meta:
        abstract = True

class Player(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    srid = models.CharField(max_length=64, unique=True, null=False,
                                help_text='the sportsradar global id')
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)

    # reference the position
    position    = models.ForeignKey(Position, null=False, related_name='%(app_label)s_%(class)s_player_position')

    # the GFK to the Game
    injury_type           = models.ForeignKey(ContentType, null=True, related_name='%(app_label)s_%(class)s_players_injury')
    injury_id             = models.PositiveIntegerField(null=True)
    injury                = GenericForeignKey('injury_type', 'injury_id')

    # # the GFK to the Team
    # team_type         = models.ForeignKey(ContentType,  related_name='%(app_label)s_%(class)s_player_team')
    # team_id           = models.PositiveIntegerField()
    # team              = GenericForeignKey('team_type', 'team_id')

    def remove_injury(self):
        """
        Remove the injury, if one exists.

        Returns True if it actual removed an injury, otherwise returns False.
        """
        if self.injury:
            self.injury = None
            self.save()
            return True
        return False

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

    # reference the position FROM THE PLAYER WHEN THEY PLAYED THE GAME.
    #   ie: the players position might be different now! but we want
    #       the position they were when the played in the game!
    position    = models.ForeignKey(Position, null=False,
                    related_name='%(app_label)s_%(class)s_playerstats_position')

    #position            = models.CharField(max_length=16, null=False, default='')
    # primary_position    = models.CharField(max_length=16, null=False, default='')

    class Meta:
        abstract = True
        unique_together = ('srid_player','srid_game')

    def __str__(self):
        return 'game %s | player %s | fantasy_points %s' % (self.srid_game,
                                        self.srid_player, self.fantasy_points)

class PlayerStatsSeason(models.Model):
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

class GamePortion(models.Model):
    """
    Defines the least divisible part of a game.
    ie: there can be a GamePortion for each inning-half of mlb games,
    quarters or nba/nfl games, and periods of nhl games.
    """
    created = models.DateTimeField(auto_now_add=True)
    srid_game   = models.CharField(max_length=64, null=False,
                            help_text='the sportsradar global id for the game this is associate with')

    # the GFK to the Game
    game_type           = models.ForeignKey(ContentType,  related_name='%(app_label)s_%(class)s_sport_game')
    game_id             = models.PositiveIntegerField()
    game                = GenericForeignKey('game_type', 'game_id')

    category = models.CharField(max_length=32, null=False, default='',
                                help_text='typically one of these: ["inning-half","quarter","period"]' )
    sequence = models.IntegerField(default=0, null=False,
                                   help_text='an ordering of all GamePortions with the same srid_game')

    class Meta:
        abstract = True
        unique_together = ('srid_game','sequence')

class PbpDescription(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    # the GFK to the main pbp object
    pbp_type            = models.ForeignKey(ContentType,  related_name='%(app_label)s_%(class)s_pbpdesc_pbp')
    pbp_id              = models.PositiveIntegerField()
    pbp                 = GenericForeignKey('pbp_type', 'pbp_id')

    portion_type        = models.ForeignKey(ContentType,  related_name='%(app_label)s_%(class)s_pbpdesc_portion')
    portion_id          = models.PositiveIntegerField()
    portion             = GenericForeignKey('portion_type', 'portion_id')

    idx                 = models.IntegerField(default=0, null=False)
    description         = models.CharField(max_length=1024, null=False, default='')

    @property
    def srid_game(self):
        return self.pbp.srid_game

    @property
    def category(self):
        return self.portion.category

    @property
    def sequence(self):
        return self.portion.sequence

    class Meta:
        abstract = True

class Pbp(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    srid_game   = models.CharField(max_length=64, null=False,
                            help_text='the sportsradar global id for the game')

    # the GFK to the Game
    game_type           = models.ForeignKey(ContentType,  related_name='%(app_label)s_%(class)s_sport_game')
    game_id             = models.PositiveIntegerField()
    game                = GenericForeignKey('game_type', 'game_id')

    descriptions        = GenericRelation(PbpDescription,
                                          content_type_field='pbp_type',
                                          object_id_field='pbp_id' )
    class Meta:
        abstract = True