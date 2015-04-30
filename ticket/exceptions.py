class InvalidTicketAmountException(Exception):
    def __init__(self, class_name, amount):
        super().__init__(\
           "In the class "+class_name+" the amount:"+ amount +" is invalid ticket amount. Please refer to the TicketAmount model for the acceptable ticket sizes.")
nts_str)