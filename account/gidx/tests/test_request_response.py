import json

import requests
import responses
from django.contrib.auth.models import User
from django.test import TestCase
from model_mommy import mommy
from rest_framework.exceptions import (APIException, ValidationError)

from cash.classes import CashTransaction
from cash.models import (GidxTransaction, CashBalance)

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
    WEB_CACHIER_PAYMENT_DETAIL_REQUEST_SUCCESS,
)
from ..request import (
    CustomerRegistrationRequest,
    WebRegCreateSession,
    WebCashierPaymentDetailRequest,
    make_web_cashier_payment_detail_request,
)
from ..response import (
    CustomerRegistrationResponse,
    WebRegCreateSessionResponse,
    IdentityStatusWebhookResponse,
    GidxTransactionStatusWebhookResponse,
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
        res = GidxTransactionStatusWebhookResponse(WEB_CASHIER_CALLBACK_SUCCESS)
        self.assertDictEqual(WEB_CASHIER_CALLBACK_SUCCESS, res.json)

    def test_is_done_method(self):
        # Success
        res = GidxTransactionStatusWebhookResponse(WEB_CASHIER_CALLBACK_SUCCESS)
        self.assertEqual(True, res.is_done())

        # Pending
        res = GidxTransactionStatusWebhookResponse(WEB_CASHIER_CALLBACK_PENDING_UNVERIFIED_IDENTITY)
        self.assertEqual(False, res.is_done())


class TestPaymentDetailRequest(TestCase):
    def setUp(self):
        self.user = mommy.make(
            User,
            username="automated_test_user",
            email="zach@runitonce.com"
        )

    def tearDown(self):
        pass

    @responses.activate
    def test_make_web_cashier_payment_detail_request(self):
        # This is the easiest way to get a user's balance. don't axe me.
        dummy_transaction = CashTransaction(self.user)
        initial_balance = dummy_transaction.get_balance_amount()
        self.assertEqual(initial_balance, 0)

        # Mock the response
        responses.add(
            responses.GET,
            WebCashierPaymentDetailRequest.url,
            body=str(json.dumps(WEB_CACHIER_PAYMENT_DETAIL_REQUEST_SUCCESS)),
            status=200,
            content_type='application/json'
        )

        req = make_web_cashier_payment_detail_request(self.user, 'tid', 'sid')

        # Now test the the proper transactions and stuff were created.

        # Get any GidxTransactions that were created because of this payment.
        cash_transaction = GidxTransaction.objects.filter(
            merchant_transaction_id=WEB_CACHIER_PAYMENT_DETAIL_REQUEST_SUCCESS[
                'MerchantTransactionID'])

        # make sure at least one 'sale' transaction was created (based on the current dummy data,
        # there should be 1 since we ignore non-sale transactions)
        self.assertGreater(cash_transaction.count(), 0)
        # Now make sure the counts  match.
        self.assertEqual(cash_transaction.count(), 1)

        # Make sure the user's balance has been udpated.
        # Hard code the amount in case  something get's goofed and it ends up as 0 or something.
        new_balance = dummy_transaction.get_balance_amount()
        self.assertEqual(new_balance, 20)
        self.user.delete()

    @responses.activate
    def test_make_web_cashier_withdraw_detail_request(self):
        # This is the easiest way to get a user's balance. don't axe me.
        dummy_transaction = CashTransaction(self.user)
        initial_balance = dummy_transaction.get_balance_amount()
        self.assertEqual(initial_balance, 0)

        # Mock the response
        responses.add(
            responses.GET,
            WebCashierPaymentDetailRequest.url,
            body=str(json.dumps(WEB_CACHIER_PAYMENT_DETAIL_REQUEST_SUCCESS)),
            status=200,
            content_type='application/json'
        )

        req = make_web_cashier_payment_detail_request(self.user, 'tid', 'sid')

        # Now test the the proper transactions and stuff were created.

        # Get any GidxTransactions that were created because of this payment.
        cash_transaction = GidxTransaction.objects.filter(
            merchant_transaction_id=WEB_CACHIER_PAYMENT_DETAIL_REQUEST_SUCCESS[
                'MerchantTransactionID'])

        # make sure at least one 'sale' transaction was created (based on the current dummy data,
        # there should be 1 since we ignore non-sale transactions)
        self.assertGreater(cash_transaction.count(), 0)
        # Now make sure the counts  match.
        self.assertEqual(cash_transaction.count(), 1)

        # Make sure the user's balance has been udpated.
        # Hard code the amount in case  something get's goofed and it ends up as 0 or something.
        new_balance = dummy_transaction.get_balance_amount()
        self.assertEqual(new_balance, 20)
        self.user.delete()


class TestGidxDepositWithdraw(TestCase):
    """
    This probably doesn't belong here but it's more related to this stuff than not.

    Sometimes GIDX gives us multiple successful callbacks, so we need to make sure we aren't
    creating a transaction for each one.
    """

    def setUp(self):
        self.user = mommy.make(
            User,
            username="automated_test_user",
            email="zach@runitonce.com"
        )
        # Give this user some moneys.
        mommy.make(
            CashBalance,
            user=self.user,
            amount=999
        )

    def tearDown(self):
        pass

    def test_multiple_deposit_gidx(self):
        # Test Transaction.deposit_gidx mulitple times with the same merchant_transaction_id
        cash_trans = CashTransaction(self.user)
        mti = 'fake_transaction_id'
        cash_trans.deposit_gidx(10, mti)
        # Should be 1 transaction
        gidx_transactions = GidxTransaction.objects.filter(merchant_transaction_id=mti)
        self.assertEqual(gidx_transactions.count(), 1)

        # Now try again with the same merchant_transaction_id and it should not allow another
        # transcation to be made
        cash_trans.deposit_gidx(10, mti)
        gidx_transactions = GidxTransaction.objects.filter(merchant_transaction_id=mti)
        self.assertEqual(gidx_transactions.count(), 1)
        self.user.delete()

    def test_multiple_withdraw_gidx(self):
        # Test Transaction.deposit_gidx mulitple times with the same merchant_transaction_id
        cash_trans = CashTransaction(self.user)
        mti = 'fake_transaction_id'
        cash_trans.withdraw_gidx(10, mti)
        # Should be 1 transaction
        gidx_transactions = GidxTransaction.objects.filter(merchant_transaction_id=mti)
        self.assertEqual(gidx_transactions.count(), 1)

        # Now try again with the same merchant_transaction_id and it should not allow another
        # transcation to be made
        cash_trans.withdraw_gidx(10, mti)
        gidx_transactions = GidxTransaction.objects.filter(merchant_transaction_id=mti)
        self.assertEqual(gidx_transactions.count(), 1)
        self.user.delete()
