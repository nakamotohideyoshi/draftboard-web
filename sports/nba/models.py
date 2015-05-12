#
# sports/nba/models.py

from django.db import models
import sports.models

# Any classes that still have the abtract = True, just havent been migrated/implemented yet!

class Season( sports.models.Season ):
    class Meta:
        abstract = False

class Game( sports.models.Game ):
    class Meta:
        abstract = False

class GameBoxscore( sports.models.GameBoxscore ):
    class Meta:
        abstract = True # TODO

class Player( sports.models.Player ):
    class Meta:
        abstract = False

class Team( sports.models.Team ):
    class Meta:
        abstract = True # TODO

class PlayerStats( sports.models.PlayerStats ):
    points = models.FloatField(null=False, default=0.0)
    fouls = models.FloatField(null=False, default=0.0)
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