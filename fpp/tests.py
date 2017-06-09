from django.test import TestCase

import mysite.exceptions
from django.contrib.auth.models import User
from django.test.client import Client
from .classes import FppTransaction
from .models import FppBalance, FppTransactionDetail, AdminFppDeposit, AdminFppWithdraw

from test.classes import AbstractTest

class TestFppTransactionInitialBalance(AbstractTest):
    """
    make sure the first time we use FppTransaction the balance is 0.00 and is autocreated (no exceptions)
    """

    def setUp(self):
        super().setUp()
        self.user = self.get_admin_user()

    def test_fpp_transaction_get_balance(self):
        try:
            balance_amount = FppTransaction(self.user).get_balance_amount()
        except:
            balance_amount = None
        self.assertIsNotNone( balance_amount )
        self.assertEqual( balance_amount, 0.00 )

class TestFppTransaction(AbstractTest):
    """
    test a wide range of behaviors for FppTransaction including its constructor, deposit, and withdraw
    """
    def setUp(self):
        super().setUp()
        self.user               = self.get_admin_user()
        self.starting_balance   = self.__get_starting_balance(self.user)

        self.amount_initial         = 1000
        self.amount_zero            = 0
        self.amount_positive        = 1
        self.amount_negative        = -1
        self.amount_positive_large  = 1000000
        self.amount_negative_large  = -1000000
        self.amount_positive_xlarge = 999999999
        #self.amount_negative_xlarge = -999999999

    def __get_starting_balance(self, user):
        return FppTransaction(self.user).get_balance_amount()

    def test_fpp_transaction_constructor_throws_invalid_type_exception(self):
        self.assertRaises( mysite.exceptions.IncorrectVariableTypeException,
                                            lambda: FppTransaction( 'string' ) )

    def test_fpp_transaction_deposit_invalid_type(self):
        ft = FppTransaction( self.user )
        self.assertRaises( mysite.exceptions.IncorrectVariableTypeException,
                                                lambda: ft.deposit( 'asdf' ))

    def test_fpp_transaction_withdraw_invalid_type(self):
        ft = FppTransaction( self.user )
        self.assertRaises( mysite.exceptions.IncorrectVariableTypeException,
                                                lambda: ft.withdraw( 'asdf' ))

    def test_fpp_deposit_negative_amount(self):
        ft = FppTransaction( self.user )
        self.assertRaises( mysite.exceptions.AmountNegativeException,
                            lambda: ft.deposit( self.amount_negative ))



    def test_fpp_deposit_positive_amount(self):
        try:
            ft = FppTransaction( self.user )
            ft.deposit( self.amount_positive )
            exception = None
        except Exception as e:
            exception = e
        self.assertIsNone( exception )

    def test_fpp_deposit_positive_large_amount(self):
        try:
            ft = FppTransaction( self.user )
            ft.deposit( self.amount_positive_large )
            exception = None
        except Exception as e:
            exception = e
        self.assertIsNone( exception )

    def test_fpp_deposit_positive_very_large_amount(self):
        try:
            ft = FppTransaction( self.user )
            ft.deposit( self.amount_positive_xlarge )
            exception = None
        except Exception as e:
            exception = e
        self.assertIsNone( exception )

    def test_fpp_withdraw_negative_amount(self):
        ft = FppTransaction( self.user )
        self.assertRaises( mysite.exceptions.AmountNegativeException,
                                lambda: ft.withdraw( self.amount_negative ))



    def test_fpp_withdraw_positive_amount(self):
        fpp_initial = FppTransaction( self.user )
        fpp_initial.deposit( self.amount_initial )
        try:
            ft = FppTransaction( self.user )
            ft.withdraw( self.amount_positive )
            exception = None
        except Exception as e:
            exception = e
        self.assertIsNone( exception )

    def test_fpp_withdraw_positive_large_amount(self):
        fpp_initial = FppTransaction( self.user )
        fpp_initial.deposit( self.amount_positive_large )
        try:
            ft = FppTransaction( self.user )
            ft.withdraw( self.amount_positive_large )
            exception = None
        except Exception as e:
            exception = e
        self.assertIsNone( exception )

    def test_fpp_withdraw_positive_very_large_amount(self):
        fpp_initial = FppTransaction( self.user )
        fpp_initial.deposit( self.amount_positive_xlarge )
        try:
            ft = FppTransaction( self.user )
            ft.withdraw( self.amount_positive_xlarge )
            exception = None
        except Exception as e:
            exception = e
        self.assertIsNone( exception )

class TestAdminPanelFppDeposit(AbstractTest):

    def setUp(self):
        super().setUp()
        self.user   = self.get_admin_user()
        self.url    = '/thinking_face/fpp/adminfppdeposit/add/' # you can determine the url from the actual admin panel
        self.client = Client()
        if not self.client.login( username=self.user.username, password=self.get_password() ):
            #
            # this is not an invalid test but it should be able to login
            raise Exception( type(self).__name__ + ' client couldnt login for some reason' )
        self.form_data = None # set in each method

    def __get_form_data_for_amount(self, amount):
        d = {
            'user'      : self.user.pk,
            'reason'    : 'testing-%s' % self.__class__.__name__,
            'amount'    : amount
        }
        return d

    def __login_and_post_data(self):
        # confirm again the person we think is logged in really is:
        logged_in_user_id = None
        for tup in self.client.session.items():
            if tup[0] == '_auth_user_id':
                logged_in_user_id = tup[1]

        #
        # compare the person whos logged in to the person we think is logged in
        self.assertEquals( logged_in_user_id, '%s' % str(self.user.pk) )
        response = self.client.post( self.url, self.form_data )
        return response

    def test_admin_fpp_deposit_view_positive_amount(self):
        self.form_data = self.__get_form_data_for_amount( 10.00 )
        response = self.__login_and_post_data()
        self.assertLess( response.status_code, 400 ) # make sure its not a straight up error

        #
        # check if there are ANY new AdminCashDeposits in the database
        acds = AdminFppDeposit.objects.all()
        #print('%s - total AdminFppDeposit objects in database' % (str(len(acds))) )
        self.assertEqual( len(acds), 1 )   ### we only expect one item here, because no existing data should exist

        # retrieve it by everything we used to set it
        acd = AdminFppDeposit.objects.all()[0]

        self.assertEqual( acd.user.pk, self.form_data['user'] )
        self.assertEqual( acd.amount, self.form_data['amount'] )
        self.assertEqual( acd.reason, self.form_data['reason'] )








