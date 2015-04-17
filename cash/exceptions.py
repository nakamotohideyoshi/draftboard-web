
class OverdraftException(Exception):
    def __init__(self, username):
       super(OverdraftException, self).__init__(\
           "The user "+username+"  does not have the funds for this withdrawal")

class IncorrectVariableTypeException(Exception):
    def __init__(self, class_name, variable_name):
       super(IncorrectVariableTypeException, self).__init__(\
           "In the class "+class_name+" the variable "+ variable_name +" is the wrong class type.")
