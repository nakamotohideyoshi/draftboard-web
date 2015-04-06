from transaction.models import Transaction, TransactionDetail, Balance, TransactionType
from transaction.exceptions import VariableNotSetException, IncorrectVariableTypeException
from django.contrib.auth.models import User
import decimal
class AbstractTransaction (object):
    """
    This class is to be implemented by any of the financial
    systems that require a transaction system. The class deals
    with modifying transaction histories and balances for a
    given currency type (points, dollars, bonus,etc).
    """
    def __init__(self):
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

        :raises :class:`transaction.exceptions.VaiableNotSetException`:
            When the transaction_detail and balance not set.

        """
        self.transaction_detail_class = None
        self.balance_class = None
        self.transaction_detail = None
        self.balance = None

    def validate_local_variables(self):
        if(self.transaction_detail_class == None):
            raise VariableNotSetException(type(self).__name__,
                                          "transaction_detail_class")
        if(self.balance_class == None):
            raise VariableNotSetException(type(self).__name__,
                                          "balance_class")
        val = issubclass(self.transaction_detail_class, TransactionDetail)
        if(not issubclass(self.transaction_detail_class, TransactionDetail)):
            raise IncorrectVariableTypeException(type(self).__name__,
                                          "transaction_detail_class")
        if(not issubclass(self.balance_class, Balance)):
            raise IncorrectVariableTypeException(type(self).__name__,
                                          "balance_class")
        return
    def create(self, user, category, amount):
        """

        :param user: The user the transaction will be associated
            with.
        :param category: The category type. The category must be
            a TransactionType model.
        :param amount: the amount stored for the transaction.

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
        #
        # Validate that user and category are proper types
        if(not isinstance(user, User)):
            raise IncorrectVariableTypeException(type(self).__name__,
                                          "user")
        if(not isinstance(category, TransactionType)):
            raise IncorrectVariableTypeException(type(self).__name__,
                                          "category")

        transaction = Transaction(user=user, category=category)
        transaction.save()
        self.transaction_detail = self.transaction_detail_class()
        self.transaction_detail.amount = amount
        self.transaction_detail.transaction = transaction
        self.transaction_detail.user = user
        self.transaction_detail.save()

        self.__update_balance(user)

       # self.__updateBalance(user)

    def __update_balance(self, user):
        """
        Updates the balance for a given user.
        :param user: the user associated with the balance update
        """
        self.balance =  self.__get_balance(user)

        if(self.balance.transaction == None):
            transactions = self.transaction_detail_class.objects.filter(user=user)
        else:
            transactions = self.transaction_detail_class.objects.filter(
                                        user=user,
                                        pk__gt= self.balance.transaction.pk)
            transactions = transactions.order_by('pk')
        if(transactions != []):
            #
            # Sums the transactions for the given user to come up
            # with the new balance
            for transaction in transactions:
                self.balance.amount = decimal.Decimal(self.balance.amount) + decimal.Decimal(transaction.amount)
            #
            # sets the pointer to in balance to the last transaction
            # in the transaction list
            self.balance.transaction = transactions[len(transactions)-1]
            self.balance.save()








    def __get_balance(self, user):
        """
        Gets the balance for a given user.
        :param user: takes in the user that we need to
            create or retrieve the balance for.
        :return balance: returns an instance of
            :class:`transaction.models.Balance` model.
        """
        try:
            balance = self.balance_class.objects.get(user=user)
        except self.balance_class.DoesNotExist:
            #
            # If the balance does not exist we will create
            # and save a new balance for hte user.
            balance = self.balance_class()
            balance.user = user
            balance.transaction = None
            balance.amount=0.00
            balance.save()
        return balance

