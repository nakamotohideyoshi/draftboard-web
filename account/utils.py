import requests
from dateutil.relativedelta import relativedelta
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2
from django.contrib.auth.forms import PasswordResetForm
from geoip2.errors import AddressNotFoundError
from raven.contrib.django.raven_compat.models import client
from mysite.legal import (BLOCKED_STATES, LEGAL_COUNTRIES, STATE_AGE_LIMITS)
from mysite.legal import BLOCKED_STATES_NAMES
from account import const as _account_const
import logging
from ipware.ip import get_real_ip, get_ip

logger = logging.getLogger('account.utils')


def encode_uid(pk):
    try:
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        return urlsafe_base64_encode(force_bytes(pk)).decode()
    except ImportError:
        from django.utils.http import int_to_base36
        return int_to_base36(pk)


def create_user_log(request=None, type=None, action=None, metadata={}, user=None):
    from .models import UserLog
    """
    Create a UserLog entry
    """
    if user is None:
        logger.info('Not creating UserLog, no user was supplied.')
        return

    # Make sure whatever we are doing doesn't die because of a UserLog failure.
    try:
        log_data = {}
        if request:
            log_data['ip'] = get_client_ip(request)
        log_data['type'] = type
        log_data['action'] = action
        log_data['metadata'] = metadata
        log_data['user'] = user or request.user
        # Don't create a user log for anonymous users.
        if log_data['user'].is_authenticated():
            UserLog.objects.create(**log_data)

    # If the log creation failed, capture the exception and log it to both
    # Sentry and the django logger.
    except Exception as e:
        logger.error("create_user_log() %s" % str(e))
        client.captureException()


def get_client_ip(request):
    ip = get_real_ip(request)
    if not ip:
        ip = get_ip(request)
    return ip


