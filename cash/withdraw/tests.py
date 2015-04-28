from testfixtures import Replacer,test_datetime
from test.classes import AbstractTest
from .classes import AbstractWithdraw, PayPalWithdraw, CheckWithdraw
from mysite.exceptions import VariableNotSetException, IncorrectVariableTypeException, \
                                InvalidArgumentException, AmbiguousArgumentException, \
                                MethodNotOverriddenInChildException
import datetime
from django.conf import settings
import decimal
import mysite
from cash.classes import CashTransaction
from account.classes import AccountInformation
from cash.exceptions import  TaxInformationException, OverdraftException
from .exceptions import  WithdrawStatusException
from .constants import WithdrawStatusConstants
from . import models
import django
from cash.tax.classes import TaxManager
from enum import Enum

class WithdrawUser(Enum):
    """
    a way free of primary keys, or model objects that helps us specify a user type

    """
    ADMIN   = 1
    MAANGER = 2
    REGULAR = 3

class AbstractWithdrawTest(AbstractTest):
    """
    for the purpose of simplifying the testing of CheckWithdraw, PayPalWithdraw,
    and any addition classes which inherit AbstractWithdraw

    """
    WITHDRAW_USER   = None  # a WithdrawUser enumeration, ie: WithdrawUser.ADMIN
    WITHDRAW_CLASS  = None  # must be a child of AbstractWithdraw, ie: CheckWithdraw

    def setUp(self):
        #
        # __validate_settings() MUST be the first call,
        #  to ensure WITHDRAW_USER, etc... were set up by the programmer
        self.__validate_settings()

        self.user = self.__get_user_from_type( self.WITHDRAW_USER )   # get the user by their WithdrawUser enum type
        self.withdraw_amount = 10.00                    # using float here on purpose
        self.account_balance = 1000.00                  # balance starting amount (once we add it)

        ct = CashTransaction(self.user)                 # get a new CashTransaction instance
        ct.deposit(self.account_balance)                # start the balance with self.account_balance

        #
        # we can move time, and restore if we'd like...
        #r = self.move_time(days = 365, hours = 1)
        #r.restore()

        # self.withdraw = None

    #
    ##########################
    # must override methods  #
    ##########################
    def get_a_new_withdraw(self, user):
        # self.user is set to the withdraw_object
        instance = self.WITHDRAW_CLASS( user=user )
        return instance

    #
    ##########################
    # internal class methods #
    ##########################
    def __validate_settings(self):
        err_msg = '\n\n'

        if self.__class__.__name__ == 'AbstractWithdrawTest':
            err_msg += self.__class__.__name__ + ' *** you may not instantiate this class directly\n'
            err_msg += self.__class__.__name__ + ' *** must not have any methods that start with "test"\n'

        if self.WITHDRAW_USER is None:
            err_msg += self.__class__.__name__ + ' *** you didnt set WITHDRAW_USER\n'
        if self.WITHDRAW_CLASS is None:
            err_msg += self.__class__.__name__ + ' *** you didnt set WITHDRAW_CLASS\n'
        # if self.WITHDRAW_MODEL is None:
        #     err_msg +=  self.__class__.__name__ + ' *** you didnt set WITHDRAW_MODEL\n'

        if err_msg.strip(): # if after stripping it of whitespace its empty...
            raise Exception( err_msg )

    def __get_user_from_type(self, withdraw_user):
        if withdraw_user == WithdrawUser.ADMIN:
            return self.get_admin_user()
        elif withdraw_user == WithdrawUser.MANAGER:
            return self.get_staff_user()
        else:
            return self.get_basic_user()

    #
    ##########################
    # helper methods
    ##########################
    def move_time(self, days, hours):
        today = datetime.datetime.now()
        time = today - datetime.timedelta(
                            days= days,
                            hours = hours
        )
        return self.set_time(time)

    def set_time(self, dt):
        r = Replacer()
        r.replace(
            'testfixtures.tests.sample1.datetime',
            test_datetime(
                dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second
            )
        )
        return r

    #
    ###################################################
    # test the core functionality of Withdraw.
    # specific tests related to PayPal, or Checks
    # should go in their own classes: PayPal
    ###################################################
    def test_invalid_instantiation_argument_user(self):
        self.assertRaises(IncorrectVariableTypeException, lambda: self.WITHDRAW_CLASS( user=int(1) ) )

    def test_invalid_instantiation_argument_pk_with_none_user(self):
        self.assertRaises(IncorrectVariableTypeException, lambda: self.WITHDRAW_CLASS( user=None, pk='asdf' ) )

    def test_invalid_instantiation_argument_pk_only(self):
        self.assertRaises(IncorrectVariableTypeException, lambda: self.WITHDRAW_CLASS( pk='asdf' ) )

    def test_invalid_instantiation_argument_pk_negative(self):
        self.assertRaises(InvalidArgumentException, lambda: self.WITHDRAW_CLASS( pk=int(-1) ) )

    def test_user_and_pk_both_valid_but_users_differ(self):
        """
        if user AND pk valid, the situation is potentially confusing, and definitely ambiguous
        """
        instance = self.get_a_new_withdraw( self.user )
        instance.withdraw( self.withdraw_amount )
        alternate_user = self.get_alternate_user( self.user ) # retrieve a user DIFFERENT than the one given
        self.assertNotEqual( alternate_user, self.user )
        self.assertRaises(AmbiguousArgumentException, lambda: self.WITHDRAW_CLASS( alternate_user, instance.withdraw_object.pk ) )

    #
    #######################################################
    # tests for calling withdraw() and for its side effects
    #######################################################
    def test_too_many_withdraws(self):
        pass # TODO

    def test_balance_the_same_after_too_many_withdraws(self):
        pass # TODO

    def test_cancel_sets_proper_status_when_complete(self):
        pass # TODO

    def test_cancel_doesnt_modify_status_on_exception(self):
        pass # TODO

    def test_cancel_and_verify_balance_updates(self):
        pass # TODO

    def test_cancel_bulk_list_of_withdraws(self):
        pass # TODO

    def test_payout_sets_proper_status_when_complete(self):
        pass # TODO

    def test_payout_doesnt_modify_status_on_exception(self):
        pass # TODO

    def test_payout_withdraw(self):
        pass # TODO

    def test_payout_bulk_list_of_withdraws(self):
        pass # TODO

    def test_autopayout_threshold(self):
        pass # TODO

    def test_withdraw_below_minimum_raises_exception(self):
        pass # TODO

    def test_withdraw_above_maximum_raises_exception(self):
        pass # TODO

    def test_withdraw_minimim_amount(self):
        pass # TODO

    def test_withdraw_maximum_amount(self):
        pass # TODO

    def test_amounts_with_decimals_dont_get_truncated_or_rounded(self):
        pass # TODO

