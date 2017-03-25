#
# sports/models.py

import json
import re

import django.core.exceptions
from dateutil.parser import parse
from dirtyfields import DirtyFieldsMixin
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core import serializers  # we will serialize select models, mainly for api use
from django.core.cache import cache
from django.db import models
from django.dispatch import Signal


class SignalNotSetupProperlyException(Exception):
    def __init__(self, class_name, variable_name):
        super().__init__('You must set "signal"')


class AbstractSportSignal(object):
    signal = None  # child will have to set this

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
        super().send(game=self.game)


# an object for a sport which anything can reference to identify its sport
class SiteSport(models.Model):
    """
    there can only be 1 instance of this model for each sport.

    the current season needs to be manually set.
    """
    created = models.DateTimeField(auto_now_add=True, null=False)
    name = models.CharField(max_length=128, null=False, unique=True)

    current_season = models.IntegerField(null=True,
                                         help_text='year this sports current season began in. example: '
                                                   'for the nba 2015-16 season, current_season should be set to: 2015')

    def __str__(self):
        return '%s' % (self.name)


class Position(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=False)
    name = models.CharField(max_length=128, null=False)
    site_sport = models.ForeignKey(SiteSport, null=False)

    class Meta:
        unique_together = ('name', 'site_sport')

    def __str__(self):
        return '%s - %s' % (self.site_sport.name, self.name)

    def get_matchname(self):
        """Returns the match name for a tag"""
        return re.sub("\W+", "", self.name)


#
#########################################################################
# abstract models for each sport to inherit as use as they wish
#########################################################################

class Sport(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=False)
    updated = models.DateTimeField(auto_now=True)

    #
    # the generic foreign key to
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()  # 'content_object', 'object_id'  are only necessary if custom

    class Meta:
        abstract = True


class Season(models.Model):
    """
    information about the part of the season we are in
    """

    srid = models.CharField(max_length=64, null=False,
                            help_text='the sportsradar global id of the season/schedule')
    season_year = models.IntegerField(default=0, null=False,
                                      help_text='the year the season started')
    season_type = models.CharField(max_length=255, null=False)

    class Meta:
        abstract = True
        unique_together = ('srid', 'season_year', 'season_type')

    def __str__(self):
        return "<Season type: %s | year: %s | srid: %s>" % (
            self.season_type, self.season_year, self.srid)

class Game(DirtyFieldsMixin, models.Model):
    """
    information about the scheduled game - mainly the start, and status
    """

    STATUS_CLOSED = 'closed'
    STATUS_INPROGRESS = 'inprogress'

    SEASON_TYPE_PRE = 'pre'  # preseason
    SEASON_TYPE_REG = 'reg'  # regular season
    SEASON_TYPE_PST = 'pst'  # postseason
    SEASON_TYPES = [
        (SEASON_TYPE_PRE, 'Preseason'),
        (SEASON_TYPE_REG, 'Regular Season'),
        (SEASON_TYPE_PST, 'Postseason'),
    ]

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    srid = models.CharField(
        max_length=64,
        unique=True,
        null=False,
        help_text='the sportsradar global id'
    )

    # season_year = models.IntegerField(default=0, null=False,
    #                                   help_text='the year the season started')
    # season_type = models.CharField(max_length=32, default=SEASON_TYPE_REG, null=False, choices=SEASON_TYPES)

    start = models.DateTimeField(null=False)
    status = models.CharField(max_length=32, null=False)
    prev_status = models.CharField(max_length=32, null=False, default='')

    boxscore_data = models.CharField(max_length=1024 * 8, null=True)

    def get_home_at_away_str(self):
        return '%s @ %s' % (str(self.away), str(self.home))

    def is_closed(self):
        """
        Indicates if this game is closed (complete + all stat corrections are in).

        Return a boolean indicating if this instance's
        status field is equal to the STATUS_CLOSED value.
        """
        return self.status == self.STATUS_CLOSED

    def is_inprogress(self):
        """
        Indicates if this game is closed (complete + all stat corrections are in).

        Return a boolean indicating if this instance's
        status field is equal to the STATUS_CLOSED value.
        """
        return self.status == self.STATUS_INPROGRESS

    def __str__(self):
        return '<Game> %s | pk: %s | status: %s | start: %s | srid: %s' % (
            self.get_home_at_away_str(), self.pk, self.status, self.start, self.srid)

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
            # print('Game model self.get_dirty_fields() threw django.core.exceptions.ValidationError because of a datetime problem... skipping it for testing purposes')
            # print('debug>>>', 'game.start', str(self.start), 'game instance[', str( self ), ']' )
            changed_fields = {}

        super().save(*args, **kwargs)  # Call the "real" save() method.

        # check if status had been changed, now that the save() was successful
        if changed_fields.get('status', None):
            # send signal that the Game status has changed
            # print( 'game.status changed: sending signal' )
            GameStatusChangedSignal(self).send()
            # else:
            #     print( 'not sending signal - unchanged status')


