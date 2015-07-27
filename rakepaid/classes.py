import fpp.models

from transaction.constants import TransactionTypeConstants
from transaction.classes import AbstractTransaction
from transaction.models import TransactionType
from .exceptions import WithdrawRakepaidException
from .models import RakepaidBalance, RakepaidTransactionDetail

from dfslog.classes import Logger, ErrorCodes

class RakepaidTransaction(AbstractTransaction):
    """
    Implements the :class:`transaction.classes.AbstractTransaction` class.
    This class handles all dealings with accounting for managing the rake paid
    of the user
    """
    def __init__(self, user):
        super().__init__(user)
        self.transaction_detail_class = RakepaidTransactionDetail
        self.balance_class = RakepaidBalance
        self.accountName = "rakepaid"

    def check_sufficient_funds(self, amount):
        """
        Check to see if the user has at least this amount
        :param amount: the amount to check against the user's account
        :return: True if the user has the amount available
        """
        balance = self.get_balance_amount()
        if(balance < amount):
            return False
        return True

    def withdraw(self, amount, trans=None):
        """
        throws an exception if called. You should not be able to withdraw
        from the Rakepaid table
        :raises:
        """
        raise WithdrawRakepaidException()

    def deposit(self, amount, category=None, trans=None):
        """
        Creates a Deposit in the users FPP account

        :param user: The user the amount is being added to.
        :param amount: The amount being added to the account.
        :param trans: the optional transaction to point the transaction to


        :raises :class:`transaction.exceptions.AmountNegativeException`:
            When the amount is a negative number.
        """

        # validates the amount is positive
        self.validate_amount(amount)

        #
        # creates the transaction
        if(category == None):
            category = TransactionType.objects.get(pk=TransactionTypeConstants.CashDeposit.value)
        self.create(category,amount, trans)
        Logger.log(ErrorCodes.INFO, "Rakepaid Deposit", self.user.username+" deposited $"+str(amount)+" into their account.")

    def get_balance_string_formatted(self):
        """

        :return: the string representation of the fpp balance
            i.e. $5.50

        """
        bal = self.get_balance_amount()
        return '{:,.0f} FPP'.format(bal)

