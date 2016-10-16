import requests
from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2
from django.contrib.auth.forms import PasswordResetForm
from geoip2.errors import AddressNotFoundError
from raven.contrib.django.raven_compat.models import client
import logging
from account import const as _account_const

logger = logging.getLogger('django')


def create_user_log(request=None, type=None, action=None, metadata={}):
    from .models import UserLog
    """
    Create a UserLog entry
    """
    # Make sure whatever we are doing doesn't die because of a UserLog failure.
    try:
        if not request:
            raise Exception('request is required')
        log_data = {}
        log_data['type'] = type
        log_data['action'] = action
        log_data['metadata'] = metadata
        log_data['ip'] = get_client_ip(request)
        log_data['user'] = request.user
        return UserLog.objects.create(**log_data)

    # If the log creation failed, capture the exception and log it to both
    # Sentry and the django logger.
    except Exception as e:
            logger.error("create_user_log() %s" % str(e))
            client.captureException()


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class CheckUserAccess(object):
    """
    Check user access for site, by checking user IP on risque and
    check that his location not in blocked one's
    """
    ip = None
    user = None
    geo_ip = GeoIP2()
    request = None

    def __init__(self, request=None):
        """
        :param request: user request to detect his ip
        :param ip: ip for validation, in case of validation some ip not from
        request
        """
        if not request:
            err_msg = 'request should be provided'
            raise Exception(err_msg)

        self.ip = get_client_ip(request)
        self.user = request.user
        self.request = request

    def create_log(self, action, metadata):
        # Simple method to pass LOCATION_VERIFY actions onto the user logger.
        create_user_log(self.request, _account_const.LOCATION_VERIFY, action, metadata)

    def is_on_local_network(self):
        # Check if the user is on the local network. If they are, log it.
        if (self.ip[:8] == '192.168.'):
            self.create_log(
                _account_const.IP_CHECK_LOCAL,
                {'result': 'Access Granted: User is on local network.'}
            )
            return True
        return False

    def check_ip(self, flag="m", subdomain=settings.GETIPNET_SUBDOMAIN):
        url = 'http://%s.getipintel.net/check.php?ip=%s&contact=%s&flags=%s'
        response = requests.get(
            url % (subdomain, self.ip, settings.GETIPNET_CONTACT, flag)
        )
        if response.status_code == 200:
            value = float(response.content)
            result = True if value < settings.GETIPNET_NORMAL else False
            msg = '' if result else 'Your ip is too risky, or VPN used'
            self.create_log(
                _account_const.IP_CHECK_STATUS,
                {
                    'result': 'Access Granted: %s, Risky value: %s' %
                              (result, value)
                }
            )
            return result, msg
        # in case of out of limit
        elif response.status_code == 429:
            print(self.check_ip(subdomain=settings.GETIPNET_DEFAULT_SUBDOMAIN))
            return self.check_ip(subdomain=settings.GETIPNET_DEFAULT_SUBDOMAIN)
        # service not working
        else:
            logger.error("Unexpected getipintel.net response: %s" % str(response))
            client.captureMessage("Unexpected getipintel.net response: %s" % str(response))
            return True, ''

    @property
    def check_location_country(self):
        try:
            country = self.geo_ip.country(self.ip)
            result = True if country.get(
                'country_code') not in settings.BLOCKED_COUNTRIES_CODES else False
            msg = '' if result else 'Country in blocked list'
            if not result:
                self.create_log(
                    _account_const.IP_CHECK_FAILED_COUNTRY,
                    {'result': 'Access Denied: Country %s in blocked list' %
                        country.get('country_code')}
                )
            return result, msg
        except AddressNotFoundError:
            self.create_log(
                _account_const.IP_CHECK_FAILED_COUNTRY,
                {'result': 'Access Denied: IP not found in country db'}
            )
            return True, ''

    @property
    def check_location_state(self):
        try:
            state = self.geo_ip.city(self.ip)
            result = True if state.get('region') not in settings.BLOCKED_STATES else False
            msg = '' if result else 'Your state in blocked list'
            if not result:
                self.create_log(
                    _account_const.IP_CHECK_FAILED_STATE,
                    {'result': 'Access Denied: State %s in blocked list' % state.get('region')}
                )

            return result, msg
        except AddressNotFoundError:
            self.create_log(
                _account_const.IP_CHECK_FAILED_STATE,
                {'result': 'Access Denied: IP not found in state db'}
            )
            return True, ''

    @property
    def check_access(self):
        # If the user is on the local network, let them through.
        if self.is_on_local_network():
            return True, ''

        # do it one by one because it doesn't make a sense to check ip if country
        # or city already blocked
        access, msg = self.check_location_country
        if not access:
            return access, msg

        access, msg = self.check_location_state
        if not access:
            return access, msg

        return self.check_ip()


def reset_user_password_email(user, request):
    if user.email:
        form = PasswordResetForm({'email': user.email})
        form.is_valid()
        form.save(from_email=settings.DEFAULT_FROM_EMAIL, request=request)
