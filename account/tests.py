from .classes import AccountInformation
from .exceptions import AccountInformationException
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import Client
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from test.classes import (
    AbstractTest,
    MasterAbstractTest,                 # has get_user() method
    ForceAuthenticateAndRequestMixin,
)
from account.views import (
    # PayPalDepositWithPayPalAccountAPIView,
    # PayPalDepositWithPayPalAccountSuccessAPIView,
    # PayPalDepositWithPayPalAccountFailAPIView,
    # PayPalDepositCreditCardAPIView,
    # PayPalDepositSavedCardAPIView,
    PayPalSavedCardAddAPIView,
    # PayPalSavedCardDeleteAPIView,
    # PayPalSavedCardListAPIView,
)


class AccountsViewsTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_default_password_change_view_inaccessible(self):
        # Make sure the default django password change views do not exist
        response = self.client.get('/password/change/')
        self.assertEqual(
            response.status_code,
            404,
            "Django default password reset view is accessible."
        )

        response = self.client.get('/password/change/done/')
        self.assertEqual(
            response.status_code,
            404,
            "Django default password reset done view is accessible."
        )

    # TODO figure out how to ignore whitenoise errors

    # def test_password_reset_page_renders(self):
    #     response = self.client.get('/password/reset/')
    #     self.assertEqual(
    #         response.status_code,
    #         200,
    #         "Password reset page is not accessible."
    #     )

    # def test_password_reset_done_page_renders(self):
    #     response = self.client.get('/password/reset/done/')
    #     self.assertEqual(
    #         response.status_code,
    #         200,
    #         "Password reset done page is not accessible."
    #     )

    # def test_login_page_renders(self):
    #     response = self.client.get(reverse('login'))
    #     self.assertEqual(
    #         response.status_code,
    #         200,
    #         "Login page is not accessible."
    #     )

    def test_logout_page_logs_user_out(self):
        UserModel = get_user_model()
        # add phil so that the new user can follow him
        UserModel.objects.create_user(
            username='ppgogo',
            password='ppgogo_rules',
            email='ppgogo@draftboard.com'
        )
        user = UserModel.objects.create_user(
            username='kreg',
            password='kreg_smells',
            email='devs@draftboard.com'
        )

        self.logged_in = self.client.login(username=user.username, password='kreg_smells')
        self.assertTrue(self.logged_in, "User not able to be logged in.")
        # Make sure they're logged in.
        self.assertIn('_auth_user_id', self.client.session, "User was not logged in")

        # Hit the log out page.
        self.client.get('/logout/')
        # Make sure they're logged out.
        self.assertNotIn('_auth_user_id', self.client.session, "Logout page does not log out user.")


# Notes:
# rest_framework.status has these helper methods (which all return a boolean):
# is_informational()  # 1xx
# is_success()        # 2xx
# is_redirect()       # 3xx
# is_client_error()   # 4xx
# is_server_error()   # 5xx

