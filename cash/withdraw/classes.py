from decimal import Decimal
from logging import getLogger

from django.conf import settings
from django.db.transaction import atomic
from django.utils import timezone

import pp.classes
from account.classes import AccountInformation
from cash.classes import CashTransaction
from cash.exceptions import TaxInformationException, OverdraftException
from cash.tax.classes import (
    TaxManager,
)
from mysite.classes import AbstractSiteUserClass
from mysite.exceptions import (
    IncorrectVariableTypeException,
    VariableNotSetException,
    InvalidArgumentException,
    AmbiguousArgumentException,
    UnimplementedException,
    MaxCurrentWithdrawsException,
    CashoutWithdrawOutOfRangeException,
    CheckWithdrawCheckNumberRequiredException,
    AmountNegativeException,
    WithdrawCalledTwiceException,
)
from pp.exceptions import PayoutError
from transaction.constants import TransactionTypeConstants
from transaction.models import TransactionType
from . import models
from .constants import WithdrawStatusConstants
from .exceptions import WithdrawStatusException

logger = getLogger('withdraw.classes')


class WithdrawMinMax(object):
    """
    class to get / set the cashout withdraw minimum and maximum dollar amounts
    """

    def __init__(self):
        try:
            self.cashout_withdraw_setting = models.CashoutWithdrawSetting.objects.get(pk=1)
        except models.CashoutWithdrawSetting.DoesNotExist:
            self.cashout_withdraw_setting = models.CashoutWithdrawSetting()
            self.cashout_withdraw_setting.min_withdraw_amount = Decimal(5.00)
            self.cashout_withdraw_setting.max_withdraw_amount = Decimal(10000.00)
            self.cashout_withdraw_setting.save()

    def set_min(self, min):
        self.cashout_withdraw_setting.min_withdraw_amount = Decimal(min)
        self.cashout_withdraw_setting.save()

    def set_max(self, max):
        self.cashout_withdraw_setting.max_withdraw_amount = Decimal(max)
        self.cashout_withdraw_setting.save()

    def get_min(self):
        return self.cashout_withdraw_setting.min_withdraw_amount

    def get_max(self):
        return self.cashout_withdraw_setting.max_withdraw_amount


class AutoPayout(object):
    """
    class for managing the single value
    """

    def __init__(self):
        try:
            self.automatic_withdraw = models.AutomaticWithdraw.objects.get(pk=1)
        except models.AutomaticWithdraw.DoesNotExist:
            self.automatic_withdraw = models.AuthomaticWithdraw()
            self.automatic_withdraw.auto_payout_below = Decimal(50.00)
            self.automatic_withdraw.save()

    def value(self):
        """
        return the auto_payout_below value as a float
        """
        return float(self.automatic_withdraw.auto_payout_below)

    def update(self, amount):
        """
        updates the auto payout threshold, so that any withdraw(cashout) requests
        equal to or below this amount dont have to wait for admin review

        this method casts the value passed to a decimal.Decimal()
        """
        self.automatic_withdraw.auto_payout_below = Decimal(amount)
        self.automatic_withdraw.save()
        return self.value()  # return the value we just set


class PendingMax(object):
    """
    class for managing the that represents the number of currently
    pending withdraws (per cashout type (ie: this number applies to Check, and PayPal separately)
    """

    def __init__(self):
        try:
            self.pending_withdraw_max = models.PendingWithdrawMax.objects.get(pk=1)
        except models.PendingWithdrawMax.DoesNotExist:
            self.pending_withdraw_max = models.PendingWithdrawMax()
            self.pending_withdraw_max.auto_payout_below = 3
            self.pending_withdraw_max.save()

    def value(self):
        """
        return the auto_payout_below value as a float
        """
        return self.pending_withdraw_max.max_pending

    def update(self, val):
        """
        updates the auto payout threshold, so that any withdraw(cashout) requests
        equal to or below this amount dont have to wait for admin review

        this method casts the value passed to a decimal.Decimal()
        """
        self.pending_withdraw_max.max_pending = val
        self.pending_withdraw_max.save()
        return self.value()  # return the value we just set


