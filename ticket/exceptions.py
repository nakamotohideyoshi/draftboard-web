class InvalidTicketAmountException(Exception):
    def __init__(self, class_name, amount):
        super().__init__(\
           "In the class "+class_name+" the amount:"+ str(amount)+" is invalid ticket amount. Please refer to the TicketAmount model for the acceptable ticket sizes.")

class TicketAlreadyUsedException(Exception):
    def __init__(self, class_name, amount, pk):
        super().__init__(\
           "In the class "+class_name+" the ticket with the amount:"+ str(amount) +"  and id:"+str(pk)+"is invalid ticket amount. Please refer to the TicketAmount model for the acceptable ticket sizes.")

class UserDoesNotHaveTicketException(Exception):
    def __init__(self, class_name, amount, user):
        super().__init__(\
           "In the class "+class_name+" the user "+user.username+" does not have a ticket with the amount:"+ str(amount) )

