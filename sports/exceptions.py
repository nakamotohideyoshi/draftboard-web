#
# sports/exceptions.py

class SportNameException(Exception):
    def __init__(self, class_name, sport_name):
        super().__init__(
           "The sport: "+sport_name+" does not exist" )

class SiteSportWithNameDoesNotExistException(Exception):
    def __init__(self, class_name, sport_name):
        super().__init__( "The string name: "+sport_name+" does not match an existing SiteSport instance" )

class GameClassNotFoundException(Exception):
    def __init__(self, class_name, sport_name):
        super().__init__( "game class for %s not found" % sport_name )

class TeamClassNotFoundException(Exception):
    def __init__(self, class_name, sport_name):
        super().__init__( "Team class for %s not found" % sport_name )

class GameBoxscoreClassNotFoundException(Exception):
    def __init__(self, class_name, sport_name):
        super().__init__( "GameBoxscore class for %s not found" % sport_name )

class SeasonClassNotFoundException(Exception):
    def __init__(self, class_name, sport_name):
        super().__init__( "Season class for %s not found" % sport_name )

class PbpDescriptionClassNotFoundException(Exception):
    def __init__(self, class_name, sport_name):
        super().__init__( "PbpDescription class for %s not found" % sport_name )

class TeamSerializerClassNotFoundException(Exception):
    def __init__(self, class_name, sport_name):
        super().__init__( "Team Serializer class for %s not found" % sport_name )

class InjuryClassNotFoundException(Exception):
    def __init__(self, class_name, sport_name):
        super().__init__( "Injury class for %s not found" % sport_name )

class InjurySerializerClassNotFoundException(Exception):
    def __init__(self, class_name, sport_name):
        super().__init__( "Injury Serializer class for %s not found" % sport_name )

class PlayerClassNotFoundException(Exception):
    def __init__(self, class_name, sport_name):
        super().__init__( "Player class for %s not found" % sport_name )

class PlayerSerializerClassNotFoundException(Exception):
    def __init__(self, class_name, sport_name):
        super().__init__( "Player Serializer class for %s not found" % sport_name )

# GameSerializerClassNotFoundException
class GameSerializerClassNotFoundException(Exception):
    def __init__(self, class_name, sport_name):
        super().__init__( "Game Serializer class for %s not found" % sport_name )

# BoxscoreSerializerClassNotFoundException
class BoxscoreSerializerClassNotFoundException(Exception):
    def __init__(self, class_name, sport_name):
        super().__init__( "Boxscore Serializer class for %s not found" % sport_name )

class PlayerHistorySerializerClassNotFoundException(Exception):
    def __init__(self, class_name, sport_name):
        super().__init__( "PlayerHistory Serializer class for %s not found" % sport_name )

class TsxModelClassNotFoundException(Exception):
    """
    Intended usage:

        >>> msg = 'No sports.%s.models modelclass found named [%s] with parent [%s]' % (sport, model_name, parent_model_class)
        >>> raise TsxModelClassNotFoundException(msg)

    """
    pass

class TsxSerializerClassNotFoundException(Exception): pass

class PlayerNewsSerializerClassNotFoundException(Exception):
    def __init__(self, class_name, sport_name):
        super().__init__( "PlayerNewsSerializer class for %s not found" % sport_name )