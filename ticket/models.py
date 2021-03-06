from django.db import models
from transaction.models import Transaction, AbstractAmount
from django.contrib.auth.models import User
import ticket.classes

#
# the total buyin amount and description of the buyin/ticket.
# 10% rake is implied, but the text part of the tuple
# includes the contest contribution and rake amount
DEFAULT_TICKET_VALUES = [
    (1.00, '$0.90 + 0.10'),
    (2.00, '$1.80 + 0.20'),
    (5.00, '$4.50 + 0.50'),
    (10.00, '$9.00 + 1.00'),
    (20.00, '$18.00 + 2.00'),
    # 25.00,
    # 30.00,
    # 40.00,
    (50.00, '$45.00 + 5.00'),
    # (100.00,'$90.00 + 10.00'), # not for launch anyways!
    # 200.00,
    # 300.00,
    # 500.00,
    # 1000.00
]

#
# generate a list of tuples in the form:
# [
#     (9, '9 spots paid'),
#     (18, '18 spots paid'),
#     ...
# ]
DEFAULT_FLAT_TICKET_PRIZE_OPTIONS = 50
DEFAULT_FLAT_TICKET_NUM_PRIZES = [(x * 9, '%s spots paid' % (str(x * 9))) for x in
                                  range(1, DEFAULT_FLAT_TICKET_PRIZE_OPTIONS)]


class TicketAmount(AbstractAmount):
    """
    A unique master/template ticket for defining a ticket value.
    """
    created = models.DateTimeField(auto_now_add=True, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10, unique=True)

    def get_category(self):
        return 'ticket'

    def get_transaction_class(self):
        """
        return a class with which we can create an instance and make a deposit transaction
        """
        return ticket.classes.TicketManager

    def get_cash_value(self):
        return self.amount

    def __str__(self):
        return '%s | %s' % (self.__class__.__name__, self.amount)


class Ticket(models.Model):
    """
    Keeps track of the tickets for all the users.
    """
    #
    # Foreign Key to the Transaction that used this specific
    # Ticket. Null by default and on creation.
    updated = models.DateTimeField(auto_now=True)

    created = models.DateTimeField(auto_now_add=True, null=True)

    #
    # When a ticket is created, this points to the transaction
    # that creates it. The related_name='+' class makes it so that
    # there is no backwards relation on the Transaction table. Since
    # we have two pointers to the Transaction table.
    deposit_transaction = models.OneToOneField(Transaction, null=False, related_name='+')

    #
    # Keeps track of the last time this transaction detail was
    # modified. In theory it would be the time it was created
    # or the time it was used if it has been used.
    consume_transaction = models.OneToOneField(Transaction, null=True, related_name='+')
    user = models.ForeignKey(User)
    amount = models.ForeignKey(TicketAmount, null=False)

    def __str__(self):
        return '%s | %s value' % (self.__class__.__name__, self.amount)
