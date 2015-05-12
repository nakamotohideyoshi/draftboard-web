
import sports.models

class Season( sports.models.Season ):
    class Meta:
        abstract = False

class Game( sports.models.Game ):
    class Meta:
        abstract = False

class GameBoxscore( sports.models.GameBoxscore ):
    class Meta:
        abstract = False

class Player( sports.models.Player ):
    class Meta:
        abstract = False

class Team( sports.models.Team ):
    class Meta:
        abstract = False

class PlayerStats( sports.models.PlayerStats ):
    class Meta:
        abstract = False

class PlayerStatsSeason( sports.models.PlayerStatsSeason ):
    class Meta:
        abstract = False

class Injury( sports.models.Injury ):
    class Meta:
        abstract = False

class RosterPlayer( sports.models.RosterPlayer ):
    class Meta:
        abstract = False

class Venue( sports.models.Venue ):
    class Meta:
        abstract = False