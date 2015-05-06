from testfixtures import Replacer,test_datetime
from test.classes import AbstractTest
from .classes import AbstractWithdraw, PayPalWithdraw, CheckWithdraw
from mysite.exceptions import VariableNotSetException, IncorrectVariableTypeException, \
                                InvalidArgumentException, AmbiguousArgumentException, \
                                MethodNotOverriddenInChildException, WithdrawCalledTwiceException, \
                                CheckWithdrawCheckNumberRequiredException, CashoutWithdrawOutOfRangeException, \
                                MaxCurrentWithdrawsException, AmountZeroException
import datetime
from django.conf import settings
import decimal
import mysite
from cash.classes import CashTransaction
from cash.withdraw.classes import WithdrawMinMax, PendingMax
from account.classes import AccountInformation
from cash.exceptions import  TaxInformationException, OverdraftException
from .exceptions import  WithdrawStatusException
from .constants import WithdrawStatusConstants
from . import models
import django
from cash.tax.classes import TaxManager
from enum import Enum
from decimal import Decimal
import time
import psycopg2 # for IntegrityError exception

class WithdrawUser(Enum):
    """
    a way free of primary keys, or model objects that helps us specify a user type

    """
    ADMIN   = 1
    MANAGER = 2
    REGULAR = 3

# class CanGetNewWithdraw(object):
#     pass

