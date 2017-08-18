#
# lineup/exceptions.py


class LineupDoesNotMatchUser(Exception):

    def __init__(self):
        super().__init__(
            "The lineup does not match the User's account")


class LineupDoesNotMatchExistingEntryLineup(Exception):
    pass
    # def __init__(self, lineup_name):
    # super().__init__("Lineup must match the existing lineup '%s' for this Contest." % lineup_name)


class LineupInvalidRosterSpotException(Exception):

    def __init__(self):
        super().__init__(
            "The player selected cannot be drafted for the roster spot")


class InvalidLineupSizeException(Exception):

    def __init__(self):
        super().__init__(
            "You have not drafted enough players to make a lineup")


class PlayerDoesNotExistInDraftGroupException(Exception):

    def __init__(self, player_id, draftgroup_id):
        super().__init__(
            "The player ["+str(player_id)+"] does not exist in the draftgroup #"+str(draftgroup_id))


class InvalidLineupSalaryException(Exception):

    def __init__(self, username, salary, max_team_salary):
        super().__init__(
            "Please adjust your lineup so it fits under the %s salary cap." % max_team_salary)


class DuplicatePlayerException(Exception):

    def __init__(self):
        super().__init__(
            "You have a lineup with duplicate players")


class PlayerSwapGameStartedException(Exception):

    def __init__(self):
        super().__init__(
            "You cannot swap players that are already in games")


class EditLineupInProgressException(Exception):

    def __init__(self):
        super().__init__(
            "You are currently saving an edit. Please try again later.")


class LineupUnchangedException(Exception):

    def __init__(self):
        super().__init__(
            "The lineup you are trying to edit had not changes.")


class CreateLineupExpiredDraftgroupException(Exception):

    def __init__(self):
        super().__init__(
            "The draftgroup has expired, you cannot create a new lineup for this contest.")


class NotEnoughTeamsException(Exception):

    def __init__(self):
        super().__init__(
            "Please select players from more than one game.")


class DraftgroupLineupLimitExceeded(Exception):

    def __init__(self):
        super().__init__("You cannot create any more lineups for this sport.")
