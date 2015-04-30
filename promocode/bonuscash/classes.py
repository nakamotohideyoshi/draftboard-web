
from transaction.constants import TransactionTypeConstants
from transaction.classes import AbstractTransaction
from transaction.models import TransactionType
from cash.exceptions import OverdraftException

import datetime
import promocode.bonuscash.models

from dfslog.classes import Logger, ErrorCodes

class BonusCashTransaction(AbstractTransaction):
    """
    Implements the :class:`transaction.classes.AbstractTransaction` class.
    This class handles transactions for BonusCash related things
    """
    def __init__(self, user):
        super().__init__(user)
        self.transaction_detail_class   = promocode.bonuscash.models.BonusCashTransactionDetail
        self.balance_class              = promocode.bonuscash.models.BonusCashBalance
        self.accountName                = "bonuscash"

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

    def withdraw(self, amount):
        """
        Creates a Withdraw from the users bonuscash account

        :param amount: The amount that is being removed from the account.
            This should be a positive number.

        :raises :class:`cash.exceptions.OverdraftException`: When
            the user does not have the amount for the withdraw
        :raises :class:`transaction.exceptions.AmountNegativeException`:
            When the amount is a negative number.
        """

        #
        # validates the amount is positive
        self.validate_amount(amount)

        #
        # Validate the user has the amount for the withdraw
        if not self.check_sufficient_funds(amount):
            raise OverdraftException(self.user.username)

        #
        # creates the transaction
        category = TransactionType.objects.get(pk=TransactionTypeConstants.BonusCashWithdraw.value)

        #
        # makes the amount negative because it is a withdrawal
        self.create(category, -amount)
        Logger.log(ErrorCodes.INFO,"Withdraw", self.user.username+" withdrew "+str(amount)+" "+self.accountName+" from their account.")

    def deposit(self, amount, category = None):
        """
        Creates a Deposit in the users bonuscash account

        :param user: The user the amount is being added to.
        :param amount: The amount being added to the account.

        :raises :class:`transaction.exceptions.AmountNegativeException`:
            When the amount is a negative number.
        """

        # validates the amount is positive
        self.validate_amount(amount)

        #
        # creates the transaction
        if(category == None):
            category = TransactionType.objects.get(pk=TransactionTypeConstants.BonusCashDeposit.value)
        self.create(category,amount)
        Logger.log(ErrorCodes.INFO, "Deposit", self.user.username+" deposited "+str(amount)+" "+self.accountName+" into their account.")

    def get_balance_string_formatted(self):
        """

        :return: the string representation of the bonuscash balance
            i.e. $5.50

        """
        bal = self.get_balance_amount()
        return '${:,.2f} '.format(bal) + self.accountName