class AdminCheckWithdrawTest(AbstractTest):
    """
    for the purpose of simplifying the testing of CheckWithdraw, PayPalWithdraw,
    and any addition classes which inherit AbstractWithdraw

    """
    WITHDRAW_CLASS  = CheckWithdraw  # must be a child of AbstractWithdraw, ie: CheckWithdraw

    def setUp(self):
        self.user               = self.get_admin_user()     # get a superuser
        self.withdraw_amount    = 10.00                     # using float here on purpose
        self.account_balance    = 10000.00                  # balance starting amount (once we add it)

        ct = CashTransaction(self.user)                     # get a new CashTransaction instance
        ct.deposit(self.account_balance)                    # start the balance with self.account_balance

        tm = TaxManager(self.user)
        tm.set_tax_id("123456789")


    def get_balance(self):
        return CashTransaction(self.user).get_balance_amount()


    def get_a_new_withdraw(self, user):
        # information must exist for the user who makes a withdraw
        information = AccountInformation(user)     # give self.user an Information object
        information.set_fields(
            fullname        = user.username + ' Mc' + user.username,
            address1        = 'address1',
            city            = 'city',
            state           = 'NH',
            zipcode         = '03820'
        )

        # self.user is set to the withdraw_object
        instance = self.WITHDRAW_CLASS( user=user )
        return instance

    #
    ###################################################
    # test the core functionality of Withdraw.
    # specific tests related to PayPal, or Checks
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
    def test_too_many_withdraws_for_same_user(self):
        # Make sure that we cannot add more than the max allowed withdraws for one user
        max_pending = PendingMax().value()
        print ("max_pending = " + str(max_pending))
        withdraws = []

        # This loop will create exactly the maximum allowable withdraws
        for withdrawAmount in range(11, 11 + max_pending):
            w = self.get_a_new_withdraw(self.user) # ie: w = CheckWithdraw( user )
            w.withdraw(Decimal(withdrawAmount))
            withdraws.append(w)

        # This withdraw should exceed the maximum allowable
        w = self.get_a_new_withdraw(self.user) # ie: w = CheckWithdraw( user )
        self.assertRaises(MaxCurrentWithdrawsException, lambda: w.withdraw( 95.00 ) )

        # Clean up the pending withdraws
        for w in withdraws:
            w.cancel()

    def test_too_many_withdraws_for_same_withdraw_object(self):
        # The withdraw method should only be called once per withdraw object
        w = self.get_a_new_withdraw(self.user) # ie: w = CheckWithdraw( user )
        w.withdraw( 101.00 )
        self.assertRaises(WithdrawCalledTwiceException, lambda: w.withdraw( 95.00 ) )
        w.cancel()

    def test_balance_the_same_after_too_many_withdraws(self):
        w = self.get_a_new_withdraw(self.user) # ie: w = CheckWithdraw( user )
        w.withdraw( 101.00 )
        balance_after_first_withdraw = self.get_balance()
        self.assertRaises(WithdrawCalledTwiceException, lambda: w.withdraw( 95.00 ) )
        self.assertEquals( balance_after_first_withdraw, self.get_balance() )
        w.cancel()

    def test_cancel_sets_proper_status_when_complete(self):
        cancelled = models.WithdrawStatus.objects.get(pk=WithdrawStatusConstants.CancelledAdminDefault.value)
        w = self.get_a_new_withdraw(self.user) # ie: w = CheckWithdraw( user )
        w.withdraw( 64.00 )
        w.cancel()
        self.assertEquals( w.withdraw_object.status, cancelled )

    def test_cancel_doesnt_modify_status_on_exception(self):
        pass # TODO - i dont think you can test this for CheckWithdraw

    def test_cancel_and_verify_balance_updates(self):
        amount = Decimal( 101.00 )
        start_balance = self.get_balance()
        w = self.get_a_new_withdraw(self.user) # ie: w = CheckWithdraw( user )
        w.withdraw( amount )
        balance_after_withdraw = self.get_balance()
        self.assertEquals( (balance_after_withdraw + amount), start_balance )
        w.cancel()
        self.assertEquals( start_balance, self.get_balance() )

    def test_cancel_bulk_list_of_withdraws(self):
        pass # TODO

    def test_payout_sets_proper_status_when_complete(self):
        processed = models.WithdrawStatus.objects.get(pk=WithdrawStatusConstants.Processed.value)
        w = self.get_a_new_withdraw(self.user) # ie: w = CheckWithdraw( user )
        w.withdraw( 80.00 )
        w.withdraw_object.check_number = 85
        w.payout()
        self.assertEquals( w.withdraw_object.status, processed )

    def test_payout_doesnt_modify_status_on_exception(self):
        w = self.get_a_new_withdraw(self.user) # ie: w = CheckWithdraw( user )
        w.withdraw( 195.00 )
        status_before = w.withdraw_object.status
        w.withdraw_object.check_number = None
        self.assertRaises( CheckWithdrawCheckNumberRequiredException, lambda: w.payout() ) # we dont care the type of exception in this test
        self.assertEquals( status_before, w.withdraw_object.status )

    def test_payout_bulk_list_of_withdraws(self):
        processed = models.WithdrawStatus.objects.get(pk=WithdrawStatusConstants.Processed.value)

        # First test a set of withdrawals that all should work
        for withdrawAmount in range(11, 20):
            w = self.get_a_new_withdraw(self.user) # ie: w = CheckWithdraw( user )
            w.withdraw(Decimal(withdrawAmount))
            # Use the withdrawAmount as the check number also
            w.withdraw_object.check_number = withdrawAmount
            w.payout()
            self.assertEquals( w.withdraw_object.status, processed )

        # Now, create a set of withdrawals where the 4th fails for no check number
        # Verify that the status on the other withdrawals is correct
        for withdrawAmount in range(21, 30):
            w = self.get_a_new_withdraw(self.user) # ie: w = CheckWithdraw( user )
            w.withdraw(Decimal(withdrawAmount))
            if withdrawAmount != 24:
                # Use the withdrawAmount as the check number also
                w.withdraw_object.check_number = withdrawAmount
                w.payout()
                self.assertEquals( w.withdraw_object.status, processed )
            else:
                self.assertRaises( CheckWithdrawCheckNumberRequiredException, lambda: w.payout() )



    def test_autopayout_threshold(self):
        pass # TODO

    def test_withdraw_below_minimum_raises_exception(self):
        cashout = WithdrawMinMax()
        amount = cashout.get_min()

        w = self.get_a_new_withdraw(self.user) # ie: w = CheckWithdraw( user )
        self.assertRaises( CashoutWithdrawOutOfRangeException, lambda: w.withdraw( Decimal(amount - 1)) )

    def test_withdraw_above_maximum_raises_exception(self):
        cashout = WithdrawMinMax()
        amount = cashout.get_max()

        w = self.get_a_new_withdraw(self.user) # ie: w = CheckWithdraw( user )
        self.assertRaises( CashoutWithdrawOutOfRangeException, lambda: w.withdraw( Decimal(amount + 1)) )

    def test_withdraw_minimim_amount(self):
        processed = models.WithdrawStatus.objects.get(pk=WithdrawStatusConstants.Processed.value)
        cashout = WithdrawMinMax()
        amount = cashout.get_min()

        w = self.get_a_new_withdraw(self.user) # ie: w = CheckWithdraw( user )
        w.withdraw(Decimal(amount))
        w.withdraw_object.check_number = 11
        w.payout()
        self.assertEquals( w.withdraw_object.status, processed )

    def test_withdraw_maximum_amount(self):
        processed = models.WithdrawStatus.objects.get(pk=WithdrawStatusConstants.Processed.value)
        cashout = WithdrawMinMax()
        amount = cashout.get_max()

        w = self.get_a_new_withdraw(self.user) # ie: w = CheckWithdraw( user )
        w.withdraw(Decimal(amount))
        w.withdraw_object.check_number = 11
        w.payout()
        self.assertEquals( w.withdraw_object.status, processed )

    def test_amounts_with_decimals_dont_get_truncated_or_rounded(self):
        # Make sure that decimal numbers are handled correctly
        start_balance = self.get_balance()
        withdraws = [23.01, 42.49, 18.99, 21.99]
        for withdraw in withdraws:
            amount = Decimal( withdraw )
            w = self.get_a_new_withdraw(self.user) # ie: w = CheckWithdraw( user )
            w.withdraw( amount )
            balance_after_withdraw = self.get_balance()
            self.assertAlmostEquals( (balance_after_withdraw + amount), start_balance, 4 )
            w.cancel()
        self.assertEquals( start_balance, self.get_balance() )

    def test_call_withdraw_twice_after_invalid_withdraw(self):
        # The withdraw method should only be called once per withdraw object, even if the first call failed
        w = self.get_a_new_withdraw(self.user) # ie: w = CheckWithdraw( user )
        self.assertRaises(AmountZeroException, lambda: w.withdraw( 0.00 ) )
        self.assertRaises(WithdrawCalledTwiceException, lambda: w.withdraw( 95.00 ) )

    def test_need_tax_id_if_withdraws_too_high(self):
        pass # TODO

    #
    #######################################################
    # tests specifically for CheckWithdraw
    #######################################################
    def test_payout_raises_exception_check_number_invalid(self):
        w = self.get_a_new_withdraw(self.user) # ie: w = CheckWithdraw( user )
        w.withdraw( 10.00 )
        self.assertRaises( CheckWithdrawCheckNumberRequiredException, lambda: w.payout() )

    def test_withdraw_method_called_more_than_once_in_a_row(self):
        # The withdraw method should only be called once per withdraw object
        w = self.get_a_new_withdraw(self.user) # ie: w = CheckWithdraw( user )
        w.withdraw( 101.00 )
        self.assertRaises(WithdrawCalledTwiceException, lambda: w.withdraw( 95.00 ) )

