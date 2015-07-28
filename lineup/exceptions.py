class LineupDoesNotMatchUser(Exception):
    def __init__(self):
        super().__init__(
           "The lineup does not match the User's account" )

class LineupInvalidRosterSpotException(Exception):
    def __init__(self):
        super().__init__(
           "The player selected cannot be drafted for the roster spot" )

class InvalidLineupSizeException(Exception):
    def __init__(self):
        super().__init__(
           "You have not drafted enough players to make a lineup" )
