from testfixtures import Replacer,test_datetime
from test.classes import AbstractTest
from .classes import AbstractWithdraw, PayPalWithdraw, CheckWithdraw
from mysite.exceptions import VariableNotSetException, IncorrectVariableTypeException
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
class WithdrawTest(AbstractTest):
    """
    Test the :class:`cash.classes.CashWithdrawalManager` class

    TODO - need to test paypal and tax info manager working with
           the withdraw function for cash withdrawal
    """
    def setUp(self):
        self.withdraw_amount = decimal.Decimal(10.00)
        self.account_balance = 1000.00
        self.user     = self.get_admin_user()
        r = self.move_time(days = 365, hours = 1)
        ct = CashTransaction(self.user)

        ct.deposit(self.account_balance)
        information = AccountInformation(self.user)
        information.set_fields(
            fullname        = 'Ryan',
            address1        = 'address1',
            city            = 'city',
            state           = 'NH',
            zipcode         = '03820'
        )
        r.restore()


    def __make_withdrawal_check(self, amount):
        w = CheckWithdraw( self.user )
        w.withdraw(amount)
        return w
    def __make_withdrawal_paypal(self, amount):
        w = PayPalWithdraw( self.user )
        w.withdraw(amount,self.user.email)
        return w




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


    def test_improper_use(self):


        #
        # instantiation of PayPalWithdraw object without user
        self.assertRaises(IncorrectVariableTypeException, lambda:PayPalWithdraw(1))

        #
        # proper initialization of PayPalWithdraw
        self.assertIsNotNone(PayPalWithdraw(self.user))

        #
        # instantiation of CheckWithdraw object without user
        self.assertRaises(IncorrectVariableTypeException, lambda:CheckWithdraw(1))

        #
        # proper initialization of CheckWithdraw
        self.assertIsNotNone(CheckWithdraw(self.user))




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



