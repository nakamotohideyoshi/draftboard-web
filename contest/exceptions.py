class ContestLineupMismatchedDraftGroupsException(Exception):
    def __init__(self):
        super().__init__(
           "Lineup cannot be submitted to Contest because of mismatched DraftGroup." )

class ContestIsInProgressOrClosedException(Exception):
    def __init__(self):
        super().__init__(
           "The contest is in Progress or Closed and cannot be entered." )

class ContestIsFullException(Exception):
    def __init__(self):
        super().__init__(
           "The contest is full." )

class ContestCouldNotEnterException(Exception):
    def __init__(self):
        super().__init__(
           "Could not enter contest. Please try again later." )

class ContestMaxEntriesReachedException(Exception):
    def __init__(self):
        super().__init__(
           "User cannot submit entry. Maximum Entries submitted" )

class ContestIsNotAcceptingLineupsException(Exception):
    def __init__(self):
        super().__init__(
           "The contest is not accepting lineups. Please try again later." )