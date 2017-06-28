from logging import getLogger
from pprint import pprint

import requests
from django.conf import settings

from .exceptions import (ResponseMessageException, RequestError)

logger = getLogger('account.gidx.request')


class GidxRequest(object):
    url = None
    response = None
    # Extra params that sub-classes can fill up.
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

    def _get(self):
        self.validate_params()
        res = requests.post(self.url, self.params)
        self.response = res

        if res.status_code != 200:
            raise RequestError(self.response.text)

        pprint(res.json())
        self.res_payload = res.json()

        # a ResponseCode of 0 indicates no errors.
        if not self.res_payload['ResponseCode'] == 0:
            logger.warning(self.res_payload['ResponseMessage'])
            raise ResponseMessageException(
                '%s - %s' %
                (self.res_payload['ResponseCode'], self.res_payload['ResponseMessage'])
            )

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

    def get(self):
        # Call the parent's _send, it does the actual work.
        self._get()

        # Now do any response handling.
        if len(self.res_payload['ProfileMatches']) == 0:
            logger.warning('No profile match found!')
