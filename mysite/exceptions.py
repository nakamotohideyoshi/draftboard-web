class IncorrectVariableTypeException(Exception):
    def __init__(self, class_name, variable_name):
        super().__init__(
           "In the class "+class_name+" the variable "+ variable_name +" is the wrong class type." )

class VariableNotSetException(Exception):
    def __init__(self, class_name, variable_name):
        super().__init__(\
           "In the class "+class_name+" the variable "+ variable_name +" is null. It is required to be set.")

class AmountNegativeException(Exception):
    def __init__(self, class_name, variable_name):
        super().__init__(\
           "Incorrect usage of "+str(variable_name)+"  argument. The amount value must be a positive number.")


class AmountZeroException(Exception):
    def __init__(self, class_name, variable_name):
        super().__init__(\
           "Incorrect usage of amount argument. The amount value must be greater than 0.00.")

class InvalidArgumentException(Exception):
    def __init__(self, class_name, variable_name):
        super().__init__(\
           "Invalid argument.")

class AmbiguousArgumentException(Exception):
    def __init__(self, class_name, variable_name):
        super().__init__("Ambiguous argument.")

class AdminDoNotDeleteException(Exception):
    def __init__(self, class_name, variable_name):
        super().__init__("These objects are not allowed to be deleted!")

class MethodNotOverriddenInChildException(Exception):
    def __init__(self, class_name, variable_name):
        super().__init__("Method must be overridden in the child class!")

class UnimplementedException(Exception):
    def __init__(self, class_name, variable_name):
        super().__init__('(Tell a developer) - this method is not implemented.')

class MaxCurrentWithdrawsException(Exception):
    def __init__(self, class_name, variable_name):
        super().__init__('You may not currently create any new withdraws.')

class CashoutWithdrawOutOfRangeException(Exception):
    def __init__(self, class_name, variable_name):
       super().__init__('Cashout amount out of range.')

class CheckWithdrawCheckNumberRequiredException(Exception):
    def __init__(self, class_name, variable_name):
       super().__init__('You need to save the check number before you process the cashout')

class TooManyArgumentsException(Exception):
    def __init__(self, class_name, arguments_arr):
        arguments_str = ', '.join(arguments_arr)
        super().__init__(\
           "In the class "+class_name+", too many arguments were used. You can only chose one of the following arguments: "+arguments_str)

class TooLittleArgumentsException(Exception):
    def __init__(self, class_name, arguments_arr):
        arguments_str = ', '.join(arguments_arr)
        super().__init__(\
           "In the class "+class_name+", too little arguments were used. You must set one of the following arguments: "+arguments_str)

class WithdrawCalledTwiceException(Exception):
    def __init__(self, class_name, variable_name):
       super().__init__('Withdraw can not be called more than once the object')

class InvalidPromoCodeException(Exception):
    def __init__(self, class_name, variable_name):
       super().__init__('That promo code does not exist')

class PromoCodeAlreadyUsedException(Exception):
    def __init__(self, class_name, variable_name):
       super().__init__('The promo code has already been used.')

class PromoCodeExpiredException(Exception):
    def __init__(self, class_name, variable_name):
       super().__init__('The promo code is no longer valid.')

class CanNotRemovePromoCodeException(Exception):
    def __init__(self, class_name, variable_name):
       super().__init__('The promo code does not exist for the user.')

class NullModelValuesException(Exception):
    def __init__(self, class_name, model_name):
       super().__init__('In the '+class_name+' the model has null values for the object '+ model_name)

class InvalidSiteSportTypeException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class InvalidStartTypeException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class InvalidEndTypeException(Exception):
   def __init__(self, msg):
        super().__init__(msg)

class SalaryPoolException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class NoGamesInRangeException(Exception):
    def __init__(self, msg):
        super().__init__(msg)