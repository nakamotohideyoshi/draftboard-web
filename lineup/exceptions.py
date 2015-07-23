class LineupDoesNotMatchUser(Exception):
    def __init__(self):
        super().__init__(
           "The lineup does not match the User's account" )

