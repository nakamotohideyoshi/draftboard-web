import json
from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, User
from django.test import Client
from django.test import RequestFactory
from django.test import TestCase
from django.test.utils import override_settings
from rest_framework import status
from rest_framework.test import APITestCase

from account import const as _account_const
from account.models import (Identity)
from account.models import (UserLog)
from account.utils import CheckUserAccess
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
from test.classes import (
    MasterAbstractTest,  # has get_user() method
    ForceAuthenticateAndRequestMixin,
)


class AccountsViewsTest(TestCase):
    def setUp(self):
        super().setUp()
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
        }
        password_short = {
            'email': 'user@test.com',
            'username': 'user',
            'password': 'pass',
        }
        proper_data = {
            'username': 'user',
            'email': "user@test.com",
            'password': 'password',
        }

        url = '/api/account/register/'

        # Tests for invalid password
        response = self.client.post(url, invalid_password_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Tests for missing password field
        response = self.client.post(url, missing_password_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # short password field
        response = self.client.post(url, password_short, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Tests for invalid username
        response = self.client.post(url, invalid_username_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Tests for missing username field
        response = self.client.post(url, missing_username_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Tests for invalid email data
        response = self.client.post(url, invalid_email_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Tests for missing email data
        response = self.client.post(url, missing_email_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # we no longer require password confirm fields
        # Tests for mismatched passwords
        # response = self.client.post(url, password_mismatch, format='json')
        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Tests for proper creation
        response = self.client.post(url, proper_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Hit the log out page, since creation auto logs in
        self.client.get('/logout/')

        # Tests for duplicates
        response = self.client.post(url, proper_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


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


class AddSavedCardAPI_TestMissingInformation(
    APITestCaseMixin, MasterAbstractTest, ForceAuthenticateAndRequestMixin):
    def setUp(self):
        super().setUp()
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


class AddSavedCardAPI_TestEmptyPostParams(
    APITestCaseMixin, MasterAbstractTest, ForceAuthenticateAndRequestMixin):
    def setUp(self):
        super().setUp()
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


class CheckUserAccessTest(TestCase, MasterAbstractTest):
    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()
        self.blocked_ip = '66.228.119.72'
        self.blocked_ip_country = '194.44.221.54'
        self.available_ip = '72.229.28.185'
        self.user = self.get_user_with_account_information('user_withinformation')

    @override_settings(
        BLOCKED_COUNTRIES_CODES=['UA'],
    )
    def test_checker_failure(self):
        # A request with the blocked state IP
        blocked_request = self.factory.get('/', REMOTE_ADDR=self.blocked_ip)
        blocked_request.user = self.user
        # A request with the blocked country IP
        blocked_country_request = self.factory.get('/', REMOTE_ADDR=self.blocked_ip_country)
        blocked_country_request.user = self.user

        # Make sure the blocked country request fails.
        checker = CheckUserAccess(blocked_country_request)
        self.assertFalse(checker.check_location_country()[0])

        # Make sure the blocked state request fails.
        checker = CheckUserAccess(blocked_request)
        self.assertFalse(checker.check_location_state()[0])

    def test_checker_ok(self):
        # A valid request
        valid_request = self.factory.get('/', REMOTE_ADDR=self.available_ip)
        valid_request.user = self.user

        # Make sure a valid request passes.
        checker = CheckUserAccess(valid_request)
        self.assertTrue(checker.check_location_country()[0])
        self.assertTrue(checker.check_location_state()[0])
        self.assertTrue(checker.check_for_vpn()[0])

    def test_check_invalid_location_age(self):
        # Test that a user NOT old enough cannnot access the site.
        invalid_request = self.factory.get('/', REMOTE_ADDR=self.available_ip)
        # This user is too young to use the site.
        Identity(
            user=self.user,
            dob=date(2015, 1, 1),
        )
        invalid_request.user = self.user

        checker = CheckUserAccess(request=invalid_request)
        checker.check_location_age('CO')
        self.assertFalse(checker.check_location_age('CO')[0])

        # give the user bypass permisison and make sure it works.
        perm = Permission.objects.get(codename='can_bypass_age_check')
        self.user.user_permissions.add(perm)
        # clear the user's permission cache by re-fetching the user
        self.user = User.objects.get(username=self.user)
        # Re-set the user + checker
        invalid_request.user = self.user
        checker = CheckUserAccess(request=invalid_request)
        checker.check_location_age('CO')
        self.assertTrue(checker.check_location_age('CO')[0])
        # Remove the permission
        self.user.user_permissions.remove(perm)
        self.user = User.objects.get(username=self.user)

    def test_check_valid_location_age(self):
        # Test that a user old enough can access the site.
        valid_request = self.factory.get('/', REMOTE_ADDR=self.available_ip)
        # This user is old enough to use the site.
        Identity(
            user=self.user,
            dob=date(1984, 1, 1),
        )
        valid_request.user = self.user

        checker = CheckUserAccess(request=valid_request)
        checker.check_location_age('CO')
        self.assertTrue(checker.check_location_age('CO')[0])

        # give the user bypass permisison and make sure it works.
        perm = Permission.objects.get(codename='can_bypass_age_check')
        self.user.user_permissions.add(perm)
        # clear the user's permission cache by re-fetching the user
        self.user = User.objects.get(username=self.user)

        # Re-set the user + checker
        valid_request.user = self.user
        checker = CheckUserAccess(request=valid_request)
        checker.check_location_age('CO')
        self.assertTrue(checker.check_location_age('CO')[0])


class UserLogModelTest(TestCase):
    # Basic test to ensure UserLogs can be created
    def test_create_user_log(self):
        UserModel = get_user_model()

        user = UserModel.objects.create_user(
            username='ppgogo',
            password='ppgogo_rules',
            email='ppgogo@draftboard.com'
        )

        # Create a user login log.
        UserLog.objects.create(
            type=_account_const.AUTHENTICATION,
            ip='127.0.0.1',
            user=user,
            action=_account_const.LOGIN,
            metadata=json.dumps({'test_key': 'test_value'})
        )
