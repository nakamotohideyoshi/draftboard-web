import copy
import json
import uuid
from logging import getLogger

import requests
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from raven.contrib.django.raven_compat.models import client
from rest_framework.exceptions import (APIException, ValidationError)

from cash.classes import CashTransaction
from mysite.celery_app import app
from transaction.tasks import send_deposit_receipt
from .models import GidxSession
from .response import (CustomerRegistrationResponse, WebRegCreateSessionResponse)

logger = getLogger('account.gidx.request')

# We don't want to log or save these fields in our request logs.
REQUEST_FIELD_BLACKLIST = ['FirstName', 'LastName', 'DateOfBirth']


def get_short_uuid():
    """
    Paypal only supports 30 char transaction ID limit, so if we use our
    GIDX_MERCHANT_SESSION_ID_PREFIX and a uuid, it's too dang long. this will crete a uuid4
    but only return a chunk of it.
    :return:
    """
    return str(uuid.uuid4())[:18]


def get_user_from_session_id(session_id):
    """
    If we have a session_id, and need to find the user that is associated with that session, this
    will find the GidxSession that matches and returns the user.

     This is necessary because GIDX callback webhooks do not include any user identifier, only
     session_ids.

    :param session_id:
    :return: User
    """
    # I'm pretty sure there shouldn't be more than one with a specific ID, but grab the latest
    # just in case.
    last_session = GidxSession.objects.filter(session_id=session_id).latest()
    if last_session:
        return last_session.user

    raise Exception('No User could be found from session_id: %s' % session_id)


def get_webhook_base_url():
    """
    If we have a specific domain in our settings (probably for local dev), return that.
    Otherwise, use our site's DOMAIN setting to build a url.
    :return: string
    """
    if hasattr(settings, 'GIDX_WEBHOOK_URL'):
        return settings.GIDX_WEBHOOK_URL
    return 'https://%s' % settings.DOMAIN


def get_customer_id_for_user(user):
    """
    If we have already saved a customer id, send that one back.
    If not, generate a new, deterministic one based on their username + id.
    This should probably make username changes ok.

    :param user:
    :return: string
    """
    try:
        return user.identity.gidx_customer_id
    except ObjectDoesNotExist:
        pass

    return "%s%s--%012d" % (
        settings.GIDX_CUSTOMER_ID_PREFIX, user.username, user.id)


def strip_sensitive_fields(params):
    """
    Used on request params, this returns a new dict of the params, with the REQUEST_FIELD_BLACKLIST
    replaced with "*****" filler text.
    :param params:
    :return:
    """
    clean_params = copy.deepcopy(params)

    for (key, value) in clean_params.items():
        if key in REQUEST_FIELD_BLACKLIST:
            clean_params[key] = '*****'
    return clean_params


