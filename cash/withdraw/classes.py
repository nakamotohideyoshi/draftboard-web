from . import models
from mysite.exceptions import IncorrectVariableTypeException, VariableNotSetException
from django.contrib.auth.models import User
from mysite.classes import  AbstractSiteUserClass
from account.classes import AccountInformation
from cash.classes import CashTransaction
from .constants import WithdrawStatusConstants
from .exceptions import WithdrawStatusException
from django.conf import settings
from cash.exceptions import  TaxInformationException, OverdraftException
from cash.tax.classes import TaxManager
from transaction.constants import TransactionTypeConstants
from transaction.models import TransactionType
from cash.withdraw.models import WithdrawStatus
#-------------------------------------------------------------------
#-------------------------------------------------------------------

class AbstractWithdraw( AbstractSiteUserClass ):
    """
    Abstract class for maintaining the Withdraw process
    """
    withdraw_class = None
    def __init__(self, user):
        """
        Initializes the variables
        :param user:
        :return:
        """
        super().__init__(user)
        self.withdraw_object = None
        self.validate_local_variables()

    def validate_local_variables(self):
        if(self.withdraw_class == None):
            raise VariableNotSetException(type(self).__name__,
                                          "withdraw_class")

        if(not issubclass(self.withdraw_class, models.Withdraw)):
            raise IncorrectVariableTypeException(type(self).__name__,
                                          "withdraw_class")
        return

    def validate_withdraw(self, amount):
        """
        Sets the standard withdraw data in the :class:`cash.withdraw.models.Withdraw`
        abstract model.

        """
        #
        # Checks to make sure we are not withdrawing more than we have
        ct= CashTransaction(self.user)
        balance = ct.get_balance_amount()
        if(balance < amount ):
            raise OverdraftException(self.user.username)


        #
        # Gets the profit for the year before the current withdrawal
        # and raises an exception if their tax information needs to
        # be collected.
        current_year_profit = ct.get_withdrawal_amount_current_year()
        if(current_year_profit + amount >= settings.DFS_CASH_WITHDRAWAL_AMOUNT_REQUEST_TAX_INFO):
            #
            # Checks to see if we collected tax information for the user
            tm = TaxManager(self.user)
            if(not tm.info_collected()):
                raise TaxInformationException(self.user.username)



    def update_status(self):
        pass


    def withdraw(self, amount):
        """
        This method creates a cash withdrawal transaction and the appropriate book
        keeping for allowing
        :param amount:
        :return:
        """
        if(self.withdraw_object == None):
            self.withdraw_object = self.withdraw_class()

        self.validate_withdraw(amount)

        #
        # Performs the transaction since everything has been validated
        # and saves the the transaction detail with the withdraw object.
        ct= CashTransaction(self.user)
        ct.withdraw(amount)
        self.withdraw_object.cash_transaction_detail = ct.transaction_detail
        self.withdraw_object.status = self.get_withdraw_status(WithdrawStatusConstants.Pending.value)

        self.withdraw_object.save()


        #
        # updates the status and pays out if possible
        self.update_status()

    def __check_status_pending(self):


        if(self.withdraw_object.status != self.get_withdraw_status(WithdrawStatusConstants.Pending.value)):
            print(self.withdraw_object.status.description)
            raise WithdrawStatusException(
                str(self.withdraw_object.pk),
                type(self.withdraw_object).__name__
            )

    def cancel(self, withdraw_pk, status_pk ):
        """
        Cancels a withdraw assuming the status is still pending. Also refunds
        the bad amount.
        :param withdraw_pk:
        :param status_pk:
        """
        self.withdraw_object = self.withdraw_class.objects.get(pk=withdraw_pk)
        self.__check_status_pending()
        self.withdraw_object.status = self.get_withdraw_status(status_pk)
        self.withdraw_object.save()

        #
        # Creates a new transaction for the refunded amount.
        category = TransactionType.objects.get(pk=TransactionTypeConstants.AdminCancelWithdraw.value)
        ct = CashTransaction(self.user)
        ct.deposit(abs(self.withdraw_object.cash_transaction_detail.amount), category)

    def payout(self, withdraw_pk):
        """
        Marks the check as paid by updating hte status to processed
        """
        self.withdraw_object = self.withdraw_class.objects.get(pk=withdraw_pk)

        self.__check_status_pending()


    def get_withdraw_status(self, status_pk):
        return models.WithdrawStatus.objects.get(pk=status_pk)

#-------------------------------------------------------------------
#-------------------------------------------------------------------

class PayPalWithdraw(AbstractWithdraw):
    """
    Class for interfacing with paypal. Allows the admin to process payouts
    and update the statuses of withdrawals.

    """
    def __init__(self, user):
        self.withdraw_class = models.PayPalWithdraw

        super().__init__(user)


    def validate_withdraw(self, amount):
        super().validate_withdraw(amount)

    def update_status(self):
        """
        Sets the status to Pending
        """
        super().update_status()
        if(self.withdraw_object.cash_transaction_detail.amount < settings.DFS_CASH_WITHDRAWAL_APPROVAL_REQ_AMOUNT):
            #
            # TODO payout automatically
            pass

        # paypalrestsdk.PAYOUT()

    def withdraw(self, amount, email):
        """
        :param amount:
        :param email: the PayPal email. This MUST be validated twice by the front end
            because it will automatically get paid out and once that is done, it
            cannot be undone.
        """
        self.withdraw_object =  models.PayPalWithdraw()
        self.withdraw_object.email = email
        super().withdraw(amount)

    def payout(self, withdraw_pk):
        """
        Pays out the user via PayPal
        """
        super().payout(withdraw_pk)
        self.withdraw_object = models.PayPalWithdraw.objects.get(pk=withdraw_pk)


#-------------------------------------------------------------------
#-------------------------------------------------------------------
class CheckWithdraw(AbstractWithdraw):
    def __init__(self, user):
        self.withdraw_class = models.CheckWithdraw
        super().__init__(user)


    def validate_withdraw(self, amount):
        """
        Validates the user has the proper mailing address.

        :raise :class:`account.exceptions.AccountInformationException`: When there are
            missing fields for the user's mailing address.
        """
        #
        # Validates the mailing address. Throws an exception
        # if the address is not validated
        account_information = AccountInformation(self.user)
        account_information.validate_mailing_address()

        #
        # Then call the super class's validation for balance and tax checks
        super().validate_withdraw(amount)

        #
        # sets the local variables in the withdraw object
        self.withdraw_object.fullname   = account_information.information.fullname
        self.withdraw_object.address1   = account_information.information.address1
        self.withdraw_object.address2   = account_information.information.address2
        self.withdraw_object.city       = account_information.information.city
        self.withdraw_object.state      = account_information.information.state
        self.withdraw_object.zipcode    = account_information.information.zipcode


    def payout(self, withdraw_pk, check_number):
        """
        Marks the check as paid by updating hte status to processed
        """
        super().payout(withdraw_pk)
        self.withdraw_object = models.CheckWithdraw.objects.get(pk=withdraw_pk)
        self.withdraw_object.check_number = check_number
        self.withdraw_object.status = self.get_withdraw_status(WithdrawStatusConstants.Processed.value)
        self.withdraw_object.save()


#-------------------------------------------------------------------
#-------------------------------------------------------------------
class ReviewWithdraw(AbstractWithdraw):
    def __init__(self, user):
        self.withdraw_class = models.ReviewWithdraw
        super().__init__(user)

    def get_pending_withdraws(self):
        """
        Gets the pending check and paypal transactions
        :return:
        """
        category = WithdrawStatusConstants.Processed.value
        return models.Withdraw.objects.filter(status=category)