class WithdrawTestCheckWithdraw( AbstractWithdrawTest ):

    WITHDRAW_USER   = WithdrawUser.ADMIN
    WITHDRAW_CLASS  = CheckWithdraw

    # Override
    def get_a_new_withdraw(self, user):

        information = AccountInformation( user )     # give self.user an Information object
        information.set_fields(
            fullname        = 'Ryan',
            address1        = 'address1',
            city            = 'city',
            state           = 'NH',
            zipcode         = '03820'
        ) # calls save() by default

        return super().get_a_new_withdraw( user )

    #
    #######################################################
    # tests specifically for CheckWithdraw
    #######################################################
    def test_payout_raises_exception_check_number_invalid(self):
        pass # TODO

    def test_withdraw_method_called_more_than_once_in_a_row(self):
        pass # TODO

class WithdrawTestPayPalWithdraw( AbstractWithdrawTest ):

    WITHDRAW_USER   = WithdrawUser.ADMIN
    WITHDRAW_CLASS  = PayPalWithdraw

    # Override
    def get_a_new_withdraw(self, user):
        instance = super().get_a_new_withdraw( user )

        # we must set the email before withdraw can be called
        instance.set_paypal_email( 'testpaypal@test.com' )
        return instance

    #
    #######################################################
    # tests specifically for PayPalWithdraw
    #######################################################
    def test_paypal_email_not_set_exception_new_instance_created_with_user(self):
        pass # TODO

    def test_paypal_email_not_set_exception_field_was_none(self):
        pass # TODO

    def test_paypal_email_not_set_exception_field_was_empty_string(self):
        pass # TODO

    def test_paypal_task_payout_completes(self):
        pass # TODO

    def test_paypal_payout_timeout_60_seconds(self):
        pass # TODO

    def test_paypal_payout_sets_paypal_transaction_id(self):
        pass # TODO

    def test_paypal_payout_bulk(self):
        pass # TODO

    def test_paypal_cancel_bulk(self):
        pass # TODO

    def test_withdraw_method_called_more_than_once_in_a_row(self):
        pass # TODO