class GidxRequest(object):
    user = None
    url = None
    service_type = None
    response_wrapper = None
    responseClass = None
    action_name = None
    # Extra params that subclasses can fill up.
    params = {}
    # Params that are required for every API request.
    base_params = {
        # Your assigned ApiKey, provided to you by the GIDX team.
        'ApiKey': settings.GIDX_API_KEY,
        # Your assigned Merchant ID, provided to you by the GIDX team.
        'MerchantID': settings.GIDX_MERCHANT_ID,
        # Your assigned ID for merchant product type.
        'ProductTypeID': settings.GIDX_PRODUCT_ID,
        # Your assigned ID for this specific customer device type.
        'DeviceTypeID': settings.GIDX_DEVICE_ID,
        # Your assigned ID for this specific customer activity type.
        'ActivityTypeID': settings.GIDX_ACTIVITY_ID,
    }

    def validate_params(self):
        """
        Run through each param and ensure it is not None.
        :return:
        """
        for param, value in self.params.items():
            if value is None or value == '':
                raise ValidationError('%s must be provided.' % param)

    def _send(self):
        # Do a simple `None` check on all params
        self.validate_params()

        # Make the request!
        res = requests.post(
            self.url,
            data=json.dumps(self.params),
            headers={'content-type': 'application/json'}
        )

        # Save the response. This will do some basic response error handling.
        self.response_wrapper = self.responseClass(
            response=res,
            params=self.params,
            url=self.url,
        )
        self.handle_response()

        # Return the response wrapper.
        return self.response_wrapper

    def handle_response(self):
        # Log out the req + res
        logger.info({
            'url': self.url,
            "action": self.action_name,
            "request": self.params,
            "response": self.response_wrapper.json,
        })

        ip_address = self.params.get('DeviceIpAddress') or self.params.get('CustomerIpAddress')

        # Save our session info
        GidxSession.objects.create(
            user=self.user,
            gidx_customer_id=self.params.get('MerchantCustomerID'),
            session_id=self.params.get('MerchantSessionID'),
            service_type=self.service_type,
            device_location=ip_address,
            request_data=strip_sensitive_fields(self.params),
            response_data=self.response_wrapper.json,
            reason_codes=self.response_wrapper.json.get('ReasonCodes', None),
        )

        # 500+ means some kind of service-level error. make sure we get notified about these.
        if self.response_wrapper.json['ResponseCode'] >= 500:
            logger.error({
                'url': self.url,
                "action": "%s%s" % (self.action_name, '--FAIL'),
                "request": self.params,
                "response": self.response_wrapper.response.text,
            })
            # Send some useful information to Sentry.
            client.context.merge({'extra': {
                'response_json': self.response_wrapper.json,
                'response_text': self.response_wrapper.response.text,
                'params': self.params,
                'url': self.url,
            }})
            client.captureMessage(
                "GIDX request failed - %s" % self.response_wrapper.json['ResponseMessage'])
            client.context.clear()

            raise ValidationError(detail='%s' % self.response_wrapper.json['ResponseMessage'])

        # a ResponseCode of 0 indicates no errors. If we had errors, raise an exception that can
        # be caught on the view layer.
        if not self.response_wrapper.json['ResponseCode'] == 0:
            logger.warning(self.response_wrapper.json)
            raise ValidationError(detail='%s' % self.response_wrapper.json['ResponseMessage'])


class CustomerRegistrationRequest(GidxRequest):
    """
     This method should be called to register the customer within the GIDX system and find
     verify a match to their identity.
    """
    url = 'https://api.gidx-service.in/v3.0/api/CustomerIdentity/CustomerRegistration'
    service_type = 'CustomerRegistration'
    responseClass = CustomerRegistrationResponse
    action_name = "CUSTOMER_REGISTRATION_REQUEST"

    def __init__(self, user, first_name, last_name, date_of_birth, ip_address):
        # Bail immediately if we have no logged-in user.
        if user is None or not user.is_authenticated():
            raise APIException('Authenticated user must be provided. - %s' % user)

        self.user = user

        args = {
            # A unique SessionID from your system assigned to this active session.
            'MerchantSessionID': '%s%s' % (
            settings.GIDX_MERCHANT_SESSION_ID_PREFIX, get_short_uuid()),
            # IP address for the current device (The Customers' Device – NOT your servers
            # IP address) for this active session.
            'DeviceIpAddress': ip_address,
            # Your unique ID for this customer.
            'MerchantCustomerID': get_customer_id_for_user(user),
            'FirstName': first_name,
            'LastName': last_name,
            'EmailAddress': user.email,
            # 04/03/1984 (In MM/DD/YYYY Format)
            'DateOfBirth': date_of_birth,
            # I can't for the life of me get reverse() to work here. I am sorry.
            'CallbackURL': '%s%s' % (get_webhook_base_url(), '/api/account/identity-webhook/'),
        }

        # Combine the base parameters and the supplied arguments into a single dict that
        # we can pass as POST parameters.
        self.params.update(self.base_params)
        self.params.update(args)

    def send(self):
        # Call the parent's _send, it does the actual work.
        response = self._send()

        # Now do any response handling.
        if ('ProfileMatches' in self.response_wrapper.json and len(
                self.response_wrapper.json['ProfileMatches']) == 0):
            logger.warning('No profile match found!')

        return response


