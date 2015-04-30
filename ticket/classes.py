from transaction.classes import AbstractTransaction
from transaction.constants import TransactionTypeConstants
from transaction.models import TransactionType, Transaction
from .models import Ticket, TicketAmount
from mysite.classes import  AbstractSiteUserClass
from mysite.exceptions import AmountZeroException, AmountNegativeException, TooManyArgumentsException, TooLittleArgumentsException, IncorrectVariableTypeException
class TicketManager(AbstractSiteUserClass):
    """
    Manages the ticket accounts for a given user. Each ticket
    is createed via the deposit method and then used via the
    consume method.
    """
    def __init__(self, user):
        super().__init__(user)
        self.transaction = None
        self.ticket = None

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

        return TicketAmount.objects.get(amount = amount)
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
        self.ticket = Ticket()
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
        :param amount: The
        :param ticket_obj: The :class:`ticket.models.Ticket` model object.
        :param transaction_obj: The :class:`transaction.models.Transaction`
            model object. If not set it will create one and then make
            the reference.
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
        # TODO get the tickets that are not consumed and throw and
        # exception if there are no tickets for the given user.

        #
        # TODO
#
# ●	@override __update_balance ⇒ need to figure out a way to do this. I want at the very least for __update_balance to be protected. We don’t want this public. This has to be modified to do the proper accounting.
# ●	deposit(amount)
# ●	consume(amount =0, ticket_transaction_pk= None) ⇒ can take one or the other. If both are given throw an exception. This should update the balance and set the transaction_used in the TicketTransactionDetail model.
# ○	Exceptions
# ■	general
# ●	No tickets
# ●	amount=0 and ticket_transaction_pk = None
# ●	amount >0 and ticket_transaction_pk != None
# ■	amount
# ●	doesnt match any existing tickets
# ■	ticket_transaction_pk
# ●	if transaction_used != None


