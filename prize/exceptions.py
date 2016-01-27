class PrizeGenerationException(Exception):
    def __init__(self):
        super().__init__(
           "The prize structure could not be generated with the arguments supplied." )

class InvalidBuyinAndPrizePoolException(Exception):
    def __init__(self):
        super().__init__(
           "The prize pool must be evenly divisible by the buyin." )

class RakeIsNot10PercentException(Exception): pass

class NoMatchingTicketException(Exception): pass