class RegistrationStatusRequest(GidxRequest):
    """
    Check the status of a user's registration.
    (http://www.tsevo.com/Docs/WebReg)
    """
    url = 'https://api.gidx-service.in/v3.0/api/WebReg/RegistrationStatus'
    service_type = 'RegistrationStatus'
    responseClass = CustomerRegistrationResponse
    action_name = "REGISTRATION_STATUS_REQUEST"

    def __init__(self, user, merchant_session_id):
        self.user = user

        args = {
            'MerchantSessionID': merchant_session_id,
        }

        # Combine the base parameters and the supplied arguments into a single dict that
        # we can pass as POST parameters.
        self.params.update(self.base_params)
        self.params.update(args)

    def send(self):
        # Call the parent's _send, it does the actual work.
        return self._send()

    # We have to override this becase this reqeust is a GET. the default is POST
    def _send(self):
        # Do a simple `None` check on all params
        self.validate_params()
        # Make the request!
        res = requests.get(self.url, self.params)
        # Save the response. This will do some basic response error handling.
        self.response_wrapper = self.responseClass(response=res, params=self.params, url=self.url)
        self.handle_response()

        # Return the response wrapper.
        return self.response_wrapper

    def handle_response(self):

        # Log out the req + res
        logger.info({
            'url': self.url,
            "action": self.action_name,
            "request": self.params,
            "response": self.response_wrapper.json,
        })

        # 500+ means some kind of service-level error. make sure we get notified about these.
        if self.response_wrapper.json['ResponseCode'] >= 500:
            logger.error({
                'url': self.url,
                "action": "%s%s" % (self.action_name, '--FAIL'),
                "request": self.params,
                "response": '%s - %s' % (
                    self.response_wrapper, self.response_wrapper.response.text),
            })
            # Send some useful information to Sentry.
            client.context.merge({'extra': {
                'response_json': self.response_wrapper.json,
                'response_text': self.response_wrapper.response.text,
                'params': self.params,
                'url': self.url,
            }})
            client.captureMessage(
                "GIDX request failed - REGISTRATION_STATUS_REQUEST")
            client.context.clear()

            raise ValidationError(
                detail='%s' % self.response_wrapper.json['RegistrationStatusMessage'])

        # a ResponseCode of 0 indicates no errors. If we had errors, raise an exception that can
        # be caught on the view layer.
        if not self.response_wrapper.json['ResponseCode'] == 0:
            logger.warning(self.response_wrapper.json)
            raise ValidationError(
                detail='%s' % self.response_wrapper.json['RegistrationStatusMessage'])


class WebRegCreateSession(GidxRequest):
    """
    If we fail to identify the user with a CustomerRegistrationRequest, we make this request
    which returns a JS snippet that will embed a hosted form for additional user info.

    (http://www.tsevo.com/Docs/WebReg#MethodRef_ID_CreateSession)
    """
    url = 'https://api.gidx-service.in/v3.0/api/WebReg/CreateSession'
    service_type = 'WebReg_CreateSession'
    responseClass = WebRegCreateSessionResponse
    action_name = "WEB_REG_CREATE_SESSION_REQUEST"

    def __init__(self, user, first_name, last_name, date_of_birth, ip_address):
        # Bail immediately if we have no logged-in user.
        if user is None or not user.is_authenticated():
            raise APIException('Authenticated user must be provided. - %s' % user)

        self.user = user

        args = {
            # A unique SessionID from your system assigned to this active session.
            'MerchantSessionID': '%s%s' % (
            settings.GIDX_MERCHANT_SESSION_ID_PREFIX, get_short_uuid()),
            # IP address for the current device (The Customers' Device – NOT your servers
            # IP address) for this active session.
            'CustomerIpAddress': ip_address,
            # Your unique ID for this customer.
            'MerchantCustomerID': get_customer_id_for_user(user),
            'FirstName': first_name,
            'LastName': last_name,
            'EmailAddress': user.email,
            # 04/03/1984 (In MM/DD/YYYY Format)
            'DateOfBirth': date_of_birth,
        }

        # Combine the base parameters and the supplied arguments into a single dict that
        # we can pass as POST parameters.
        self.params.update(self.base_params)
        self.params.update(args)

    def send(self):
        # Call the parent's _send, it does the actual work.
        return self._send()


