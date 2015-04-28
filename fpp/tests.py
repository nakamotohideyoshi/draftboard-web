from django.test import TestCase

import mysite.exceptions
from django.contrib.auth.models import User
from django.test.client import Client
from .classes import FppTransaction
from .models import FppBalance, FppTransactionDetail, AdminFppDeposit, AdminFppWithdraw

from test.classes import AbstractTest

class TestFppTransaction(AbstractTest):

    def setUp(self):
        self.user           = self.get_admin_user()

    def test_fpp_transaction_get_balance(self):
        try:
            balance_amount = FppTransaction(self.user).get_balance_amount()
        except:
            balance_amount = None
        self.assertIsNotNone( balance_amount )
        self.assertGreaterEqual( balance_amount, 0.00 )

    def test_fpp_transaction_constructor_throws_invalid_type_exception(self):
        self.assertRaises( mysite.exceptions.IncorrectVariableTypeException,
                                            lambda: FppTransaction( 'string' ) )

    def test_fpp_transaction_deposit_invalid_type(self):
        pass # TODO

    def test_fpp_transaction_withdraw_invalid_type(self):
        pass # TODO

    def test_fpp_deposit_negative_amount(self):
        pass # TODO

    def test_fpp_deposit_zero_amount(self):
        pass # TODO

    def test_fpp_deposit_positive_amount(self):
        pass # TODO

    def test_fpp_deposit_positive_large_amount(self):
        pass # TODO

    def test_fpp_deposit_positive_very_large_amount(self):
        pass # TODO

    def test_fpp_withdraw_negative_amount(self):
        pass # TODO

    def test_fpp_withdraw_zero_amount(self):
        pass # TODO

    def test_fpp_withdraw_positive_amount(self):
        pass # TODO

    def test_fpp_withdraw_positive_large_amount(self):
        pass # TODO

    def test_fpp_withdraw_positive_very_large_amount(self):
        pass # TODO

class TestAdminPanelFppDeposit(AbstractTest):

    def setUp(self):
        self.user   = self.get_admin_user()
        self.url    = '/admin/fpp/adminfppdeposit/add/' # you can determine the url from the actual admin panel
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

    def test_admin_fpp_deposit_view_negative_amount(self):
        self.form_data = self.__get_form_data_for_amount( -10.00 )
        self.assertRaises( mysite.exceptions.AmountNegativeException,
                                    lambda: self.__login_and_post_data() )

    def test_admin_fpp_deposit_view_zero_amount(self):
        self.form_data = self.__get_form_data_for_amount( 0.00 )
        self.assertRaises( mysite.exceptions.AmountZeroException,
                                    lambda: self.__login_and_post_data() )

class TestAdminPanelFppWithdraw(AbstractTest):

    # def test_admin_fpp_deposit_view_positive_amount(self):

    # def test_admin_fpp_deposit_view_negative_amount(self):

    # def test_admin_fpp_deposit_view_zero_amount(self):

    pass # TODO ... TestAdminpanelFppWithdraw (its very similar to TestAdminPanelFppDeposit)








