class PrizeGenerationException(Exception):
    def __init__(self):
        super().__init__(
           "The prize structure could not be generated with the arguments supplied." )
