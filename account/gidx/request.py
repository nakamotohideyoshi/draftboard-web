from logging import getLogger
from raven.contrib.django.raven_compat.models import client

import requests
from django.conf import settings

from rest_framework.exceptions import (APIException, ValidationError)

logger = getLogger('account.gidx.request')

EXISTING_IDENTITY_MESSAGE = "We are unable to verify your identity. Please contact " \
                            "support@draftboard.com for more info."


class GidxRequest(object):
    url = None
    response = None
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

    def _send(self):
        # Do a simple `None` check on all params
        self.validate_params()
        # Make the request!
        res = requests.post(self.url, self.params)
        # Save the response
        self.response = res

        # If we get a bad http status, exit outta here.
        if self.response.status_code != 200:
            logger.error('%s - %s' % (self.response, self.response.text))
            # Send some useful information to Sentry.
            client.context.merge({'extra': {
                'response': self.response,
                'response_text': self.response.text,
                'params': self.params,
                'url': self.url,
            }})
            client.captureMessage("GIDX request failed - %s" % self.response.status_code)
            client.context.clear()
            raise APIException(self.response.text)

        # Parse the payload
        self.res_payload = res.json()
        # Log out the req + res
        logger.info({
            "action": "ID_VERIFICATON_REQUEST",
            "request": self.params,
            "response": self.res_payload,
        })
        # a ResponseCode of 0 indicates no errors. If we had errors, raise an exception that can
        # be caught on the view layer.
        if not self.res_payload['ResponseCode'] == 0:
            logger.warning(self.res_payload)
            raise ValidationError('%s' % self.res_payload['ResponseMessage'])

    def validate_params(self):
        """
        Run through each param and ensure it is not None.
        :return:
        """
        for param, value in self.params.items():
            if value is None:
                raise Exception('%s must be provided.' % param)


class CustomerRegistrationRequest(GidxRequest):
    """
     This method should be called to register the customer within the GIDX system and find
     verify a match to their identity.
    """
    url = 'https://api.gidx-service.in/v3.0/api/CustomerIdentity/CustomerRegistration'

    def __init__(self, user, first_name, last_name, date_of_birth, ip_address):
        # Bail immediately if we have no logged-in user.
        if user is None or not user.is_authenticated():
            raise Exception('Authenticated user must be provided. - %s' % user)

        args = {
            # A unique SessionID from your system assigned to this active session.
            'MerchantSessionID': settings.GIDX_MERCHANT_SESSION_ID_PREFIX + 'TODO: this',
            # IP address for the current device (The Customers' Device – NOT your servers
            # IP address) for this active session.
            'DeviceIpAddress': ip_address,
            # Your unique ID for this customer.
            'MerchantCustomerID': '%s--%s' % (user.id, user.username),
            'FirstName': first_name,
            'LastName': last_name,
            'EmailAddress': user.email,
            # 04/03/1984 (In MM/DD/YYYY Format)
            'DateOfBirth': date_of_birth,
        }

        # Combine the base parameters and the supplied arguments into a single dict that
        # we can pass as POST parameters.
        self.params = {**self.base_params, **args}

    def send(self):
        # Call the parent's _send, it does the actual work.
        self._send()

        # Now do any response handling.
        if len(self.res_payload['ProfileMatches']) == 0:
            logger.warning('No profile match found!')

    def get_response_message(self):
        """
        This is used to filter out the stupid 'No error.' response message.
        :return:
        """
        if self.res_payload:
            # If the identity is already claimed, return that message.
            if self.identity_is_claimed():
                return EXISTING_IDENTITY_MESSAGE

            # There is no error, so return nothing, not their dumb default.
            if self.res_payload['ResponseMessage'] == 'No error.':
                return ''

            return self.res_payload['ResponseMessage']
        return ''

    def identity_is_claimed(self):
        """
        Check if the response reasonCod contains `ID-EX` which means that
        this identity has already been verified by us before.
        :return:
        """
        if self.res_payload is None:
            logger.warning('You have not made a request yet.')
            return False

        reason_codes = self.res_payload['ReasonCodes']
        if 'ID-EX' in reason_codes:
            logger.warning('This identity has been previously verified.')
            return True

        return False

    def is_verified(self):
        """
        After we have made our request, use this to check the if the response tells us the
        identity we sent was a verified match.
        :return: bool
        """

        # If we haven't retrieved the payload yet, it obviously isn't an identity match.
        if self.res_payload is None:
            logger.warning('You have not made a request yet.')
            return False

        reason_codes = self.res_payload['ReasonCodes']
        # If we have reason codes...
        if len(reason_codes):
            # And one of othem is an id verified flag, we are verified!
            if 'ID-VERIFIED' in reason_codes:
                return True

        # If we have no codes or are missing  the verified one, we are not verified.
        return False

    def get_country(self):
        if self.res_payload is None:
            logger.warning('You have not made a request yet.')
            return False

        for code in self.res_payload['ReasonCodes']:
            if 'LL-GEO-' in code:
                return code.split('-')[-2]

    def get_region(self):
        def get_country(self):
            if self.res_payload is None:
                logger.warning('You have not made a request yet.')
                return False

            for code in self.res_payload['ReasonCodes']:
                if 'LL-GEO-' in code:
                    return code.split('-')[-1]

    def is_identity_previously_claimed(self):
        if self.res_payload is None:
            logger.warning('You have not made a request yet.')
            return False

        return 'ID-EX' in self.res_payload['ReasonCodes']
