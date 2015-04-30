
class AccountInformationException(Exception):
    def __init__(self, username, missing_fields):
       super().__init__(\
           "The user "+username+"  does not have the following Information fields: "+missing_fields)