class WithdrawTest(AbstractTest):
    """
    Test :class:`cash.classes.CheckWithdraw` and  :class:`cash.classes.PayPalWithdraw`

    """

    def setUp(self):
        self.withdraw_amount = decimal.Decimal(10.00)   # a decimal amount
        self.account_balance = 1000.00                  # balance starting amount (once we add it)
        self.user     = self.get_admin_user()           #
        r = self.move_time(days = 365, hours = 1)       # adjust time test
        ct = CashTransaction(self.user)                 # get a new CashTransaction instance

        ct.deposit(self.account_balance)                # start the balance with self.account_balance
        information = AccountInformation(self.user)     # give self.user an Information object
        information.set_fields(
            fullname        = 'Ryan',
            address1        = 'address1',
            city            = 'city',
            state           = 'NH',
            zipcode         = '03820'
        )
        r.restore()

    #
    ##########################
    # internal class methods #
    ##########################
    def move_time(self, days, hours):
        today = datetime.datetime.now()
        time = today - datetime.timedelta(
                            days= days,
                            hours = hours
        )

        return self.set_time(time)

    def set_time(self, dt):
        r = Replacer()
        r.replace(
            'testfixtures.tests.sample1.datetime',
            test_datetime(
                dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second
            )
        )
        return r

    def __make_withdrawal_check(self, amount):
        w = CheckWithdraw(self.user)
        w.withdraw(amount)
        return w

    def __make_withdrawal_paypal(self, amount):
        w = PayPalWithdraw(self.user)
        w.set_paypal_email(self.user.email)
        w.withdraw(amount)
        return w

    # def __make_payout_check(self):
    #     pass
    #
    # def __make_payout_paypal(self):
    #     pass

    #
    #########################################################################################
    # CheckWithdraw
    #########################################################################################

    def test_checkwithdraw_invalid_instantiation_argument_user(self):
        self.assertRaises(IncorrectVariableTypeException, lambda:CheckWithdraw(1))

    def test_checkwithdraw_invalid_instantiation_argument_model_pk(self):
        pass

    def test_checkwithdraw_valid_instantiation_argument_user(self):
        self.assertIsNotNone(CheckWithdraw(self.user))

    def test_checkwithdraw_valid_instantiation_argument_model_pk(self):
        pass

    def test_negative_withdrawal(self):
        self.assertRaises(
            mysite.exceptions.AmountNegativeException,
            lambda: self.__make_withdrawal_check(decimal.Decimal(-1))
        )
        self.assertRaises(
            mysite.exceptions.AmountNegativeException,
            lambda: self.__make_withdrawal_paypal(decimal.Decimal(-1))
        )
    def test_zero_withdrawal(self):
        self.assertRaises(
            mysite.exceptions.AmountZeroException,
            lambda: self.__make_withdrawal_check(decimal.Decimal(0.00))
        )
        self.assertRaises(
            mysite.exceptions.AmountZeroException,
            lambda: self.__make_withdrawal_paypal(decimal.Decimal(0.00))
        )

    def test_overdraft(self):
        self.assertRaises(
            OverdraftException,
            lambda: self.__make_withdrawal_check(decimal.Decimal(self.account_balance +1) )
        )
        self.assertRaises(
            OverdraftException,
            lambda: self.__make_withdrawal_paypal(decimal.Decimal(self.account_balance +1) )
        )


    def test_check_withdraw(self):
        cw = self.__make_withdrawal_check(self.withdraw_amount)
        pending = models.WithdrawStatus.objects.get(pk=WithdrawStatusConstants.Pending.value)
        self.assertEquals(cw.withdraw_object.status, pending)

        #
        # Tests the withdrawal over the amount where tax info is required
        self.assertRaises(TaxInformationException, lambda:self.__make_withdrawal_check(decimal.Decimal(settings.DFS_CASH_WITHDRAWAL_AMOUNT_REQUEST_TAX_INFO)))

        #
        # Test that there is no error when we have the amount to withdraw
        tm = TaxManager(self.user)
        tm.set_tax_id("012345678")
        cw = self.__make_withdrawal_check(
                decimal.Decimal(settings.DFS_CASH_WITHDRAWAL_AMOUNT_REQUEST_TAX_INFO)
        )
        self.assertEquals(cw.withdraw_object.status, pending)



    def test_check_payout(self):
        cw = self.__make_withdrawal_check(self.withdraw_amount)
        pending = models.WithdrawStatus.objects.get(pk=WithdrawStatusConstants.Pending.value)
        self.assertEquals(cw.withdraw_object.status, pending)
        check_number = 101
        #
        # Tests proper payout
        processed = models.WithdrawStatus.objects.get(pk=WithdrawStatusConstants.Processed.value)
        new_cw =CheckWithdraw(self.user)
        new_cw.payout(cw.withdraw_object.pk, check_number)
        self.assertEqual(new_cw.withdraw_object.status , processed)

        #
        # Tests already marked version
        new_cw =CheckWithdraw(self.user)
        self.assertRaises(WithdrawStatusException, lambda:new_cw.payout(cw.withdraw_object.pk, check_number))

        #
        # Tests duplicate check number
        cw = self.__make_withdrawal_check(self.withdraw_amount)
        self.assertEquals(cw.withdraw_object.status, pending)
        new_cw =CheckWithdraw(self.user)
        self.assertRaises(django.db.utils.IntegrityError, lambda:new_cw.payout(cw.withdraw_object.pk, check_number))


    def test_check_cancel_payout(self):

        cw = self.__make_withdrawal_check(self.withdraw_amount)
        pending = models.WithdrawStatus.objects.get(pk=WithdrawStatusConstants.Pending.value)
        self.assertEquals(cw.withdraw_object.status, pending)

        #
        # Tests cancel payout
        cancelled = models.WithdrawStatus.objects.get(pk=WithdrawStatusConstants.CancelledAdminDefault.value)
        new_cw =CheckWithdraw(self.user)
        new_cw.cancel(cw.withdraw_object.pk, WithdrawStatusConstants.CancelledAdminDefault.value)
        self.assertEqual(new_cw.withdraw_object.status , cancelled)

        ct = CashTransaction(self.user)
        self.assertAlmostEquals(ct.get_balance_amount(), decimal.Decimal(self.account_balance))

    #
    #########################################################################################
    # PayPalWithdraw
    #########################################################################################
    def test_paypal_withdrawl_invalid_instantiation_arguments(self):
        #
        # instantiation of PayPalWithdraw object without user
        self.assertRaises(IncorrectVariableTypeException, lambda:PayPalWithdraw(1))

        #
        # proper initialization of PayPalWithdraw
        self.assertIsNotNone(PayPalWithdraw(self.user))

