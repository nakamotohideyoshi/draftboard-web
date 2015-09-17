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
        super().__init__( "team class for %s not found" % sport_name )

class GameBoxscoreClassNotFoundException(Exception):
    def __init__(self, class_name, sport_name):
        super().__init__( "GameBoxscore class for %s not found" % sport_name )

class PbpDescriptionClassNotFoundException(Exception):
    def __init__(self, class_name, sport_name):
        super().__init__( "PbpDescription class for %s not found" % sport_name )