class WebCashierCreateSession(GidxRequest):
    """
     This method should be called to create a new Cashier Web Session within the GIDX system for
     payments.

     The response from this request will contain a <script> tag to embed on the client in order
     to initiate the gidx payment interface.

     http://www.tsevo.com/Docs/WebCashier#MethodRef_ID_CreateSession
    """

    url = 'https://api.gidx-service.in/v3.0/api/WebCashier/CreateSession'
    service_type = 'WebCashier_CreateSession'
    responseClass = WebRegCreateSessionResponse
    action_name = "WEB_CACHIER_CREATE_SESSION_REQUEST"

    def __init__(self, user, ip_address):
        # Bail immediately if we have no logged-in user.
        if user is None or not user.is_authenticated():
            raise APIException('Authenticated user must be provided. - %s' % user)

        self.user = user

        args = {
            # A unique SessionID from your system assigned to this active session.
            'MerchantSessionID': '%s%s' % (
            settings.GIDX_MERCHANT_SESSION_ID_PREFIX, get_short_uuid()),
            # IP address for the current device (The Customers' Device – NOT your servers
            # IP address) for this active session.
            'CustomerIpAddress': ip_address,
            # Your unique ID for this customer.
            'MerchantCustomerID': get_customer_id_for_user(user),
            'PayActionCode': 'PAY',
            'MerchantTransactionID': get_short_uuid(),
            'MerchantOrderID': get_short_uuid(),
            # I can't for the life of me get reverse() to work here. I am sorry.
            'CallbackURL': '%s%s' % (get_webhook_base_url(), '/api/account/deposit-webhook/'),
        }

        # Combine the base parameters and the supplied arguments into a single dict that
        # we can pass as POST parameters.
        self.params.update(self.base_params)
        self.params.update(args)

    def send(self):
        # Call the parent's _send, it does the actual work.
        return self._send()


