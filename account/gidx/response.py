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
        reason_codes = self.json['ReasonCodes']
        # If we have reason codes...
        if len(reason_codes):
            # And one of othem is an id verified flag, we are verified!
            if 'ID-VERIFIED' in reason_codes:
                return True

        # If we have no codes or are missing  the verified one, we are not verified.
        return False

    def get_country(self):
        return get_country_from_response(self.json)

    def get_region(self):
        return get_region_from_response(self.json)

    def location_is_blocked(self):
        # TODO: `LL-BLOCK` for blocked locations
        pass

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
                'form_embed': urllib.parse.unquote_plus(self.json['SessionURL'])
            }
        return ''

    def is_verified(self):
        """
        The WebRegCreateSession endpoint cannot tell us if the user is verified or not. it will
        simply give us an embeddable JS script, so this is always False.
        :return: Bool
        """
        return False


class WebhookResponse(CustomerRegistrationResponse):

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
        status_code = self.json['StatusCode']

        # 0 is the 'success' code.
        return status_code == 0