class RegisterAccountTest(APITestCase):

    def test_api(self):
        invalid_password_data = {
            'username': 'user',
            'email': 'user@test.com',
            'password': '',
        }
        missing_password_data = {
            'username': 'user',
            'email': "user@test.com",
        }
        invalid_username_data = {
            'username': '',
            'email': "user@test.com",
            'password': 'password',
        }
        missing_username_data = {
            'email': "user@test.com",
            'password': 'password',
        }
        invalid_email_data = {
            'username': 'user',
            'email': "usertest.com",
            'password': 'password',
        }
        missing_email_data = {
            'username': 'user',
            'password': 'password',
        }
        password_mismatch = {
            'email': 'user@test.com',
            'username': 'user',
            'password': 'password',
            'password_confirm': 'not_same',
        }
        proper_data = {
            'username': 'user',
            'email': "user@test.com",
            'password': 'password',
            'password_confirm': 'password',
        }

        url = '/api/account/register/'

        #
        # Tests for invalid password
        response = self.client.post(url, invalid_password_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #
        # Tests for missing password field
        response = self.client.post(url, missing_password_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #
        # Tests for invalid username
        response = self.client.post(url, invalid_username_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #
        # Tests for missing username field
        response = self.client.post(url, missing_username_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #
        # Tests for invalid email data
        response = self.client.post(url, invalid_email_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #
        # Tests for missing email data
        response = self.client.post(url, missing_email_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #
        # Tests for mismatched passwords
        response = self.client.post(url, password_mismatch, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #
        # Tests for proper creation
        response = self.client.post(url, proper_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Hit the log out page, since creation auto logs in
        self.client.get('/logout/')

        #
        # Tests for duplicates
        response = self.client.post(url, proper_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AccountInformationTest(AbstractTest):

    def setUp(self):
        from django.conf import settings
        self.db = settings.DATABASES['default'].get('NAME')
        print('account app db name: %s' % str(self.db))
        self.user = self.get_admin_user()

    def should_fail_validate_mailing_address(self, information):
        self.assertRaises(
            AccountInformationException,
            lambda: information.validate_mailing_address()
        )

    def test_validate_mailing_address_missing_all_fields(self):
        information = AccountInformation(self.user)
        self.should_fail_validate_mailing_address(information)

        #
        # Working Fields
        information.set_fields(
            fullname='Ryan',
            address1='address1',
            city='city',
            state='NH',
            zipcode='03820'
        )
        information.validate_mailing_address()

        #
        # missing fullname
        information.set_fields(
            fullname='',
            address1='address1',
            city='city',
            state='NH',
            zipcode='03820'
        )
        self.should_fail_validate_mailing_address(information)

        #
        # missing address1
        information.set_fields(
            fullname='Ryan',
            address1='',
            city='city',
            state='NH',
            zipcode='03820'
        )
        self.should_fail_validate_mailing_address(information)

        #
        # missing city
        information.set_fields(
            fullname='Ryan',
            address1='address1',
            city='',
            state='NH',
            zipcode='03820'
        )
        self.should_fail_validate_mailing_address(information)

        #
        # missing state
        information.set_fields(
            fullname='Ryan',
            address1='address1',
            city='city',
            state='',
            zipcode='03820'
        )
        self.should_fail_validate_mailing_address(information)

        #
        # missing zipcode
        information.set_fields(
            fullname='Ryan',
            address1='address1',
            city='city',
            state='NH',
            zipcode=''
        )
        self.should_fail_validate_mailing_address(information)


class APITestCaseMixin(APITestCase):
    """
    provides print_response just while were setting up tests to help print the response
    and help diagnose problems
    """

    def print_response(self, response):
        status_code = response.status_code
        data = response.data
        print('HTTP [%s] %s' % (status_code, str(data)))


class PayWithCreditCardAPITest(APITestCase, MasterAbstractTest, ForceAuthenticateAndRequestMixin):
    pass  # TODO


class AddSavedCardAPI_TestMissingInformation(APITestCaseMixin, MasterAbstractTest, ForceAuthenticateAndRequestMixin):

    def setUp(self):
        # the view class
        self.view = PayPalSavedCardAddAPIView
        # the url of the endpoint and a default user
        self.url = '/api/account/paypal/saved-card/add/'
        self.user = self.get_user('user_missinginformation')

    def test_1(self):
        # double quotes is real JSON, single quotes will make it unhappy
        # data = {
        #     "type":"visa",
        #     "number":"4032036765082399",
        #     "exp_month":"12",
        #     "exp_year":"2020",
        #     "cvv2":"012"
        # }

        data = {}
        response = self.force_authenticate_and_POST(self.user, self.view, self.url, data)

        self.print_response(response)

        # is_client_error() checks any 400 errors (401, 402, etc...)
        self.assertTrue(status.is_client_error(response.status_code))


class AddSavedCardAPI_TestEmptyPostParams(APITestCaseMixin, MasterAbstractTest, ForceAuthenticateAndRequestMixin):

    def setUp(self):
        # the view class
        self.view = PayPalSavedCardAddAPIView
        # the url of the endpoint and a default user
        self.url = '/api/account/paypal/saved-card/add/'
        self.user = self.get_user_with_account_information('user_withinformation')

    def test_1(self):
        data = {}

        response = self.force_authenticate_and_POST(self.user, self.view, self.url, data)
        self.print_response(response)
        # is_client_error() checks any 400 errors (401, 402, etc...)
        self.assertTrue(status.is_client_error(response.status_code))

# class AddSavedCardAPI_TestEmptyPostParams(APITestCaseMixin, MasterAbstractTest, ForceAuthenticateAndRequestMixin):
#
#     def setUp(self):
#         # the view class
#         self.view = PayPalSavedCardAddAPIView
#         # the url of the endpoint and a default user
#         self.url = '/api/account/paypal/saved-card/add/'
#         self.user = self.get_user_with_account_information('userWithInformation')
#
#     def test_1(self):
#         data = {}
#
#         response = self.force_authenticate_and_POST(self.user, self.view, self.url, data )
#         self.print_response(response)
#         # is_client_error() checks any 400 errors (401, 402, etc...)
#         self.assertTrue(status.is_client_error(response.status_code))
