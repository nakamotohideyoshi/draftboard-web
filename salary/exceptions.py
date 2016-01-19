#
# salary/exceptions.py

class NoPlayersAtRosterSpotException(Exception):
    def __init__(self):
        super().__init__(
           "Salary generation failed because there were no player to sum an average fppg at a roster spot" )

class NoPlayerStatsClassesFoundException(Exception): pass