# -------------------------------------------------------------------
# -------------------------------------------------------------------
class AbstractWithdraw(AbstractSiteUserClass):
    """
    Abstract class for maintaining the Withdraw process
    """

    OUTSTANDING_WITHDRAW_STATUSES = [
        WithdrawStatusConstants.Pending.value,
        WithdrawStatusConstants.Processing.value,
    ]

    withdraw_class = None  # this represents the class of the model
    payout_transaction_model_class = models.PayoutTransaction

    def __init__(self, user, pk):
        """
        Initializes the variables
        :param user:
        :return:
        """

        # if the pk is valid, we want to use the user already
        # associated with the cash_transaction_detail
        if pk:
            try:
                pk = int(pk)
            except:
                raise IncorrectVariableTypeException(type(self).__name__,
                                                     "pk - it needs to be an int()")
            if pk < 0:
                raise InvalidArgumentException(type(self).__name__, "pk - must be non-negative")

            # get the model instance for the withdraw_class we have
            withdraw_model = self.withdraw_class.objects.get(pk=pk)

            # call the super, with the user in the original transaction
            if user and user.username not in withdraw_model.cash_transaction_detail.user.username:
                raise AmbiguousArgumentException(type(self).__name__,
                                                 "user is valid, but different from the user in the model for that pk!!!")

            super().__init__(withdraw_model.cash_transaction_detail.user)

            self.withdraw_object = withdraw_model  # self.withdraw_class.objects.get(pk=pk)

        else:
            # call super with the user object passed to us
            super().__init__(user)
            self.withdraw_object = None

        self.validate_local_variables()

    def validate_local_variables(self):
        if (self.withdraw_class == None):
            raise VariableNotSetException(type(self).__name__, "withdraw_class")

        if (not issubclass(self.withdraw_class, models.Withdraw)):
            raise IncorrectVariableTypeException(type(self).__name__, "withdraw_class")

    def save_payout_history(self, withdraw_object, api_response_data):
        """
        save the paypal api response (as json) along with the WithdrawRequest

        :param withdraw_object:
        :param api_response_data:
        :return:
        """
        model_instance = self.payout_transaction_model_class()
        model_instance.withdraw = withdraw_object
        model_instance.data = api_response_data
        model_instance.save()

    def validate_withdraw(self, amount):
        """
        Sets the standard withdraw data in the :class:`cash.withdraw.models.Withdraw`
        abstract model.

        """

        if amount < Decimal(0.0):
            raise AmountNegativeException(type(self).__name__, 'amount: ' + str(amount))

        #
        # make sure they dont have more than the max outstanding withdraw requests
        max_pending = PendingMax().value()
        user_pending_withdraws = self.withdraw_class.objects.filter(
            cash_transaction_detail__user=self.user,
            status__in=self.OUTSTANDING_WITHDRAW_STATUSES)
        if len(user_pending_withdraws) >= max_pending:
            raise MaxCurrentWithdrawsException(type(self).__name__, "user at max pending withdraws")

        #
        # less than minimum ? greater than maximum ? we dont want that
        cashout = WithdrawMinMax()
        if amount < cashout.get_min() or cashout.get_max() < amount:
            raise CashoutWithdrawOutOfRangeException(type(self).__name__,
                                                     "the amount must be within the range ($%s to $%s)" % (
                                                         str(cashout.get_min()),
                                                         str(cashout.get_max())))

        #
        # Checks to make sure we are not withdrawing more than we have
        ct = CashTransaction(self.user)
        balance = ct.get_balance_amount()
        if balance < amount:
            raise OverdraftException(self.user.username)

        #
        # Gets the profit for the year before the current withdrawal
        # and raises an exception if their tax information needs to
        # be collected.
        current_year_profit = ct.get_withdrawal_amount_current_year()
        if (current_year_profit + amount) >= settings.DFS_CASH_WITHDRAWAL_AMOUNT_REQUEST_TAX_INFO:
            #
            # Checks to see if we collected tax information for the user
            tm = TaxManager(self.user)
            if not tm.info_collected():
                raise TaxInformationException(self.user.username)

    def decline(self):
        """
        TOOD - implement

        :return: #2r8y82pc
        """
        raise UnimplementedException(type(self).__name__, 'decline()')

    def should_auto_payout(self, amount):
        """
        currently, this method always returns False

        if this amount is at least the minimum cashout,
        and is under the set autopay value, process the payout immediately.
        :param amount:
        :return:
        """
        self.__should_auto_payout(self, amount)
        x = settings.DFS_CASH_WITHDRAWAL_APPROVAL_REQ_AMOUNT
        raise UnimplementedException(type(self).__name__, 'should_auto_payout()')

    def withdraw(self, amount):
        """
        This method creates a cash withdrawal transaction and the appropriate book
        keeping for allowing
        :param amount:
        :return:
        """

        # The first time withdraw is called, withdraw_object and withdraw_object.status will both not be set.
        # On a successful withdraw, withdraw_object and withdraw_object.status will both be set.
        # On an invalid withdraw (amount 0, amount too large, etc),
        #  withdraw_object will be set but withdraw_object.status will not.
        # If withdraw_object is set, we want to raise a WithdrawCalledTwice exception if withdraw_object.status is set
        #  or if it does not exist.
        if self.withdraw_object:
            try:
                if self.withdraw_object.status:
                    raise WithdrawCalledTwiceException(type(self).__name__,
                                                       'withdraw() can only be called on the object one time')
            except:
                raise WithdrawCalledTwiceException(type(self).__name__,
                                                   'withdraw() can only be called on the object one time')

        amount = Decimal(amount)

        #
        # if this instance wasnt created by pk, its not set/created yet.
        if self.withdraw_object == None:
            logger.info('creating withdraw_object in parent')
            self.withdraw_object = self.withdraw_class()

            tm = TaxManager(self.user)
            self.withdraw_object.net_profit = tm.calendar_year_net_profit()

        #
        # throws exceptions if insufficient funds, or tax info required
        logger.info('parent - call validate_withdraw')
        self.validate_withdraw(amount)

        #
        # Performs the transaction since everything has been validated
        # and saves the the transaction detail with the withdraw object.
        logger.info('parent - create the cash transaction')
        ct = CashTransaction(self.user)
        ct.withdraw(amount)
        self.withdraw_object.cash_transaction_detail = ct.transaction_detail
        self.withdraw_object.status = self.get_withdraw_status(
            WithdrawStatusConstants.Pending.value)
        self.withdraw_object.save()  # save in db

    def __check_status_pending(self):
        """
        this internal method is used to throw an exception if an action
        is called, primarily payout(), but the model is not in a state that would allow that.

        :return:
        """
        if self.withdraw_object.status != self.get_withdraw_status(
                WithdrawStatusConstants.Pending.value):
            logger.info(self.withdraw_object.status.description)
            raise WithdrawStatusException(str(self.withdraw_object.pk),
                                          type(self.withdraw_object).__name__)

    def cancel(self):  # old args: , withdraw_pk, status_pk ):
        """
        Cancels a withdraw assuming the status is still pending. Releases the funds back to user.

        :param withdraw_pk:
        :param status_pk:
        """
        self.__check_status_pending()
        self.withdraw_object.status = self.get_withdraw_status(
            WithdrawStatusConstants.CancelledAdminDefault.value)
        self.withdraw_object.save()

        #
        # Creates a new transaction for the refunded amount.
        category = TransactionType.objects.get(
            pk=TransactionTypeConstants.AdminCancelWithdraw.value)
        ct = CashTransaction(self.user)
        ct.deposit(abs(self.withdraw_object.cash_transaction_detail.amount), category)

    def payout(self):
        """
        we shouldnt need the pk to do the payout because,
        regardless of how it was created it must have the
        model instance set internally to do payouts.

        """
        self.__check_status_pending()  # throws exception if we cant
        status = self.get_withdraw_status(WithdrawStatusConstants.Processing.value)
        self.withdraw_object.status = status
        self.withdraw_object.save()

    def get_withdraw_status(self, status_pk):
        """
        Get the WithdrawStatus by its pk, which is the same as its WithdrawStatusConstants value
        """
        return models.WithdrawStatus.objects.get(pk=status_pk)


