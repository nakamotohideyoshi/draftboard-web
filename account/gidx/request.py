import copy
import uuid
from logging import getLogger

import requests
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from raven.contrib.django.raven_compat.models import client
from rest_framework.exceptions import (APIException, ValidationError)

from .models import GidxSession
from .response import (CustomerRegistrationResponse, WebRegCreateSessionResponse)
from mysite.celery_app import app


logger = getLogger('account.gidx.request')

# We don't want to log or save these fields in our request logs.
REQUEST_FIELD_BLACKLIST = ['FirstName', 'LastName', 'DateOfBirth']


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
        res = requests.post(self.url, self.params)
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
            'MerchantSessionID': '%s%s' % (settings.GIDX_MERCHANT_SESSION_ID_PREFIX, uuid.uuid4()),
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
            'MerchantSessionID': '%s%s' % (settings.GIDX_MERCHANT_SESSION_ID_PREFIX, uuid.uuid4()),
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
            'MerchantSessionID': '%s%s' % (settings.GIDX_MERCHANT_SESSION_ID_PREFIX, uuid.uuid4()),
            # IP address for the current device (The Customers' Device – NOT your servers
            # IP address) for this active session.
            'CustomerIpAddress': ip_address,
            # Your unique ID for this customer.
            'MerchantCustomerID': get_customer_id_for_user(user),
            'PayActionCode': 'PAY',
            'MerchantTransactionID': str(uuid.uuid4()),
            'MerchantOrderID': str(uuid.uuid4()),
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

    def __init__(self, user, merchant_transaction_id):
        # Bail immediately if we have no logged-in user.
        if user is None or not user.is_authenticated():
            raise APIException('Authenticated user must be provided. - %s' % user)

        self.user = user

        args = {
            'MerchantTransactionID': merchant_transaction_id,
            'MerchantSessionID': '%s%s' % (settings.GIDX_MERCHANT_SESSION_ID_PREFIX, uuid.uuid4()),

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


@app.task(bind=True)
def make_web_cashier_payment_detail_request(self, user, merchant_transaction_id):
    req = WebCashierPaymentDetailRequest(user=user, merchant_transaction_id=merchant_transaction_id)
    return req.send()
