class IncorrectVariableTypeException(Exception):
    def __init__(self, class_name, variable_name):
       super().__init__(\
           "In the class "+class_name+" the variable "+ variable_name +" is the wrong class type.")
class VariableNotSetException(Exception):
    def __init__(self, class_name, variable_name):
       super().__init__(\
           "In the class "+class_name+" the variable "+ variable_name +" is null. It is required to be set.")

class AmountNegativeException(Exception):
    def __init__(self, class_name, variable_name):
       super().__init__(\
           "Incorrect usage of amount argument. The amount value must be a positive number.")

class AmountZeroException(Exception):
    def __init__(self, class_name, variable_name):
       super().__init__(\
           "Incorrect usage of amount argument. The amount value must be greater than 0.00.")