class PayPalEmailNotSetException(Exception):
    def __init__(self, class_name, variable_name):
        super().__init__('the paypal "email" field was not set - '
                         'use set_paypal_email() before calling withdraw()')


# -------------------------------------------------------------------
# -------------------------------------------------------------------
class PayPalWithdraw(AbstractWithdraw):
    """
    Class for interfacing with paypal. Allows the admin to process payouts
    and update the statuses of withdrawals.

    """

    def __init__(self, user=None, pk=None):
        """
        to create a new PayPalWithdraw, specify only the user.
        if pk is non-negative, attempt to get an existing PayPalWithdraw object

        :param user:
        :param paypal_withdraw_pk:
        :return:
        """
        self.withdraw_class = models.PayPalWithdraw  # before super()
        self.paypal_email = None
        super().__init__(user, pk)

    def validate_withdraw(self, amount):
        """

        :param amount:
        :return:
        """
        logger.info('child - check if paypal email has been set')
        # if the email doesnt already exist in the withdraw_object, nor has it been set yet...
        if not self.__get_paypal_email():
            raise PayPalEmailNotSetException(type(self).__name__, 'paypal_email')

        print('child - self.__get_paypal_email()', self.__get_paypal_email())
        self.withdraw_object.email = self.__get_paypal_email()
        # self.withdraw_object.email = self.__get_paypal_email()
        # self.withdraw_object.save()
        print('child calls super() validate_withdraw()')
        print('child withdraw_object.pk', self.withdraw_object.pk)
        print('child withdraw_object.email', self.withdraw_object.email)
        super().validate_withdraw(amount)

    #
    # Must be called before withdraw()
    # This should  be used when the programmer wants to create
    # a paypalwithdraw from scratch. This email will be ignored
    # if the instance is created from a withdraw primary key
    def set_paypal_email(self, email):
        """
        if PayPalWithdraw was created from a pk, this has no effect
        :param email:
        :return:
        """

        # if the class was not created from a primary key
        # the withdraw_object will currently be None and
        # we will need to use the email passed into this method
        if self.withdraw_object is None:
            self.paypal_email = email

    def __get_paypal_email(self):
        """
        first tries to get the email from the withdraw_object,
        and if it doesnt exist there, returns self.paypal_email.
        :return:
        """
        if self.withdraw_object and self.withdraw_object.email:
            # try to get the email from the withdraw_object
            return self.withdraw_object.email
        else:
            return self.paypal_email

    @atomic
    def payout(self, request=None):
        """
        Pays out the user via PayPal
        """

        # validates that it can payout, and sets status to indicate processing
        super().payout()

        # process the payout
        payout = pp.classes.Payout(self.withdraw_object)
        data = payout.payout()
        payout_response = pp.classes.PayoutResponse(data)

        # save the paypal json api response and link it to this withdraw object
        self.save_payout_history(self.withdraw_object, data)

        # depending on the paypal transaction status...
        # error_str = ''
        # try:
        errors = payout_response.get_errors()

        self.withdraw_object.paypal_payout_item = payout_response.get_payout_item_id()
        self.withdraw_object.paypal_transaction = payout_response.get_transaction_id()
        self.withdraw_object.paypal_transaction_status = payout_response.get_transaction_status()

        if errors is None or errors == []:
            self.withdraw_object.status = self.get_withdraw_status(
                WithdrawStatusConstants.Processed.value)
            self.withdraw_object.processed_at = timezone.now()
        else:
            logger.error('withdraw.classes: errors list was non-empty! errors: %s' % errors)
            self.withdraw_object.status = self.get_withdraw_status(
                WithdrawStatusConstants.Pending.value)
            self.withdraw_object.paypal_errors = str(errors.get('message'))

        # save the model with the paypal information
        self.withdraw_object.save()
        # If we had errors, throw an exception that is caught by the admin function and displayed
        # in the admin section messages.
        if self.withdraw_object.paypal_errors:
            raise PayoutError(self.withdraw_object.paypal_errors)


