#from cash.models import CashBalance, CashTransactionDetail
import cash.models
from transaction.classes import AbstractTransaction
from transaction.models import TransactionType
from transaction.constants import TransactionTypeConstants
from cash.exceptions import OverdraftException
from dfslog.classes import Logger, ErrorCodes
class CashTransaction(AbstractTransaction):
    """
    Implements the :class:`transaction.classes.AbstractTransaction` class.
    This class handles all dealings with accounting for managing the cash
    finances.
    """
    def __init__(self, user):
        super().__init__(user)
        self.transaction_detail_class = cash.models.CashTransactionDetail
        self.balance_class = cash.models.CashBalance
        self.accountName = "cash"

    def check_sufficient_funds(self, amount):
        """
        Check to see if the user has enough funds
        :param amount: the amount to check against the user's account
        :return: True if the user has enough funds
        """
        cash_balance = self.get_balance_amount()
        if(cash_balance < amount):
            return False
        return True


    def withdraw(self, amount):
        """
        Creates a Withdraw in the user's Cash account.

        :param amount: The dollar amount that is being removed from the account.
            This should be a positive number.

        :raises :class:`cash.exceptions.OverdraftException`: When
            the user does not have enough cash for the withdrawal
        :raises :class:`transaction.exceptions.AmountNegativeException`:
            When the amount is a negative number.
        """

        #
        # validates the amount is positive
        self.validate_amount(amount)

        #
        # Validate the user has the funds for the withdrawal
        if(not self.check_sufficient_funds( amount)):
            raise OverdraftException(self.user.username)

        #
        #creates the transaction
        category = TransactionType.objects.get(pk=TransactionTypeConstants.CashWithdrawal.value)
        #
        # makes the amount negative because it is a withdrawal
        self.create(category,-amount)
        Logger.log(ErrorCodes.INFO,"Withdrawal", self.user.username+" withdrew $"+str(amount)+" from their cash account.")


    def deposit(self, amount):
        """
        Creates a Deposit in the user's Cash account.

        :param user: The user the cash is being added to.
        :param amount: The dollar amount that is being added to the account.

        :raises :class:`transaction.exceptions.AmountNegativeException`:
            When the amount is a negative number.
        """
        #
        # validates the amount is positive
        # validates the amount is positive
        self.validate_amount(amount)

        #
        #creates the transaction
        category = TransactionType.objects.get(pk=TransactionTypeConstants.CashDeposit.value)
        self.create(category,amount)
        Logger.log(ErrorCodes.INFO, "Deposit", self.user.username+" deposited $"+str(amount)+" into their cash account.")


    def get_balance_string_formatted(self):
        """

        :return: the string representation of the cash balance
            i.e. $5.50

        """
        bal = self.get_balance_amount()
        return '${:,.2f}'.format(bal)