from transaction.classes import AbstractTransaction
from transaction.constants import TransactionTypeConstants
from transaction.models import TransactionType, Transaction
#from .models import Ticket, TicketAmount
import ticket.models # transaction.models.
from mysite.classes import  AbstractSiteUserClass
from mysite.exceptions import AmountZeroException, AmountNegativeException, TooManyArgumentsException, TooLittleArgumentsException, IncorrectVariableTypeException
from .exceptions import  InvalidTicketAmountException, TicketAlreadyUsedException, UserDoesNotHaveTicketException

class TicketManager(AbstractSiteUserClass):
    """
    Manages the ticket accounts for a given user. Each ticket
    is created via the deposit method and then used via the
    consume method.
    """
    def __init__(self, user):
        super().__init__(user)
        self.transaction = None
        self.ticket = None

    def create_default_ticket_amounts():
        """
        Create the default TicketAmounts if they do not alrady exist
        """
        for amt in ticket.models.DEFAULT_TICKET_VALUES:
            try:
                ta = ticket.models.TicketAmount.objects.get( amount = amt )
            except ticket.models.TicketAmount.DoesNotExist:
                ta = ticket.models.TicketAmount()
                ta.amount = amt
                ta.save()
            print(str(ta))
    create_default_ticket_amounts = staticmethod( create_default_ticket_amounts )

    def __get_ticket_amount(self, amount):
        """
        Validates and gets  the amount.

        :param amount: the amount that we are looking for the ticket.
        :return: the model :class:`ticket.models.TicketAmount`.
        :raise :class:`mysite.exceptions.AmountZeroException`:
        :raise :class:`mysite.exceptions.AmountNegativeException`:
        :raise :class:`ticket.models.TicketAmount.DoesNotExist`:

        """
        if(amount == 0):
            raise AmountZeroException(type(self).__name__, 'amount')

        if(amount < 0 ):
            raise AmountNegativeException(type(self).__name__, 'amount')

        return ticket.models.TicketAmount.objects.get(amount = amount)

    def __get_deposit_category(self):
        """
        Gets the deposit ticket category for the Transaction
        :return: category
        """
        return TransactionType.objects.get(
            pk=TransactionTypeConstants.TicketDeposit.value
        )
    def __get_consume_category(self):
        """
        Gets the deposit ticket category for the Transaction
        :return: category
        """
        return TransactionType.objects.get(
            pk=TransactionTypeConstants.TicketConsume.value
        )
    def deposit(self, amount, transaction_obj=None):
        """
        Deposits a ticket for a given amount into the
        ticket system for a given user. .

        :param amount: the dollar value of the ticket being
            created.
        :raise :class:`mysite.exceptions.AmountZeroException`: if
            the amount is 0.
        :raise :class:`mysite.exceptions.AmounNegativeException`:
            if the amount argument is less than 0.

        """
        ta = self.__get_ticket_amount(amount)

        #
        # creates a Transaction if it does not exists
        if(transaction_obj != None):
            #
            # Validates it is trulya Transaction Object
            if(not isinstance(transaction_obj, Transaction)):
                raise IncorrectVariableTypeException(
                    type(self).__name__,
                    "transaction_obj"
                )
            self.transaction = transaction_obj
        else:
            self.transaction = Transaction(
                user=self.user,
                category=self.__get_deposit_category()
            )
            self.transaction.save()

        #
        # creates the ticket
        self.ticket = ticket.models.Ticket()
        self.ticket.deposit_transaction = self.transaction
        self.ticket.user = self.user
        self.ticket.amount = ta
        self.ticket.save()


    def consume(self, amount = None, ticket_obj = None, transaction_obj = None):
        """
        Uses one of the tickets and points the ticket to the transaction.
        This consume method can only take one of the following arguments:
            * amount
            * ticket
        :param amount: The dollar amount (decimal) that the user wishes to use
            for a ticket.
        :param ticket_obj: The :class:`ticket.models.Ticket` model object.
        :param transaction_obj: The :class:`transaction.models.Transaction`
            model object. If not set it will create one and then make
            the reference.
        :raise :class:`mysite.exceptions.IncorrectVariableTypeException`:
            if arguments are the wrong types
        :raise :class:`ticket.exceptions.InvalidTicketAmountException`:
            if the ticket amount is an amount not in the TicketAmount table.
        :raise :class:`ticket.exceptions.TicketAlreadyUsedException`:
            if the ticket object passed has already been consumed.
        :raise :class:`ticket.exceptions.UserDoesNotHaveTicketException`:
            if the user does not have a ticket with the amount provided.

        """
        #---------------------------------------------------------------
        #---------------------------------------------------------------
        # Validation of the arguments before we attempt to consume

        #
        # Make sure that amount and ticket_obj are not both set.
        if(amount != None and ticket_obj != None):
            raise TooManyArgumentsException(
                type(self).__name__,
                ['amount', 'ticket_obj']
            )

        #
        # Makes sure that amount or ticket is set.
        if(amount == None and ticket_obj == None):
            raise TooLittleArgumentsException(
                type(self).__name__,
                ['amount', 'ticket_obj']
            )



        #
        # Gets the tickets that are not consumed and throw and
        # exception if there are no tickets for the given user.
        if(amount != None):

            #
            # Gets the amount from the pre-defined Ticket Amounts
            amount_obj = self.__get_ticket_amount(amount)


            #
            # Checks the ticket
            tickets = ticket.models.Ticket.objects.filter(
                amount = amount_obj,
                user = self.user,
                consume_transaction = None
            ).order_by('-created')


            if(len(tickets) == 0):
                raise UserDoesNotHaveTicketException(
                    type(self).__name__,
                    amount,
                    self.user
                )
            self.ticket = tickets[0]

        else:
            if(not isinstance(ticket_obj, ticket.models.Ticket)):
                raise IncorrectVariableTypeException(type(self).__name__,
                                          "ticket_obj")
            self.ticket = ticket_obj

        #
        # Makes sure that the ticket has not been consumed, and throws
        # an exception if has been.
        if(self.ticket.consume_transaction != None):
            raise TicketAlreadyUsedException(
                type(self).__name__,
                amount,
                self.ticket.pk
            )

        #
        # Creates a new transaction if it was not supplied by the
        # consume functionality.
        if(transaction_obj == None):
            self.transaction = ticket.models.Transaction(
                user=self.user,
                category=self.__get_consume_category()
            )
            self.transaction.save()
        else:
            #
            # check to make sure the transaction object is in fact
            # a transaction
            if(not isinstance(transaction_obj, Transaction)):
                raise IncorrectVariableTypeException(type(self).__name__,
                                          "transaction_obj")
            self.transaction = transaction_obj
        #
        # Sets the ticket's consume_transaction field so that
        # it will be marked as used.
        self.ticket.consume_transaction = self.transaction
        self.ticket.save()



    def get_available_tickets(self):
        return ticket.models.Ticket.objects.filter(
                user = self.user,
                consume_transaction = None
            ).order_by('-created')