class WebCashierPaymentDetailRequest(GidxRequest):
    """
    Get the details for a transaction.

     http://www.tsevo.com/Docs/WebCashier#MethodRef_ID_PaymentDetail
    """

    url = 'https://api.gidx-service.in/v3.0/api/WebCashier/PaymentDetail'
    service_type = 'WebCashier_PaymentDetail'
    responseClass = WebRegCreateSessionResponse
    action_name = "WEB_CACHIER_PAYMENT_DETAIL_REQUEST"

    def __init__(self, user, merchant_transaction_id, merchant_session_id):
        # Bail immediately if we have no logged-in user.
        if user is None or not user.is_authenticated():
            raise APIException('Authenticated user must be provided. - %s' % user)

        self.user = user

        args = {
            'MerchantTransactionID': merchant_transaction_id,
            'MerchantSessionID': merchant_session_id,
        }

        # Combine the base parameters and the supplied arguments into a single dict that
        # we can pass as POST parameters.
        self.params.update(self.base_params)
        self.params.update(args)

    def handle_response(self):
        # Log out the req + res
        logger.info({
            'url': self.url,
            "action": self.action_name,
            "request": self.params,
            "response": self.response_wrapper.json,
        })

        # Save our session info
        GidxSession.objects.create(
            user=self.user,
            session_id=self.response_wrapper.json['MerchantSessionID'],
            service_type=self.service_type,
            request_data=strip_sensitive_fields(self.params),
            response_data=self.response_wrapper.json,
        )

        # 500+ means some kind of service-level error. make sure we get notified about these.
        if self.response_wrapper.json['ResponseCode'] >= 500:
            logger.error({
                'url': self.url,
                "action": "%s%s" % (self.action_name, '--FAIL'),
                "request": self.params,
                "response": self.response_wrapper.response.text,
            })
            # Send some useful information to Sentry.
            client.context.merge({'extra': {
                'response_json': self.response_wrapper.json,
                'response_text': self.response_wrapper.response.text,
                'params': self.params,
                'url': self.url,
            }})
            client.captureMessage(
                "GIDX request failed - %s" % self.response_wrapper.json['ResponseMessage'])
            client.context.clear()

            raise ValidationError(detail='%s' % self.response_wrapper.json['ResponseMessage'])

    # This does the actual sending.
    def _send(self):
        # Do a simple `None` check on all params
        self.validate_params()
        # Make the request!
        res = requests.get(self.url, self.params)
        # Save the response. This will do some basic response error handling.
        self.response_wrapper = self.responseClass(response=res, params=self.params, url=self.url)
        self.handle_response()

        # Return the response wrapper.
        return self.response_wrapper

    # The external method that is used to make the request.
    def send(self):
        logger.info("WEB_CACHIER_PAYMENT_DETAIL_REQUEST - MerchantTransactionID: %s" % (
            self.params['MerchantTransactionID']))
        # Call the parent's _send, it does the actual work.
        return self._send()

    def has_payments(self):
        # we have a successful response
        if self.response_wrapper.json['ResponseCode'] == 0:
            # and there are payment details.
            if len(self.response_wrapper.json['PaymentDetails']) == 0:
                error_msg = 'PaymentDetails list is empty! -- %s' % self.response_wrapper.json
                logger.error(error_msg)
                raise Exception(error_msg)

            return True

        # If ResponseCode is not 0, something went wrong.
        return False

    def get_payments_info(self):
        return self.response_wrapper.json['PaymentDetails']

    def get_successful_deposits(self):
        """
        Return ony succesfull money deposits, not bonus cash or anything like that.
        :return: List
        """
        payments = self.response_wrapper.json['PaymentDetails']
        ok_deposits = []

        # Loop through the payments and pluck out the good ones.
        for payment in payments:
            # Cast the PaymentStatusCode as a string.. it comes through that way but I don't really
            # trust it because similar fields come through the API as Ints
            if payment['PaymentAmountCode'] == 'Sale' and str(payment['PaymentStatusCode']) == '1':
                ok_deposits.append(payment)

        return ok_deposits


