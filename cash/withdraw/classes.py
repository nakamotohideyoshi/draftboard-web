from . import models
from mysite.exceptions import IncorrectVariableTypeException, VariableNotSetException
from django.contrib.auth.models import User
from mysite.classes import  AbstractSiteUserClass
from account.classes import AccountInformation
from cash.classes import CashTransaction
from .constants import WithdrawStatusConstants
from .exceptions import WithdrawStatusException
#-------------------------------------------------------------------
#-------------------------------------------------------------------

class AbstractWithdraw( AbstractSiteUserClass ):
    """
    Abstract class that imports
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

        :return:
        """
        pass

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

        self.validate_withdraw()

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

    def __check_status_pending(self, withdraw):
        if(self.withdraw_object.status.pk != WithdrawStatusConstants.Pending ):
            raise WithdrawStatusException(
                str(self.withdraw_object.pk),
                type(self.withdraw_class).__name__
            )

    def cancel(self, withdraw_pk, status_pk ):
        """
        Cancels a withdraw assuming the status is still pending
        :param withdraw_pk:
        :param status_pk:
        """
        self.withdraw_object = self.withdraw_class.objects.get(pk=withdraw_pk)
        self.__check_status_pending()
        self.withdraw_object.status = self.get_withdraw_status(status_pk)
        self.withdraw_object.save()


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
    def __init__(self, user):
        self.withdraw_class = models.PayPalWithdraw

        super().__init__(user)


    def validate_withdraw(self):
        super().validate_withdraw()

    def update_status(self):
        """
        Sets the status to Pending
        """
        super().update_status()

    def withdraw(self, amount, email):
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


    def validate_withdraw(self):
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

        super().validate_withdraw()

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
        self.withdraw_object = models.PayPalWithdraw.objects.get(pk=withdraw_pk)
        self.withdraw_object.check_number = check_number
        self.withdraw_object.status = self.get_withdraw_status(WithdrawStatusConstants.Processed.value)
        self.withdraw_object.save()



