import datetime
from transaction.models import Transaction, TransactionDetail, Balance, TransactionType
from mysite.exceptions import VariableNotSetException, IncorrectVariableTypeException, AmountNegativeException, AmountZeroException
from django.contrib.auth.models import User
import decimal
from dfslog.classes import Logger, ErrorCodes
from mysite.classes import  AbstractSiteUserClass
from django.db.models import F
from django.db.transaction import atomic
from .tasks import send_deposit_receipt


class AbstractTransaction (AbstractSiteUserClass):
    """
    This class is to be implemented by any of the financial
    systems that require a transaction system. The class deals
    with modifying transaction histories and balances for a
    given currency type (points, dollars, bonus,etc).
    """
    def __init__(self, user):
        """
        :ivar transaction_detail: the variable must be set by the
            child class implementing
             :class:`transaction.classes.AbstractTransaction`.
             This variable should be a model that implements the
             model :class:`transaction.models.TransactionDetail`.

        :ivar transaction_detail: the variable must be set by the
            child class implementing
            :class:`transaction.classes.AbstractTransaction`.
             This variable should be a model that implements the
             model :class:`transaction.models.Balance`.

        :raises :class:`transaction.exceptions.VariableNotSetException`:
            When the transaction_detail and balance not set.

        """
        super().__init__(user)
        self.transaction_detail_class = None
        self.balance_class = None
        self.transaction_detail = None
        self.balance = None
        self.accountName = "accountNotNamed"
        self.transaction = None

    def validate_local_variables(self):
        if(self.transaction_detail_class == None):
            raise VariableNotSetException(type(self).__name__,
                                          "transaction_detail_class")
        if(self.balance_class == None):
            raise VariableNotSetException(type(self).__name__,
                                          "balance_class")
        if(not issubclass(self.transaction_detail_class, TransactionDetail)):
            raise IncorrectVariableTypeException(type(self).__name__,
                                          "transaction_detail_class")
        if(not issubclass(self.balance_class, Balance)):
            raise IncorrectVariableTypeException(type(self).__name__,
                                          "balance_class")

        return

    @atomic
    def create(self, category, amount, trans=None):
        """
        :param user: The user the transaction will be associated
            with.
        :param category: The category type. The category must be
            a TransactionType model.
        :param amount: the amount stored for the transaction.
        :param trans: the optional transaction to point the transaction to

        :raises :class:`transaction.exceptions.IncorrectVariableTypeException`:
            If the variables are not the correct types it will
            raise this exception.
        """
        #
        # makes sure the class has valid local variables.
        try:
            self.validate_local_variables()
        except Exception as e:
            raise e

        if(not isinstance(category, TransactionType)):
            raise IncorrectVariableTypeException(type(self).__name__,
                                          "category")
        if trans is None:
            self.transaction = Transaction(user=self.user, category=category)
            self.transaction.save()
        else:
            self.transaction = trans
        self.transaction_detail = self.transaction_detail_class()
        self.transaction_detail.amount = amount
        self.transaction_detail.transaction = self.transaction
        self.transaction_detail.user = self.user
        self.transaction_detail.save()
        transaction_type = self.transaction.category

        self.__update_balance(amount, transaction_type)

    def __update_balance(self, amount, transaction_type):
        """
        Updates the balance for a given user.
        """
        self.balance = self.__get_balance()

        self.balance.amount = F('amount') + amount

        self.balance.save()
        self.balance.refresh_from_db()

        #
        # keep in mind that changing this log messages could change a format
        # that we've been using to parse logs for very long time!
        msg = 'User[%s] Account[%s] balance is now: %s' % (self.user.username,
                                                           self.accountName,
                                                           self.balance.amount)

        Logger.log(ErrorCodes.INFO, "Balance Update", msg )
        transaction_date = datetime.datetime.now().strftime("%b %d %Y %H:%M%p")
        if self.user.email and transaction_type.name == 'deposit':
            send_deposit_receipt.delay(self, amount, transaction_date)

    def __get_balance(self):
        """
        Gets the balance for a given user.

        :param user: takes in the user that we need to
            create or retrieve the balance for.

        :return : an instance of
            :class:`transaction.models.Balance` model.
        """
        try:
            balance = self.balance_class.objects.get(user=self.user)
        except self.balance_class.DoesNotExist:
            #
            # If the balance does not exist we will create
            # and save a new balance for hte user.
            balance = self.balance_class()
            balance.user = self.user
            balance.transaction = None
            balance.amount = 0.00
            balance.save()
        return balance

    def get_balance_amount(self):
        """
        Gets the balance amount for a given user.

        :param user: takes in the user that we need to create or
            retrieve the balance for.

        :return :  returns the decimal value of the balance
        """
        self.balance = self.__get_balance()
        return self.balance.amount

    def validate_amount(self, amount):
        """
        Validates that amount is a positive number.


        :param amount: The amount that is being added to a transaction.

        :raises :class:`transaction.exceptions.AmountNegativeException`:
            When the amount is a negative number.
        """
        if(amount < 0.00):
            raise AmountNegativeException(type(self).__name__, amount)

class CanDeposit(object):
    pass