from django.test import TestCase

import mysite.exceptions
from django.test.client import Client
from .classes import BonusCashTransaction
from .models import BonusCashBalance, BonusCashTransactionDetail, AdminBonusCashDeposit, AdminBonusCashWithdraw

from test.classes import AbstractTest

class TestBonusCashTransactionInitialBalance(AbstractTest):
    """
    make sure the first time we use BonusCashTransaction the balance is 0.00 and is autocreated (no exceptions)
    """

    def setUp(self):
        self.user = self.get_admin_user()

    def test_bonuscash_transaction_get_balance(self):
        try:
            balance_amount = BonusCashTransaction(self.user).get_balance_amount()
        except:
            balance_amount = None
        self.assertIsNotNone( balance_amount )
        self.assertEqual( balance_amount, 0.00 )

class TestBonusCashTransaction(AbstractTest):
    """
    test a wide range of behaviors for BonusCashTransaction including its constructor, deposit, and withdraw
    """
    def setUp(self):
        self.user               = self.get_admin_user()
        self.starting_balance   = self.__get_starting_balance(self.user)

    def __get_starting_balance(self, user):
        return BonusCashTransaction(self.user).get_balance_amount()

    def test_bonuscash_transaction_constructor_throws_invalid_type_exception(self):
        self.assertRaises( mysite.exceptions.IncorrectVariableTypeException,
                                            lambda: BonusCashTransaction( 'string' ) )

    def test_bonuscash_transaction_deposit_invalid_type(self):
        pass # TODO

    def test_bonuscash_transaction_withdraw_invalid_type(self):
        pass # TODO

    def test_bonuscash_deposit_negative_amount(self):
        pass # TODO

    def test_bonuscash_deposit_zero_amount(self):
        pass # TODO

    def test_bonuscash_deposit_positive_amount(self):
        pass # TODO

    def test_bonuscash_deposit_positive_large_amount(self):
        pass # TODO

    def test_bonuscash_deposit_positive_very_large_amount(self):
        pass # TODO

    def test_bonuscash_withdraw_negative_amount(self):
        pass # TODO

    def test_bonuscash_withdraw_zero_amount(self):
        pass # TODO

    def test_bonuscash_withdraw_positive_amount(self):
        pass # TODO

    def test_bonuscash_withdraw_positive_large_amount(self):
        pass # TODO

    def test_bonuscash_withdraw_positive_very_large_amount(self):
        pass # TODO

#
# Using RequestFactory to test views:
#    https://docs.djangoproject.com/en/1.8/topics/testing/advanced/
#
# from django.contrib.auth.models import AnonymousUser, User
# from django.test import TestCase, RequestFactory
#
# from .views import my_view
#
# class SimpleTest(TestCase):
#     def setUp(self):
#         # Every test needs access to the request factory.
#         self.factory = RequestFactory()
#         self.user = User.objects.create_user(
#             username='jacob', email='jacob@…', password='top_secret')
#
#     def test_details(self):
#         # Create an instance of a GET request.
#         request = self.factory.get('/customer/details')
#
#         # Recall that middleware are not supported. You can simulate a
#         # logged-in user by setting request.user manually.
#         request.user = self.user
#
#         # Or you can simulate an anonymous user by setting request.user to
#         # an AnonymousUser instance.
#         request.user = AnonymousUser()
#
#         # Test my_view() as if it were deployed at /customer/details
#         response = my_view(request)
#         self.assertEqual(response.status_code, 200)

class TestAdminPanelBonusCashDeposit(AbstractTest):

    def setUp(self):
        self.user   = self.get_admin_user()
        self.url    = '/admin/bonuscash/adminbonuscashdeposit/add/' # you can determine the url from the actual admin panel
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

    def test_admin_bonuscash_deposit_view_positive_amount(self):
        self.form_data = self.__get_form_data_for_amount( 10.00 )
        response = self.__login_and_post_data()
        self.assertLess( response.status_code, 400 ) # make sure its not a straight up error

        #
        # check if there are ANY new AdminCashDeposits in the database
        acds = AdminBonusCashDeposit.objects.all()
        #print('%s - total AdminBonusCashDeposit objects in database' % (str(len(acds))) )
        self.assertEqual( len(acds), 1 )   ### we only expect one item here, because no existing data should exist

        # retrieve it by everything we used to set it
        acd = AdminBonusCashDeposit.objects.all()[0]

        self.assertEqual( acd.user.pk, self.form_data['user'] )
        self.assertEqual( acd.amount, self.form_data['amount'] )
        self.assertEqual( acd.reason, self.form_data['reason'] )

    def test_admin_bonuscash_deposit_view_negative_amount(self):
        self.form_data = self.__get_form_data_for_amount( -10.00 )
        self.assertRaises( mysite.exceptions.AmountNegativeException,
                                    lambda: self.__login_and_post_data() )

    def test_admin_bonuscash_deposit_view_zero_amount(self):
        self.form_data = self.__get_form_data_for_amount( 0.00 )
        self.assertRaises( mysite.exceptions.AmountZeroException,
                                    lambda: self.__login_and_post_data() )

class TestAdminPanelBonusCashWithdraw(AbstractTest):

    # def test_admin_bonuscash_deposit_view_positive_amount(self):

    # def test_admin_bonuscash_deposit_view_negative_amount(self):

    # def test_admin_bonuscash_deposit_view_zero_amount(self):

    pass # TODO ... TestAdminpanelBonusCashWithdraw (its very similar to TestAdminPanelBonusCashDeposit)