@app.task(bind=True)
def make_web_cashier_payment_detail_request(self, user, transaction_id, session_id):
    payment_detail_request = WebCashierPaymentDetailRequest(
        user=user,
        merchant_transaction_id=transaction_id,
        merchant_session_id=session_id,
    )

    payment_detail_response = payment_detail_request.send()
    transaction_id = payment_detail_response.json['MerchantTransactionID']
    logger.info('Payment detail received: %s' % payment_detail_response.json)

    # The response contains payments...
    if payment_detail_request.has_payments():
        payments = payment_detail_request.get_successful_deposits()

        for payment in payments:
            # was it a credit (deposit) or debit (withdraw)?
            payment_type = payment['PaymentAmountType']

            # Create a gidx cash transaction which will save the transaction to the db and
            # update the user's balance.
            trans = CashTransaction(user)

            #
            # It is a DEPOSIT
            if payment_type.lower() == 'credit'.lower():
                if payment['PaymentStatusMessage'] == 'Failed':
                    logger.warning(
                        'Deposit payment was not a success, not adding funds. %s' % payment)

                elif payment['PaymentStatusMessage'] == 'Complete':
                    # Deposit the amount into their account
                    trans.deposit_gidx(payment['PaymentAmount'], transaction_id)

                    # Create a task that will send the user an email confirming the transaction
                    try:
                        send_deposit_receipt.delay(
                            user, payment['PaymentAmount'], trans.get_balance_string_formatted(),
                            timezone.now())
                    except Exception as e:
                        logger.error(e)
                        client.captureException(e)
                else:
                    raise Exception(
                        'Unknown PaymentStatusMessage from GIDX payment detail response: %s' % (
                            payment
                        ))

            #
            # It is a PAYOUT
            elif payment_type.lower() == 'debit'.lower():
                # The withdraw failed - We can leave everything alone.
                if payment['PaymentStatusMessage'] == 'Failed':
                    logger.warning(
                        'Withdraw was not a success, refunding amount. %s' % payment)

                # Withdraw was a success! We need to withdraw + notify the user.
                elif payment['PaymentStatusMessage'] == 'Complete':
                    trans.withdraw_gidx(payment['PaymentAmount'], transaction_id)

                    # Create a task that will send the user an email confirming the transaction
                    try:
                        send_deposit_receipt.delay(
                            user, payment['PaymentAmount'], trans.get_balance_string_formatted(),
                            timezone.now())
                    except Exception as e:
                        logger.error(e)
                        client.captureException(e)
                else:
                    raise Exception(
                        'Unknown PaymentStatusMessage from GIDX payment detail response: %s' % (
                            payment
                        ))
            else:
                raise Exception(
                    'Unknown PaymentAmountType from GIDX payment detail response: %s' % (
                        payment
                    ))


class WebCashierCreatePayoutSession(GidxRequest):
    """
     This method should be called to create a new PAYOUT Cashier Web Session within the GIDX system for
     payments.

    A payout is just like a depsit except the `PayActionCode` is `PAYOUT` instead of `PAY` and
    we need to add an amount into the request.

     http://www.tsevo.com/Docs/WebCashier#MethodRef_ID_CreateSession
    """

    url = 'https://api.gidx-service.in/v3.0/api/WebCashier/CreateSession'
    service_type = 'WebCashier_CreateSession'
    responseClass = WebRegCreateSessionResponse
    action_name = "WEB_CACHIER_CREATE_SESSION_REQUEST"

    def __init__(self, user, ip_address, amount):
        # Bail immediately if we have no logged-in user.
        if user is None or not user.is_authenticated():
            raise APIException('Authenticated user must be provided. - %s' % user)

        self.user = user

        args = {
            # A unique SessionID from your system assigned to this active session.
            'MerchantSessionID': '%s%s' % (
            settings.GIDX_MERCHANT_SESSION_ID_PREFIX, get_short_uuid()),
            # IP address for the current device (The Customers' Device – NOT your servers
            # IP address) for this active session.
            'CustomerIpAddress': ip_address,
            # Your unique ID for this customer.
            'MerchantCustomerID': get_customer_id_for_user(user),
            'PayActionCode': 'PAYOUT',
            'MerchantTransactionID': get_short_uuid(),
            'MerchantOrderID': get_short_uuid(),
            # I can't for the life of me get reverse() to work here. I am sorry.
            'CallbackURL': '%s%s' % (get_webhook_base_url(), '/api/account/withdraw-webhook/'),
            'CashierPaymentAmount': {
                'PaymentAmount': amount,
                'PaymentAmountOverride': True,
                'PaymentCurrencyCode': 'USD'
            },
            'CustomerRegistration': {
                'CustomerIpAddress': ip_address,
                'MerchantCustomerID': get_customer_id_for_user(user)
            }
        }

        # Combine the base parameters and the supplied arguments into a single dict that
        # we can pass as POST parameters.
        self.params.update(self.base_params)
        self.params.update(args)

    def send(self):
        # Call the parent's _send, it does the actual work.
        return self._send()
