
class OverdraftException(Exception):
    def __init__(self, username):
       super().__init__(\
           "The user "+username+"  does not have the funds for this withdrawal")


class TaxInformationException(Exception):
    def __init__(self, username):
       super().__init__(\
           "The user "+username+"  does not the required tax information to perform this action.")

