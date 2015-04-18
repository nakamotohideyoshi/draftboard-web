from testfixtures import Replacer,test_datetime
from test.classes import AbstractTest
from .classes import AbstractWithdraw, PayPalWithdraw, CheckWithdraw
from mysite.exceptions import VariableNotSetException, IncorrectVariableTypeException
import datetime
from django.conf import settings
import decimal
from cash.classes import CashTransaction
class WithdrawTest(AbstractTest):
    """
    Test the :class:`cash.classes.CashWithdrawalManager` class

    TODO - need to test paypal and tax info manager working with
           the withdraw function for cash withdrawal
    """
    def setUp(self):
        self.dailyFreq = \
            settings.DFS_CASH_WITHDRAWAL_APPROVAL_REQ_DAILY_FREQ
        self.weeklyFreq = \
            settings.DFS_CASH_WITHDRAWAL_APPROVAL_REQ_WEEKLY_FREQ
        self.monthlyFreq = \
            settings.DFS_CASH_WITHDRAWAL_APPROVAL_REQ_MONTHLY_FREQ
        self.withdraw_amount = decimal.Decimal(10.00)

        self.user     = self.get_admin_user()
        r = self.move_time(days = 365, hours = 1)
        ct = CashTransaction(self.user)
        ct.deposit(1000.00)
        r.restore()


    def __make_withdrawal(self, amount, withdraw_class):
        w = withdraw_class( self.user )
        w.withdraw(amount)
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


    def test_check_withdraw(self):
       cw = self.__make_withdrawal(self.withdraw_amount, CheckWithdraw)



    # def create_max_daily_transactions(self):
    #     for count in range(self.dailyFreq-1):
    #         cm = self.__make_withdrawal(self.withdraw_amount)
    #         self.__validate_withdrawal_results(
    #             cm, -self.withdraw_amount, False, False, False,True,'')
    #
    # def create_max_weekly_transactions(self):
    #     #
    #     # moves the time back a week so we can create transactions
    #     # almost a week ago
    #     r= self.move_time(6, 4)
    #     for count in range(self.weeklyFreq-1):
    #         cm = self.__make_withdrawal(self.withdraw_amount)
    #     r.restore()
    #
    # def create_max_monthly_transactions(self):
    #     #
    #     # moves the time back a month so we can create transactions
    #     # almost a month ago
    #     r= self.move_time(29, 4)
    #     for count in range(self.monthlyFreq-1):
    #         cm = self.__make_withdrawal(self.withdraw_amount)
    #     r.restore()
    #
    # def test_daily_withdraw_limit(self):
    #     #
    #     # creates dailyFreq-1 transactions
    #     self.create_max_daily_transactions()
    #
    #     #
    #     # Now we should get a True for the flagged field
    #     withdraw_amount = decimal.Decimal(10.00)
    #     cm = self.__make_withdrawal(self.withdraw_amount)
    #     self.__validate_withdrawal_results(
    #         cm, -self.withdraw_amount, False, True, False,True,'')
    #
    # def test_weekly_withdraw_limit(self):
    #     #
    #     # creates weeklyFreq-1 transactions
    #     self.create_max_weekly_transactions()
    #
    #
    #     #
    #     # Now we should get a True for the flagged field
    #     cm = self.__make_withdrawal(self.withdraw_amount)
    #     self.__validate_withdrawal_results(
    #         cm, -self.withdraw_amount, False, True, False,True,'')
    #
    # def test_monthly_withdraw_limit(self):
    #     #
    #     # creates monthlyFreq-1 transactions
    #     self.create_max_monthly_transactions()
    #
    #
    #     #
    #     # Now we should get a True for the flagged field
    #     cm = self.__make_withdrawal(self.withdraw_amount)
    #     self.__validate_withdrawal_results(
    #         cm, -self.withdraw_amount, False, True, False,True,'')
    #
    #
    # def test_negative_withdrawal(self):
    #     self.assertRaises(
    #         transaction.exceptions.AmountNegativeException,
    #         lambda: self.__make_withdrawal(decimal.Decimal(-1))
    #     )
    # def test_zero_withdrawal(self):
    #     self.assertRaises(
    #         transaction.exceptions.AmountZeroException,
    #         lambda: self.__make_withdrawal(decimal.Decimal(0.00))
    #     )
    #
    # def test_no_user_cash_withdrawal_manager(self):
    #     self.assertRaises(
    #         cash.exceptions.IncorrectVariableTypeException,
    #         lambda: CashWithdrawalManager(1)
    #     )
