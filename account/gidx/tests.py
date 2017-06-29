from django.contrib.auth.models import User
from django.test import TestCase
from model_mommy import mommy

from .exceptions import (ResponseMessageException)
from .request import (
    CustomerRegistrationRequest,
    EXISTING_IDENTITY_MESSAGE
)
from .mock_response_data import (
    CUSTOMER_REGISTRATION_MATCH_RESPONSE,
    CUSTOMER_REGISTRATION_FAIL_RESPONSE,
    CUSTOMER_REGISTRATION_BAD_INPUT_RESPONSE,
    CUSTOMER_REGISTRATION_EXISTING_MATCH_RESPONSE,
)


class TestCustomerRegistrationRequest(TestCase):
    def setUp(self):
        self.user = mommy.make(
            User,
            username="automated_test_user",
            email="me@zacharywood.com"
        )

    def tearDown(self):
        self.user.delete()

    # Makes a real API call to the service. with z's real info.
    # def test_service(self):
    #     crr = CustomerRegistrationRequest(
    #         user=self.user,
    #         first_name='zachary',
    #         last_name='wood',
    #         date_of_birth='02/23/1984',
    #         ip_address='174.51.188.204'
    #     )
    #
    #     crr.send()
    #     response = crr.res_payload

    def test_response_message_exception(self):
        # None of these params matter since we never call .send().
        crr = CustomerRegistrationRequest(
            user=self.user,
            first_name='',
            last_name='',
            date_of_birth='',
            ip_address=''
        )
        crr.res_payload = CUSTOMER_REGISTRATION_BAD_INPUT_RESPONSE
        self.assertRaises(ResponseMessageException, crr.send())

    def test_is_verified_false(self):
        # None of these params matter since we never call .send().
        crr = CustomerRegistrationRequest(
            user=self.user,
            first_name='',
            last_name='',
            date_of_birth='',
            ip_address=''
        )
        crr.res_payload = CUSTOMER_REGISTRATION_MATCH_RESPONSE
        self.assertTrue(crr.is_verified())

    def test_is_verified_true(self):
        # None of these params matter since we never call .send().
        crr = CustomerRegistrationRequest(
            user=self.user,
            first_name='',
            last_name='',
            date_of_birth='',
            ip_address=''
        )
        crr.res_payload = CUSTOMER_REGISTRATION_FAIL_RESPONSE
        self.assertFalse(crr.is_verified())

    # We have been provided a valid identity, but it has already
    # been "claimed" by another user.
    def test_identity_claimed(self):
        # None of these params matter since we never call .send().
        crr = CustomerRegistrationRequest(
            user=self.user,
            first_name='',
            last_name='',
            date_of_birth='',
            ip_address=''
        )
        crr.res_payload = CUSTOMER_REGISTRATION_EXISTING_MATCH_RESPONSE
        self.assertFalse(crr.is_verified())
        self.assertEqual(crr.get_response_message(), EXISTING_IDENTITY_MESSAGE)
        self.assertNotEqual(crr.get_response_message(), '')
