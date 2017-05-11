class EmptySalaryPoolException(Exception):
    def __init__(self):
        super().__init__('There are no players in the salary pool.')


class NotEnoughGamesException(Exception):
    def __init__(self):
        super().__init__(
            'There are not enough scheduled games to create a draft group for start and end time range')


class NoGamesAtStartTimeException(Exception):
    def __init__(self):
        super().__init__('There are no actual games scheduled for the start time specified')


class FantasyPointsAlreadyFinalizedException(Exception): pass
