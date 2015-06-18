from django.db import models
from transaction.models import Transaction, AbstractAmount
from django.contrib.auth.models import User
import ticket.classes

DEFAULT_TICKET_VALUES = [
    5.00,
    10.00,
    20.00,
    50.00,
    100.00,
    200.00,
    500.00
]

class TicketAmount(AbstractAmount):
    """
    A unique master/template ticket for defining a ticket value.
    """
    created  = models.DateTimeField(auto_now_add=True, null=True)
    amount   = models.DecimalField(decimal_places=2, max_digits=10, unique=True)

    def get_transaction_class(self):
        """
        return a class with which we can create an instance and make a deposit transaction
        """
        return ticket.classes.TicketManager

    def __str__(self):
        return '%s | %s' % (self.__class__.__name__, self.amount)

class Ticket(models.Model):
    """
    Keeps track of the tickets for all the users.
    """
    #
    # Foreign Key to the Transaction that used this specific
    # Ticket. Null by default and on creation.
    updated             = models.DateTimeField(auto_now=True)

    created             = models.DateTimeField(auto_now_add=True, null=True)

    #
    # When a ticket is created, this points to the transaction
    # that creates it. The related_name='+' class makes it so that
    # there is no backwards relation on the Transaction table. Since
    # we have two pointers to the Transaction table.
    deposit_transaction =  models.OneToOneField( Transaction , null=False, related_name='+')

    #
    # Keeps track of the last time this transaction detail was
    # modified. In theory it would be the time it was created
    # or the time it was used if it has been used.
    consume_transaction = models.OneToOneField( Transaction , null=True, related_name='+' )
    user                = models.ForeignKey( User )
    amount              = models.ForeignKey( TicketAmount, null=False )

    def __str__(self):
        return '%s | %s value' % (self.__class__.__name__, str(self.amount))


