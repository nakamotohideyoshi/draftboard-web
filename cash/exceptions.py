
class OverdraftException(Exception):

    def __init__(self, username):
        super().__init__(
            "You do not have the funds for this withdrawal")


class TaxInformationException(Exception):

    def __init__(self, username):
        super().__init__(
            "You have not provided the required tax information to perform this action.")
