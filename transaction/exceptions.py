

class VariableNotSetException(Exception):
    def __init__(self, class_name, variable_name):
       super(VariableNotSetException, self).__init__(\
           "In the class "+class_name+" the variable "+ variable_name +" is null. It is required to be set.")

class IncorrectVariableTypeException(Exception):
    def __init__(self, class_name, variable_name):
       super(IncorrectVariableTypeException, self).__init__(\
           "In the class "+class_name+" the variable "+ variable_name +" is the wrong class type.")

class AmountNegativeException(Exception):
    def __init__(self, class_name, variable_name):
       super(AmountNegativeException, self).__init__(\
           "Incorrect usage of amount argument. The amount value must be a positive number.")

class AmountZeroException(Exception):
    def __init__(self, class_name, variable_name):
       super(AmountZeroException, self).__init__(\
           "Incorrect usage of amount argument. The amount value must be greater than 0.00.")
