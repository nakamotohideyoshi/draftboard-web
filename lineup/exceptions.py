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

class PlayerDoesNotExistInDraftGroupException(Exception):
    def __init__(self, player_id, draftgroup_id):
        super().__init__(
           "The player ["+str(player_id)+"] does not exist in the draftgroup #"+str(draftgroup_id))


class InvalidLineupSalaryException(Exception):
    def __init__(self, username, salary, max_team_salary):
        super().__init__(
           "The User["+username+"]'s salary for the lineup was:"+str(salary)+
           " but it was expected to be less than:"+str(max_team_salary))

class DuplicatePlayerException(Exception):
    def __init__(self):
        super().__init__(
           "You have a lineup with duplicate players" )