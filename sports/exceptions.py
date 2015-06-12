class SportNameException(Exception):
    def __init__(self, sport_name):
        super().__init__(
           "The sport: "+sport_name+" does not exist" )
