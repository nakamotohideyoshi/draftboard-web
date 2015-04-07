
class OverdraftException(Exception):
    def __init__(self, username):
       super(OverdraftException, self).__init__(\
           "The user "+username+"  does not have the funds for this withdrawal")