class CheckUserAccess(object):
    """
    Check user access for site, by checking user IP on risque and
    check that his location not in blocked one's
    """
    ip = None
    user = None
    geo_ip = GeoIP2()
    geo_ip_response = None
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

        # Make a query on the geoIP database.
        if self.ip:
            try:
                self.geo_ip_response = self.geo_ip.city(self.ip)
            except AddressNotFoundError:
                self.geo_ip_response = None
                self.create_log(
                    _account_const.IP_CHECK_UNKNOWN,
                    {'result': 'Access Granted: IP not found in city db'}
                )

    def create_log(self, action, metadata):
        # Simple method to pass LOCATION_VERIFY actions onto the user logger.
        create_user_log(request=self.request, type=_account_const.LOCATION_VERIFY, action=action,
                        metadata=metadata, user=self.user)

    def is_on_local_network(self):
        try:
            no_dots = self.ip.replace('.', '')
            ip_first_five_int = int(no_dots[0:5])
        except:
            logger.warning('Invalid IP address error - %s' % self.ip)
            client.captureMessage("Invalid IP address error - %s" % self.ip)
            return False

        # Check if the user is on the local network. If they are, log it.
        # Check for 192.168 addresses.
        if (self.ip[:8] == '192.168.'):
            self.create_log(
                _account_const.IP_CHECK_LOCAL,
                {'result': 'Access Granted: User is on local network.'}
            )
            logger.info('User is on local IP address - %s' % self.ip)
            return True
        # Check for 172.16.0.0 -- 172.31.255.255
        elif ip_first_five_int >= 17216 and ip_first_five_int <= 17231:
            self.create_log(
                _account_const.IP_CHECK_LOCAL,
                {'result': 'Access Granted: User is on local network.'}
            )
            logger.info('User is on local IP address - %s' % self.ip)
            return True

        return False

    def check_for_vpn(self, flag="m", subdomain=settings.GETIPNET_SUBDOMAIN):
        url = 'https://%s.getipintel.net/check.php?ip=%s&contact=%s&flags=%s'
        response = requests.get(
            url % (subdomain, self.ip, settings.GETIPNET_CONTACT, flag)
        )
        if response.status_code == 200:
            value = float(response.content)
            result = True if value < settings.GETIPNET_NORMAL else False
            msg = '' if result else MODAL_MESSAGES['VPN']['message']

            # Log all failed attempts.
            if result is False:
                logger.info('check_for_vpn Failed. risk value: %s' % value)

                self.create_log(
                    _account_const.IP_CHECK_STATUS,
                    {'result': 'Access Denied, Risk value: %s' % value}
                )
            else:
                logger.info('check_for_vpn Passed. risk value: %s' % value)

            return result, msg
        # in case of out of limit
        elif response.status_code == 429:
            logger.error("getipintel.net 429 response: %s" % response.reason)
            client.context.merge({'extra': {
                'reason': response.reason,
                'status_code': response.status_code,
                'ip': self.ip,
                'user': self.user.username,
            }})
            client.captureMessage("Unexpected getipintel.net response: %s" % str(response))
            client.context.clear()
            return True, response.reason
        # service not working
        else:
            logger.error("Unexpected getipintel.net response: %s" % response.reason)
            client.context.merge({'extra': {
                'reason': response.reason,
                'status_code': response.status_code,
                'ip': self.ip,
                'user': self.user.username,
            }})
            client.captureMessage("Unexpected getipintel.net response: %s" % str(response))
            client.context.clear()
            return True, ''

    def check_location_country(self, return_country=False):
        try:
            country = self.geo_ip_response.get('country_code')
            result = True if country in LEGAL_COUNTRIES else False
            msg = '' if result else MODAL_MESSAGES['COUNTRY']['message']

            if not result:
                self.create_log(
                    _account_const.IP_CHECK_FAILED_COUNTRY,
                    {'result': 'Access Denied: Country %s in blocked list' % country}
                )
            if return_country:
                return result, msg, country
            return result, msg
        except AddressNotFoundError:
            self.create_log(
                _account_const.IP_CHECK_UNKNOWN,
                {'result': 'Access Granted: IP not found in country db'}
            )
            return True, 'Access Granted: IP not found in country db'

    def check_location_state(self, return_state=False):
        try:
            state = self.geo_ip_response.get('region')
            result = True if state not in BLOCKED_STATES else False
            msg = '' if result else MODAL_MESSAGES['STATE']['message'].format(
                        barred_state=BLOCKED_STATES_NAMES[state])
            if not result:
                self.create_log(
                    _account_const.IP_CHECK_FAILED_STATE,
                    {'result': 'Access Denied: State %s in blocked list' % state}
                )
            if return_state:
                return result, msg, state
            return result, msg
        except AddressNotFoundError:
            self.create_log(
                _account_const.IP_CHECK_UNKNOWN,
                {'result': 'Access Granted: IP not found in state db'}
            )
            return True, ''

    def check_location_age(self, state=None):
        # Check if they have a verified identity and that they are old enough to play in the state
        # their IP address tells us they are in.
        #
        # If they don't have an identity, we don't care because that permission will be set on the
        # view level.

        # If the user has permission to bypass the age check, let them through.
        if self.user.has_perm('account.can_bypass_age_check'):
            logger.info('User: %s has bypassed the age check via permissions.' % self.user.username)
            return True, ''
        try:
            identity = self.user.identity
            birthdate = identity.dob
            minimum_age = STATE_AGE_LIMITS.get(state)
            # Add the legal age for the user's state to thier birthday. This tells us the date
            # that they are allowed to begin uing the site.
            # then make sure that date is in the past
            relative = relativedelta(years=minimum_age)
            if birthdate + relative >= date.today():
                # The date this user turns legal is in the future.
                return False, 'Minimum age for this location is not met.'

            return True, 'Minimum age for this location is met.'

        # They don't have a verified identity so we don't care right now.
        except (ObjectDoesNotExist, AttributeError):
            return True, 'User has no identity, no age to check.'

        except AddressNotFoundError:
            self.create_log(
                _account_const.IP_CHECK_UNKNOWN,
                {'result': 'Access Granted: IP not found in country db'}
            )
            return True, ''

    @property
    def check_access(self):
        # If the user is on the local network, let them through.
        # if self.is_on_local_network():
        #     logger.warn('User is on the local network, skipping IP checks. user: %s' % self.user)
        #     return True, ''

        if not self.geo_ip_response:
            logger.warning('IP address not found in database: %s user: %s' % (self.ip, self.user))
            return True, 'IP not found in database'

        # do it one by one because it doesn't make a sense to check ip if country
        # or city already blocked
        access, msg = self.check_location_country()
        logger.info('%s - %s - user: %s' % ('check_location_country', access, self.user))
        if not access:
            return access, msg

        access, msg = self.check_location_state()
        logger.info('%s - %s - user: %s' % ('check_location_state', access, self.user))
        if not access:
            return access, msg

        access, msg = self.check_location_age(state='CO')
        logger.info('%s - %s - user: %s' % ('check_location_age', access, self.user))
        if not access:
            return access, msg

        return self.check_for_vpn()


def reset_user_password_email(user, request):
    if user.email:
        form = PasswordResetForm({'email': user.email})
        form.is_valid()
        form.save(from_email=settings.DEFAULT_FROM_EMAIL, request=request)


# These messages get thrown back as API responses if a user fails the location/VPN check.
MODAL_MESSAGES = {
    "COUNTRY": {
        "title": "LOCATION UNAVAILABLE",
        "message": "Looks like you're outside of the US or Canada.  Draftboard is available "
                   "only to residents of the US or Canada.  You can still sign up for an "
                   "account and create a lineup, but you will be unable to deposit or enter "
                   "contests while in not in the US or Canada. "
                   "Please contact support@draftboard.com if you have further questions.",
    },
    "STATE": {
        "title": "LOCATION UNAVAILABLE",
        "message": "Looks like you're in {barred_state}, a state we do not currently operate in. "
                   "You can still sign up for an account and create a lineup, but you will be "
                   "unable to deposit or enter contests while in {barred_state}. "
                   "Please contact support@draftboard.com if you have further questions.",

    },
    "VPN": {
        "title": "LOCATION UNAVAILABLE",
        "message": "Looks like you're using a VPN or proxy, "
                   "You can still sign up for an account and create a lineup, but you will be "
                   "unable to deposit or enter contests while using this connection. "
                   "Please contact support@draftboard.com if you have further questions.",
    }
}