class AdminPayPalWithdrawTest( AbstractTest ):

    WITHDRAW_USER   = WithdrawUser.ADMIN
    WITHDRAW_CLASS  = PayPalWithdraw

    def setUp(self):
        self.user               = self.get_admin_user()     # get a superuser
        self.withdraw_amount    = 10.00                     # using float here on purpose
        self.account_balance    = 10000.00                  # balance starting amount (once we add it)

        ct = CashTransaction(self.user)                 # get a new CashTransaction instance
        ct.deposit(self.account_balance)                # start the balance with self.account_balance

        tm = TaxManager(self.user)
        tm.set_tax_id("123456789")


    def get_a_new_withdraw(self, user):
        # information must exist for the user who makes a withdraw
        information = AccountInformation(user)     # give self.user an Information object
        information.set_fields(
            fullname        = user.username + ' Mc' + user.username,
            address1        = 'address1',
            city            = 'city',
            state           = 'NH',
            zipcode         = '03820'
        )
        # self.user is set to the withdraw_object
        instance = self.WITHDRAW_CLASS( user=user )
        return instance

    #
    #######################################################
    # tests for calling withdraw() and for its side effects
    #######################################################
    def test_too_many_withdraws_for_same_user(self):
        # Make sure that we cannot add more than the max allowed withdraws for one user
        max_pending = PendingMax().value()
        print ("max_pending = " + str(max_pending))
        withdraws = []

        # This loop will create exactly the maximum allowable withdraws
        for withdrawAmount in range(11, 11 + max_pending):
            w = self.get_a_new_withdraw(self.user) # ie: w = PaypalWithdraw( user )
            w.withdraw(Decimal(withdrawAmount))
            withdraws.append(w)

        # This withdraw should exceed the maximum allowable
        w = self.get_a_new_withdraw(self.user) # ie: w = PaypalWithdraw( user )
        self.assertRaises(MaxCurrentWithdrawsException, lambda: w.withdraw( 95.00 ) )

        # Clean up the pending withdraws
        for w in withdraws:
            w.cancel()

    def test_too_many_withdraws_for_same_withdraw_object(self):
        # The withdraw method should only be called once per withdraw object
        w = self.get_a_new_withdraw(self.user) # ie: w = PaypalWithdraw( user )
        w.withdraw( 101.00 )
        self.assertRaises(WithdrawCalledTwiceException, lambda: w.withdraw( 95.00 ) )
        w.cancel()

    def test_balance_the_same_after_too_many_withdraws(self):
        w = self.get_a_new_withdraw(self.user) # ie: w = PayPalWithdraw( user )
        w.withdraw( 101.00 )
        balance_after_first_withdraw = self.get_balance()
        self.assertRaises(WithdrawCalledTwiceException, lambda: w.withdraw( 95.00 ) )
        self.assertEquals( balance_after_first_withdraw, self.get_balance() )
        w.cancel()

    def test_cancel_sets_proper_status_when_complete(self):
        cancelled = models.WithdrawStatus.objects.get(pk=WithdrawStatusConstants.CancelledAdminDefault.value)
        w = self.get_a_new_withdraw(self.user) # ie: w = PayPalWithdraw( user )
        w.withdraw( 64.00 )
        w.cancel()
        self.assertEquals( w.withdraw_object.status, cancelled )

    def test_cancel_doesnt_modify_status_on_exception(self):
        pass # TODO

    def test_cancel_and_verify_balance_updates(self):
        amount = Decimal( 101.00 )
        start_balance = self.get_balance()
        w = self.get_a_new_withdraw(self.user) # ie: w = PayPalWithdraw( user )
        w.withdraw( amount )
        balance_after_withdraw = self.get_balance()
        self.assertEquals( (balance_after_withdraw + amount), start_balance )
        w.cancel()
        self.assertEquals( start_balance, self.get_balance() )

    def test_cancel_bulk_list_of_withdraws(self):
        pass # TODO

    def test_payout_sets_proper_status_when_complete(self):
        processed = models.WithdrawStatus.objects.get(pk=WithdrawStatusConstants.Processed.value)
        processing = models.WithdrawStatus.objects.get(pk=WithdrawStatusConstants.Processing.value)
        w = self.get_a_new_withdraw(self.user) # ie: w = PayPalWithdraw( user )
        w.withdraw( 80.00 )
        w.payout()
        self.assertEquals( w.withdraw_object.status, processing )
        # Wait up to 3 minutes for PayPal to process the payment
        for i in range(0, 6):
            time.sleep(30)
            if w.withdraw_object.status == processed:
                break
        # Check that the paypal processing has finished and the status in processed
        self.assertEquals( w.withdraw_object.status, processing )



    def test_payout_doesnt_modify_status_on_exception(self):
        # TODO - may not be able to test this.  PayPal payout doesn't generate an exception unless status is not pending,
        # which is what we are testing for
        # w = self.get_a_new_withdraw(self.user) # ie: w = PayPalWithdraw( user )
        # w.withdraw( 195.00 )
        # status_before = w.withdraw_object.status
        # self.assertRaises( ???, lambda: w.payout() ) # we dont care the type of exception in this test
        # self.assertEquals( status_before, w.withdraw_object.status )

    def test_payout_withdraw(self):
        processed = models.WithdrawStatus.objects.get(pk=WithdrawStatusConstants.Processed.value)
        processing = models.WithdrawStatus.objects.get(pk=WithdrawStatusConstants.Processing.value)
        w = self.get_a_new_withdraw(self.user) # ie: w = PayPalWithdraw( user )
        w.withdraw( 80.00 )
        w.payout()
        self.assertEquals( w.withdraw_object.status, processing )

    def test_payout_bulk_list_of_withdraws(self):
        pass # TODO

    def test_autopayout_threshold(self):
        pass # TODO

    def test_withdraw_below_minimum_raises_exception(self):
        cashout = WithdrawMinMax()
        amount = cashout.get_min()

        w = self.get_a_new_withdraw(self.user) # ie: w = PayPalWithdraw( user )
        self.assertRaises( CashoutWithdrawOutOfRangeException, lambda: w.withdraw( Decimal(amount - 1)) )

    def test_withdraw_above_maximum_raises_exception(self):
        cashout = WithdrawMinMax()
        amount = cashout.get_max()

        w = self.get_a_new_withdraw(self.user) # ie: w = PayPalWithdraw( user )
        self.assertRaises( CashoutWithdrawOutOfRangeException, lambda: w.withdraw( Decimal(amount + 1)) )

    def test_withdraw_minimim_amount(self):
        processed = models.WithdrawStatus.objects.get(pk=WithdrawStatusConstants.Processed.value)
        cashout = WithdrawMinMax()
        amount = cashout.get_min()

        w = self.get_a_new_withdraw(self.user) # ie: w = PayPalWithdraw( user )
        w.withdraw(Decimal(amount))
        w.payout()
        self.assertEquals( w.withdraw_object.status, processed )

    def test_withdraw_maximum_amount(self):
        processed = models.WithdrawStatus.objects.get(pk=WithdrawStatusConstants.Processed.value)
        cashout = WithdrawMinMax()
        amount = cashout.get_max()

        w = self.get_a_new_withdraw(self.user) # ie: w = PayPalWithdraw( user )
        w.withdraw(Decimal(amount))
        w.payout()
        self.assertEquals( w.withdraw_object.status, processed )

    def test_amounts_with_decimals_dont_get_truncated_or_rounded(self):
        pass # TODO

    def test_need_tax_id_if_withdraws_too_high(self):
        pass # TODO

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
        cw.withdraw_object.check_number = check_number # set it in the model
        cw.withdraw_object.save()
        cw.payout()
        self.assertEqual(cw.withdraw_object.status , processed)

        #
        # attempt to payout() again!
        self.assertRaises(WithdrawStatusException, lambda:cw.payout())

        #
        # Tests duplicate check number
        another_cw = self.__make_withdrawal_check(self.withdraw_amount)
        self.assertEquals(another_cw.withdraw_object.status, pending)
        another_cw.withdraw_object.check_number = check_number
        self.assertRaises(django.db.utils.IntegrityError, lambda:another_cw.withdraw_object.save() )
        #self.assertRaises(django.db.utils.IntegrityError, lambda:another_cw.payout())

        # it wont ever be able to save, so lets just make sure this throws some kind of exception
        self.assertRaises(Exception, lambda:another_cw.payout())

    def test_check_cancel_payout(self):

        cw = self.__make_withdrawal_check(self.withdraw_amount)
        pending = models.WithdrawStatus.objects.get(pk=WithdrawStatusConstants.Pending.value)
        self.assertEquals(cw.withdraw_object.status, pending)

        cancelled = models.WithdrawStatus.objects.get(pk=WithdrawStatusConstants.CancelledAdminDefault.value)
        cw.cancel()
        self.assertEqual(cw.withdraw_object.status , cancelled)

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