# -------------------------------------------------------------------
# -------------------------------------------------------------------
class CheckWithdraw(AbstractWithdraw):
    def __init__(self, user=None, pk=None):
        self.withdraw_class = models.CheckWithdraw  # before super()
        super().__init__(user, pk)

    def validate_withdraw(self, amount):
        """
        raises exception if user doesnt have a valid mailing address.

        :raise :class:`account.exceptions.AccountInformationException`: When there are
            missing fields for the user's mailing address.
        """
        #
        # raise execption if overdraft possible, or tax info does not exist
        super().validate_withdraw(amount)

        #
        # Validates the mailing address. Throws an exception
        # if the address is not validated
        account_information = AccountInformation(self.user)
        account_information.validate_mailing_address()

        #
        # sets the local variables in the withdraw object
        self.withdraw_object.fullname = account_information.information.user.get_full_name()
        # information model hasn't that fields any more
        # self.withdraw_object.address1   = account_information.information.address1
        # self.withdraw_object.address2   = account_information.information.address2
        # self.withdraw_object.city       = account_information.information.city
        # self.withdraw_object.state      = account_information.information.state
        # self.withdraw_object.zipcode    = account_information.information.zipcode

    def payout(self):
        """
        Marks the check as paid by updating hte status to processed
        """

        if not self.withdraw_object.check_number:
            # if self.withdraw_object.check_number is None or self.withdraw_object.check_number == '':
            raise CheckWithdrawCheckNumberRequiredException(type(self).__name__, 'check_number')

        super().payout()  # primarily flags status as processing

        # p = pp.classes.payout_test( pk=self.withdraw_object.pk )
        self.withdraw_object.status = self.get_withdraw_status(
            WithdrawStatusConstants.Processed.value)
        self.withdraw_object.save()
