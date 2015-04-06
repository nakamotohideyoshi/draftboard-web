

class VariableNotSetException(Exception):
    def __init__(self, class_name, variable_name):
       super(VariableNotSetException, self).__init__(\
           "In the class "+class_name+" the variable "+ variable_name +" is null. It is required to be set.")

class IncorrectVariableTypeException(Exception):
    def __init__(self, class_name, variable_name):
       super(IncorrectVariableTypeException, self).__init__(\
           "In the class "+class_name+" the variable "+ variable_name +" is the wrong class type.")

