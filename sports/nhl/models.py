#
# sports/nhl/models.py

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
import sports.models

# Any classes that still have the abtract = True, just havent been migrated/implemented yet!

class Season( sports.models.Season ):
    class Meta:
        abstract = False

class Team( sports.models.Team ):

    srid_league   = models.CharField(max_length=64, null=False,
                            help_text='league sportsradar id')
    srid_conference   = models.CharField(max_length=64, null=False,
                            help_text='conference sportsradar id')
    srid_division   = models.CharField(max_length=64, null=False,
                            help_text='division sportsradar id')
    market      = models.CharField(max_length=64)

    class Meta:
        abstract = False

class Game( sports.models.Game ):
    """
    all we get from the inherited model is: 'srid', 'start' and 'status'
    """
    home = models.ForeignKey( Team, null=False, related_name='game_hometeam')
    srid_home   = models.CharField(max_length=64, null=False,
                                help_text='home team sportsradar global id')

    away = models.ForeignKey( Team, null=False, related_name='game_awayteam')
    srid_away   = models.CharField(max_length=64, null=False,
                                help_text='away team sportsradar global id')
    title       = models.CharField(max_length=128, null=True)

    class Meta:
        abstract = False

# class GameBoxscore( sports.models.GameBoxscore ):
#
#     # srid_home   = models.CharField(max_length=64, null=False)
#     home        = models.ForeignKey(Team, null=False, related_name='gameboxscore_home')
#     away        = models.ForeignKey(Team, null=False, related_name='gameboxscore_away')
#     # srid_away   = models.CharField(max_length=64, null=False)
#     #
#     # attendance  = models.IntegerField(default=0, null=False)
#     clock       = models.CharField(max_length=16, null=False, default='')
#     # coverage    = models.CharField(max_length=16, null=False, default='')
#     duration    = models.CharField(max_length=16, null=False, default='')
#     lead_changes = models.IntegerField(default=0, null=False)
#     quarter     = models.CharField(max_length=16, null=False, default='')
#     # status      = models.CharField(max_length=64, null=False, default='')
#     times_tied  = models.IntegerField(default=0, null=False)
#
#     class Meta:
#         abstract = False

class Player( sports.models.Player ):
    """
    inherited: 'srid', 'first_name', 'last_name'
    """
    team        = models.ForeignKey(Team, null=False)
    srid_team = models.CharField(max_length=64, null=False, default='')
    birth_place = models.CharField(max_length=64, null=False, default='')
    birthdate   = models.CharField(max_length=64, null=False, default='')
    college     = models.CharField(max_length=64, null=False, default='')
    experience  = models.FloatField(default=0.0, null=False)
    height      = models.FloatField(default=0.0, null=False, help_text='inches')
    weight      = models.FloatField(default=0.0, null=False, help_text='lbs')
    jersey_number = models.CharField(max_length=64, null=False, default='')

    position = models.CharField(max_length=64, null=False, default='')
    primary_position = models.CharField(max_length=64, null=False, default='')

    status = models.CharField(max_length=64, null=False, default='',
                help_text='roster status - ie: "ACT" means they are ON the roster. Not particularly active as in not-injured!')

    draft_pick = models.CharField(max_length=64, null=False, default='')
    draft_round = models.CharField(max_length=64, null=False, default='')
    draft_year = models.CharField(max_length=64, null=False, default='')
    srid_draft_team = models.CharField(max_length=64, null=False, default='')

    class Meta:
        abstract = False

class PlayerStats( sports.models.PlayerStats ):

    player  = models.ForeignKey(Player, null=False)
    game    = models.ForeignKey(Game, null=False)

    # TODO ... add the player stats !

    class Meta:
        abstract = False

class PlayerStatsSeason( sports.models.PlayerStatsSeason ):
    class Meta:
        abstract = True # TODO

class Injury( sports.models.Injury ):
    class Meta:
        abstract = True # TODO

class RosterPlayer( sports.models.RosterPlayer ):
    class Meta:
        abstract = True # TODO

class Venue( sports.models.Venue ):
    class Meta:
        abstract = True # TODO


