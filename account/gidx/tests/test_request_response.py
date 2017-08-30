import json

import requests
import responses
from django.contrib.auth.models import User
from django.test import TestCase
from model_mommy import mommy
from rest_framework.exceptions import (APIException, ValidationError)

from ..mock_response_data import (
    CUSTOMER_REGISTRATION_MATCH_RESPONSE,
    CUSTOMER_REGISTRATION_FAIL_RESPONSE,
    CUSTOMER_REGISTRATION_BAD_INPUT_RESPONSE,
    CUSTOMER_REGISTRATION_EXISTING_MATCH_RESPONSE,
    SERVICE_ERROR_RESPONSE,
    WEB_REG_SUCCESS_RESPONSE,
    WEBHOOK_COMPLETE,
    WEB_CASHIER_CALLBACK_SUCCESS,
    WEB_CASHIER_CALLBACK_PENDING_UNVERIFIED_IDENTITY,
)
from ..request import (
    CustomerRegistrationRequest,
    WebRegCreateSession,
    WebCashierPaymentDetailRequest,
)
from ..response import (
    CustomerRegistrationResponse,
    WebRegCreateSessionResponse,
    IdentityStatusWebhookResponse,
    DepositStatusWebhookResponse,
    is_underage,
    is_location_blocked,
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

    @responses.activate
    def test_response_message_exception(self):
        # Prepare our request with whatev junk data.
        crr = CustomerRegistrationRequest(
            user=self.user,
            first_name='',
            last_name='',
            date_of_birth='',
            ip_address=''
        )
        # Mock the response
        responses.add(
            responses.POST,
            crr.url,
            body=str(json.dumps(CUSTOMER_REGISTRATION_BAD_INPUT_RESPONSE)),
            status=200,
            content_type='application/json'
        )

        with self.assertRaises(ValidationError):
            crr.send()


class TestCustomerRegistrationResponse(TestCase):
    def setUp(self):
        self.user = mommy.make(
            User,
            username="automated_test_user",
            email="me@zacharywood.com"
        )

    def tearDown(self):
        self.user.delete()

    @responses.activate
    def test_is_existing_identity_is_valid(self):
        # Mock the response
        responses.add(
            responses.POST,
            CustomerRegistrationRequest.url,
            body=str(json.dumps(CUSTOMER_REGISTRATION_MATCH_RESPONSE)),
            status=200,
            content_type='application/json'
        )
        # get the response
        mock_response_data = requests.post(CustomerRegistrationRequest.url)
        # Pass the response to our response wrapper.
        response = CustomerRegistrationResponse(response=mock_response_data)
        # make some assertions.
        self.assertTrue(response.is_verified())

    @responses.activate
    def test_registration_fail_is_not_verified(self):
        # Mock the response
        responses.add(
            responses.POST,
            CustomerRegistrationRequest.url,
            body=str(json.dumps(CUSTOMER_REGISTRATION_FAIL_RESPONSE)),
            status=200,
            content_type='application/json'
        )
        # get the response
        mock_response_data = requests.post(CustomerRegistrationRequest.url)
        # Pass the response to our response wrapper.
        response = CustomerRegistrationResponse(response=mock_response_data)
        # make some assertions.
        self.assertFalse(response.is_verified())

    @responses.activate
    def test_service_error_throws_api_exception(self):
        # Mock the response
        responses.add(
            responses.POST,
            CustomerRegistrationRequest.url,
            body=str(json.dumps(SERVICE_ERROR_RESPONSE)),
            status=500,
            content_type='application/json'
        )
        # get the response
        mock_response_data = requests.post(CustomerRegistrationRequest.url)

        with self.assertRaises(APIException):
            response = CustomerRegistrationResponse(response=mock_response_data)

    # We have been provided a valid identity, but it has already
    # been "claimed" by another user.
    @responses.activate
    def test_identity_claimed(self):
        # Mock the response
        responses.add(
            responses.POST,
            CustomerRegistrationRequest.url,
            body=str(json.dumps(CUSTOMER_REGISTRATION_EXISTING_MATCH_RESPONSE)),
            status=200,
            content_type='application/json'
        )
        # get the response
        mock_response_data = requests.post(CustomerRegistrationRequest.url)

        # claimed identity respsones should count as being verified. we don't turn people
        # away for previously claimed ones, we flag them and investigate manually.
        response = CustomerRegistrationResponse(response=mock_response_data)
        self.assertTrue(response.is_verified())

    def test_is_underage(self):
        self.assertTrue(is_underage(['ID-UA-19']))
        self.assertTrue(is_underage(['ID-UA-19', 'OTHER_CODE']))
        self.assertFalse(is_underage(['LL-GEO-UA', 'OTHER_CODE']))

    def test_is_location_blocked(self):
        self.assertTrue(is_location_blocked(['LL-BLOCK']))
        self.assertFalse(is_location_blocked(['LL-GEO-UA']))
        self.assertTrue(is_location_blocked(['LL-BLOCK', 'LL-GEO-UA']))
        self.assertTrue(is_location_blocked(['ID-VERIFIED', 'LL-BLOCK', 'LL-GEO-UA']))


class TestWebRegCreateSessionResponse(TestCase):
    @responses.activate
    def test_gets_form_embed(self):
        # Mock the response
        responses.add(
            responses.POST,
            WebRegCreateSession.url,
            body=str(json.dumps(WEB_REG_SUCCESS_RESPONSE)),
            status=200,
            content_type='application/json'
        )
        # get the response
        mock_response_data = requests.post(WebRegCreateSession.url)

        # claimed identity respsones should count as being verified. we don't turn people
        # away for previously claimed ones, we flag them and investigate manually.
        response = WebRegCreateSessionResponse(response=mock_response_data)

        # Make sure we've parsed an embed script (or something that looks like one).
        self.assertIn(
            "<script src='https://ws.gidx-service.in/v3.0/WebSession/Registration?",
            response.get_response_message()['form_embed']
        )

        # this should always be false so check that here too.
        self.assertFalse(response.is_verified())


class TestWebhookResponse(TestCase):
    def test_sets_json_attribute(self):
        # We don't need to mock this response because it expects a dictionary rather than a
        # `requests` library response
        res = IdentityStatusWebhookResponse(WEBHOOK_COMPLETE)
        self.assertDictEqual(WEBHOOK_COMPLETE, res.json)


class TestDepositStatusWebhookResponse(TestCase):
    def test_sets_json_attribute(self):
        # We don't need to mock this response because it expects a dictionary rather than a
        # `requests` library response
        res = DepositStatusWebhookResponse(WEB_CASHIER_CALLBACK_SUCCESS)
        self.assertDictEqual(WEB_CASHIER_CALLBACK_SUCCESS, res.json)

    def test_is_successful_method(self):
        # Success
        res = DepositStatusWebhookResponse(WEB_CASHIER_CALLBACK_SUCCESS)
        self.assertEqual(True, res.is_successful())

        # Pending
        res = DepositStatusWebhookResponse(WEB_CASHIER_CALLBACK_PENDING_UNVERIFIED_IDENTITY)
        self.assertEqual(False, res.is_successful())

