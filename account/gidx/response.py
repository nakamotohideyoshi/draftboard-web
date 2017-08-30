from logging import getLogger
import urllib.parse
from raven.contrib.django.raven_compat.models import client
from rest_framework.exceptions import (APIException)

logger = getLogger('account.gidx.request')


def get_country_from_response(response):
    for code in response['ReasonCodes']:
        if 'LL-GEO-' in code:
            return code.split('-')[-2]


def get_region_from_response(response):
    for code in response['ReasonCodes']:
        if 'LL-GEO-' in code:
            return code.split('-')[-1]


def is_underage(reason_codes=[]):
    # exampe of underage code: 'ID-UA-19'
    for code in reason_codes:
        if 'UA' in code:
            return code.split('-')[1] == 'UA'

    return False


def is_location_blocked(reason_codes=[]):
    # `LL-BLOCK` means the user's location is on our block list.
    return 'LL-BLOCK' in reason_codes


class CustomerRegistrationResponse(object):
    response = None
    json = None

    def __init__(self, response, params=None, url=None):
        self.response = response
        # If the response was a success, parse the json.
        if self.is_ok():
            self.json = response.json()

        # If we get a bad http status, exit outta here and throw some errors.
        else:
            logger.error({
                "action": "ID_VERIFICATON_REQUEST--FAIL",
                "request": params,
                "response": '%s - %s' % (self.response, self.response.text),
            })
            # Send some useful information to Sentry.
            client.context.merge({'extra': {
                'response': self.response,
                'response_text': self.response.text,
                'params': params,
                'url': url,
            }})
            client.captureMessage(
                "GIDX request failed - %s" % self.response.status_code)
            client.context.clear()
            raise APIException(detail=self.response.text)

    def is_ok(self):
        # Do a basic 200 status_code check.
        return self.response.status_code == 200

    def get_response_message(self):
        """
        This is used to filter out the stupid 'No error.' response message.
        :return:
        """
        if self.json:
            # There is no error, so return nothing, not their dumb default.
            if self.json['ResponseMessage'] == 'No error.':
                return ''

            return self.json['ResponseMessage']
        return ''

    def is_verified(self):
        """
        After we have made our request, use this to check the if the response tells us the
        identity we sent was a verified match.
        :return: bool
        """
        reason_codes = self.get_reason_codes()
        # If we have reason codes...
        if len(reason_codes):
            # Check if their location is blocked.
            if is_location_blocked(reason_codes):
                return False

            # If we had an underage code, don't let them verify.
            if is_underage(reason_codes):
                return False

            # And one of othem is an id verified flag, we are verified!
            if 'ID-VERIFIED' in reason_codes:
                return True

        # If we have no codes or are missing the verified one, we are not verified.
        return False

    def get_country(self):
        return get_country_from_response(self.json)

    def get_region(self):
        return get_region_from_response(self.json)

    def is_identity_previously_claimed(self):
        """
        Check if the response reasonCod contains `ID-EX` which means that
        this identity has already been verified by us before.
        :return:
        """
        return 'ID-EX' in self.json['ReasonCodes']

    def get_reason_codes(self):
        return self.json['ReasonCodes']


class WebRegCreateSessionResponse(CustomerRegistrationResponse):

    def get_response_message(self):
        if self.json:
            return {
                # For some ungodly reason they plus-encode the JS snippet :(
                'form_embed': urllib.parse.unquote_plus(self.json['SessionURL']),
                'merchant_session_id': self.json['MerchantSessionID'],
            }
        return ''


class IdentityStatusWebhookResponse(CustomerRegistrationResponse):

    def __init__(self, response_dict, params=None, url=None):
        self.response = response_dict
        # Since this isnt' a `requests` library response, it's just raw json data.
        self.json = response_dict

    def is_verified(self):
        """
        After we recieve our webhook data, use this to check the if the payload tells us the
        identity we sent was a verified match.
        :return: bool
        """

        # First do the normal checking of reason codes.
        if not super().is_verified():
            return False

        # If we pass a reason code check, look at the statusCode.
        # 0 is the 'success' code.
        return self.json['StatusCode'] == 0


class DepositStatusWebhookResponse(object):
    """
    A wrapper for the data that GIDX sends to us on the api/account/deposit-webhook/. It should
    contain an small amount of information about whether or not the deposit was a success.
    """
    def __init__(self, response_dict, params=None, url=None):
        self.response = response_dict
        # Since this isnt' a `requests` library response, it's just raw json data.
        self.json = response_dict

    def is_successful(self):
        """
        Was the payment a success?

        status codes:

        -1 Payment not found.
        No payment / transaction was found for the corresponding identifier supplied.

        0 Pending
        The payment/transaction is pending approval or validation.

        1 Complete
        The payment/transaction has been Completed.

        2 Ineligible
        The payment/transaction was ineligible for processing.

        3 Failed
        The payment/transaction was rejected by the processing provider.

        4 Processing
        The payment/transaction has been sent to the processor and is awaiting a status update.

        5 Reversed
        The payment/transaction has been reversed / cancelled by an authorized party.

        :return: bool
        """

        return self.json['TransactionStatusCode'] == 1