class GameBoxscore(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    srid_game = models.CharField(max_length=64, null=False, unique=True, default=None,
                                 help_text='the sportsradar global id for the game')

    srid_home = models.CharField(max_length=64, null=False)
    srid_away = models.CharField(max_length=64, null=False)

    # the GFK to the home team
    home_type = models.ForeignKey(ContentType, related_name='%(app_label)s_%(class)s_home_team')
    home_id = models.PositiveIntegerField()
    home = GenericForeignKey('home_type', 'home_id')

    # the GFK to the away team
    away_type = models.ForeignKey(ContentType, related_name='%(app_label)s_%(class)s_away_team')
    away_id = models.PositiveIntegerField()
    away = GenericForeignKey('away_type', 'away_id')

    attendance = models.IntegerField(default=0, null=False)
    coverage = models.CharField(max_length=64, null=False, default='')
    status = models.CharField(max_length=64, null=False, default='')

    home_score = models.IntegerField(default=0, null=False)
    away_score = models.IntegerField(default=0, null=False)

    title = models.CharField(max_length=256, null=False, default='')

    # sport specific json for the scoring list,
    # if its mlb, its innings, if its nba its quarters...
    home_scoring_json = models.CharField(max_length=2048, null=False, default='')
    away_scoring_json = models.CharField(max_length=2048, null=False, default='')

    def to_json(self):
        return json.loads(serializers.serialize('json', [self]))[0]  # always only 1

    def __str__(self):
        return "<GameBoxscore> id: %s | srid_game: %s | status: %s | updated: %s" % (
            self.id,
            self.srid_game,
            self.status,
            self.updated,
        )

    class Meta:
        abstract = True


# TODO: Remove this model and all things related to it. We no longer get Injury data from
# Dataden, it comes from Swish in the form of Draftgroup.PlayerUpdates.
# /admin/draftgroup/playerupdate/
class Injury(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    #
    # "injury id" field:
    # for some sports this is the srid (nba/nhl), for sports like
    # mlb it is a standard injury type like "DL15". each sport
    # may use it for its own purposes, but must be consistent about its usage
    iid = models.CharField(max_length=128, unique=True, null=False,
                           help_text='custom injury id')

    player_type = models.ForeignKey(ContentType,
                                    related_name='%(app_label)s_%(class)s_injured_player')
    player_id = models.PositiveIntegerField()
    player = GenericForeignKey('player_type', 'player_id')

    status = models.CharField(max_length=32, default='')
    description = models.CharField(max_length=1024, default='')

    ddtimestamp = models.BigIntegerField(default=0, null=False,
                                         help_text='the time this injury update was parsed by dataden.' +
                                                   'this will be the same value for all objects that were in the feed on the last parse.')

    def get_serializer_class(self):
        """
        """
        raise Exception(
            'Injury get_serializer_class() error - inheriting model must override this method')

    class Meta:
        abstract = True


class Player(models.Model):
    STATUS_UNKNOWN = 'UNKNOWN'

    created = models.DateTimeField(auto_now_add=True)
    srid = models.CharField(max_length=64, unique=True, null=False,
                            help_text='the sportsradar global id')
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)

    # reference the position
    position = models.ForeignKey(Position, null=False,
                                 related_name='%(app_label)s_%(class)s_player_position')

    # the GFK to the Game
    injury_type = models.ForeignKey(ContentType, blank=True, null=True,
                                    related_name='%(app_label)s_%(class)s_players_injury')
    injury_id = models.PositiveIntegerField(blank=True, null=True)
    injury = GenericForeignKey('injury_type', 'injury_id')

    season_fppg = models.FloatField(null=False, default=0.0)

    lineup_nickname = models.CharField(
        max_length=64, default='', editable=True, blank=True,
        help_text='sets the the automatically generated name for lineups using this player')

    # True indicates this player is on a teams roster currently,
    # False indicates the player is NOT associated with a professional team!
    on_active_roster = models.BooleanField(default=True, null=False)

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
        return '<Player: %s %s | position: %s>' % (
            self.first_name, self.last_name, self.position)

    class Meta:
        abstract = True


class Team(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    srid = models.CharField(max_length=64, unique=True, null=False,
                            help_text='the sportsradar global id')

    srid_venue = models.CharField(max_length=64, null=False,
                                  help_text='the sportsradar global id')

    name = models.CharField(max_length=64, null=False, default='',
                            help_text='the team name, without the market/city. ie: "Lakers", or "Eagles"')
    alias = models.CharField(max_length=64, null=False, default='',
                             help_text='the abbreviation for the team, ie: for Boston Celtic alias == "BOS"')

    def __str__(self):
        if self.alias:
            return self.alias
        else:
            return self.name

    class Meta:
        abstract = True


class TeamStats(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    srid_game = models.CharField(max_length=64, null=False,
                                 help_text='the sportsradar global id for the game')
    srid_team = models.CharField(max_length=64, null=False,
                                 help_text='the sportsradar global id for the team')

    class Meta:
        abstract = True
        unique_together = ('srid_game', 'srid_team')


class PlayerStats(models.Model):
    FANTASY_POINTS_OVERRIDE = 'fantasy_points_override'

    SCORING_FIELDS = None  # override as a list in child classes, ie: ['rebounds','assists']
    SCORING_FIELDS_DONT_AVG = []

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    srid_game = models.CharField(max_length=64, null=False,
                                 help_text='the sportsradar global id for the game')
    srid_player = models.CharField(max_length=64, null=False,
                                   help_text='the sportsradar global id for the player')

    # the GFK to the Game
    game_type = models.ForeignKey(ContentType, related_name='%(app_label)s_%(class)s_sport_game')
    game_id = models.PositiveIntegerField()
    game = GenericForeignKey('game_type', 'game_id')

    # the GFK to the Player
    player_type = models.ForeignKey(ContentType,
                                    related_name='%(app_label)s_%(class)s_sport_player')
    player_id = models.PositiveIntegerField()
    player = GenericForeignKey('player_type', 'player_id')

    fantasy_points = models.FloatField(default=0.0, null=False)
    fp_change = models.FloatField(default=0.0, null=False)

    # reference the position FROM THE PLAYER WHEN THEY PLAYED THE GAME.
    #   ie: the players position might be different now! but we want
    #       the position they were when the played in the game!
    position = models.ForeignKey(Position, null=False,
                                 related_name='%(app_label)s_%(class)s_playerstats_position')

    field_id = 'id'
    field_fp = 'fp'
    field_pos = 'pos'

    def get_cache_token(self):
        """
        return a globally unique value for this object
        """
        return 'game_%s__player_%s' % (self.srid_game, self.srid_player)

    def set_cache_token(self):
        cache.set(self.get_cache_token(), 'exists')

    def get_scoring_fields(self):
        """
        get the fields relevant to scoring which we want
        to display in the gamelog/history/averages
        for the player.

        inheriting models of this class must set
        a list of fields they want to SCORING_FIELDS
        """
        if self.SCORING_FIELDS is None:
            raise Exception(
                'sports.PlayerStats.get_scoring_fields() must be overridden in child class!')
        return self.SCORING_FIELDS

    def to_json(self):
        return json.loads(serializers.serialize('json', [self]))[0]  # always only 1

    def to_score(self):
        return {
            'id': self.player_id,
            'fp': self.fantasy_points,
            'pos': self.position.name
        }

    class Meta:
        abstract = True
        unique_together = ('srid_player', 'srid_game')

    def __str__(self):
        return '<PlayerStats> game %s | player %s | fantasy_points %s | %s | last change (%s)' % (
            self.srid_game,
            self.srid_player,
            self.fantasy_points,
            str(self.player),
            str(self.fp_change))

    def save(self, *args, **kwargs):
        if self.FANTASY_POINTS_OVERRIDE in kwargs:
            # print( self.FANTASY_POINTS_OVERRIDE, True )
            self.fantasy_points = kwargs.get(self.FANTASY_POINTS_OVERRIDE)
        #
        super().save()


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
    srid_game = models.CharField(max_length=64, null=False,
                                 help_text='the sportsradar global id for the game this is associate with')

    # the GFK to the Game
    game_type = models.ForeignKey(ContentType, related_name='%(app_label)s_%(class)s_sport_game')
    game_id = models.PositiveIntegerField()
    game = GenericForeignKey('game_type', 'game_id')

    category = models.CharField(max_length=32, null=False, default='',
                                help_text='typically one of these: ["inning-half","quarter","period"]')
    sequence = models.IntegerField(default=0, null=False,
                                   help_text='an ordering of all GamePortions with the same srid_game')

    class Meta:
        abstract = True
        unique_together = ('srid_game', 'sequence')


class PbpDescription(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    # the GFK to the main pbp object
    pbp_type = models.ForeignKey(ContentType, related_name='%(app_label)s_%(class)s_pbpdesc_pbp')
    pbp_id = models.PositiveIntegerField()
    pbp = GenericForeignKey('pbp_type', 'pbp_id')

    portion_type = models.ForeignKey(ContentType,
                                     related_name='%(app_label)s_%(class)s_pbpdesc_portion')
    portion_id = models.PositiveIntegerField()
    portion = GenericForeignKey('portion_type', 'portion_id')

    idx = models.IntegerField(default=0, null=False)
    description = models.CharField(max_length=1024, null=False, default='')

    @property
    def srid_game(self):
        return self.pbp.srid_game

    @property
    def category(self):
        return self.portion.category

    @property
    def sequence(self):
        return self.portion.sequence

    def to_json(self):
        return {'idx': self.idx, 'd': self.description}

    class Meta:
        abstract = True


class Pbp(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    srid_game = models.CharField(max_length=64, null=False,
                                 help_text='the sportsradar global id for the game')

    # the GFK to the Game
    game_type = models.ForeignKey(ContentType, related_name='%(app_label)s_%(class)s_sport_game')
    game_id = models.PositiveIntegerField()
    game = GenericForeignKey('game_type', 'game_id')

    descriptions = GenericRelation(PbpDescription,
                                   content_type_field='pbp_type',
                                   object_id_field='pbp_id')

    class Meta:
        abstract = True


class TsxContent(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    srid = models.CharField(max_length=256, null=False,
                            help_text='use the right part url for the actual feed after splitting on "tsx". heres an example srid: "/news/2015/12/15/all.xml"')
    sport = models.CharField(max_length=32, null=False)

    def __str__(self):
        return '<Pbp> sport: %s | srid: %s | created:%s' % (
            self.sport, self.srid, str(self.created))

    class Meta:
        unique_together = ('srid', 'sport')


# class Content(models.Model):
#   - global id             # id of this item from sportradar
#   - provider content id   # id of this item from the provider
#   - created
#   - updated
#   - published         # not necessarily the 'created' time
#
#   - title             # string
#   - byline            # string
#   - dateline          # string
#   - credit            # string
#   - content           # long string
#
# class News(Content)
# class Injury(Content)
# class Transaction(Content)
#
# ---------
#
# class Ref(models.Model):
#   - sportsdata_id           # for NFL, might be "CIN", or a global id
#   - sportradar_id           # looks to alwasy be global id
#   - name                    # 'Cincinnati Bengal' or 'Pierce, Paul' (if player)
#   # - type                    # 'organization' | 'profile' determines if Team or Player
#   - GFK to [News|Injury|Transaction]Content
#
# class Team(Ref)
# class Player(Ref)
class AbstractTsxItem(models.Model):
    NEWS_FIELDS = [
        'title',
        'dateline',
    ]

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    srid = models.CharField(max_length=64, null=False,
                            help_text='the sportradar global id for the item')
    pcid = models.CharField(max_length=64, null=False,
                            help_text='the providers content id for this item')

    tsxcontent = models.ForeignKey(TsxContent, null=False,
                                   related_name='%(app_label)s_%(class)s_tsxcontent')

    content_created = models.DateTimeField(null=False)
    content_modified = models.DateTimeField(null=False)
    content_published = models.DateTimeField(null=False)

    title = models.CharField(max_length=256, null=False)
    byline = models.CharField(max_length=256, null=False)
    dateline = models.CharField(max_length=32, null=False)
    credit = models.CharField(max_length=128, null=False)
    content = models.CharField(max_length=1024 * 32, null=False)

    class Meta:
        abstract = True


class TsxNews(AbstractTsxItem):
    # TODO - needs to get the fields of Content, and also be abstract

    class Meta:
        abstract = True


class TsxInjury(AbstractTsxItem):
    # TODO - needs to get the fields of Content, and also be abstract

    class Meta:
        abstract = True


class TsxTransaction(AbstractTsxItem):
    # TODO - needs to get the fields of Content, and also be abstract

    class Meta:
        abstract = True


# class Ref(models.Model):
#   - sportsdata_id           # for NFL, might be "CIN", or a global id
#   - sportradar_id           # looks to alwasy be global id
#   - name                    # 'Cincinnati Bengal' or 'Pierce, Paul' (if player)
#   # - type                    # 'organization' | 'profile' determines if Team or Player
#   - GFK to [News|Injury|Transaction]Content
#
# class Team(Ref)
# class Player(Ref)

class AbstractTsxItemReference(models.Model):
    DEFAULT_DATETIME = parse("1999-01-01T12:00:00+00:00")  # one of the migrations needs this

    sportsdataid = models.CharField(max_length=64, null=False)
    sportradarid = models.CharField(max_length=64, null=False)

    name = models.CharField(max_length=128, null=False)

    # GenericForeignKey to be inherited by the child which should point to the Content
    tsxitem_type = models.ForeignKey(ContentType,
                                     related_name='%(app_label)s_%(class)s_tsxitem_tsxitemref')
    tsxitem_id = models.PositiveIntegerField()
    tsxitem = GenericForeignKey('tsxitem_type', 'tsxitem_id')

    content_published = models.DateTimeField(null=False, default=DEFAULT_DATETIME,
                                             help_text='the item ref is a GFK so also store the publish date here for ordering purposes.')

    class Meta:
        abstract = True
        ordering = ['-content_published']  # most recently published first


class TsxTeam(AbstractTsxItemReference):
    # TODO - make sure it get the TsxRef fields from inheriting

    class Meta:
        abstract = True


class TsxPlayer(AbstractTsxItemReference):
    # TODO - make sure it get the TsxRef fields from inheriting

    class Meta:
        abstract = True
