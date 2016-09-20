import requests
from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2
from .models import UserLog


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
    action = None
    log_data = {}
    geo_ip = GeoIP2()

    def __init__(self, action, request=None, ip=None, user=None):
        """

        :param action: on what action this check was running
        :param request: user request to detect his ip
        :param ip: ip for validation, in case of validation some ip not from
        request
        """
        self.ip = ip
        self.user = user
        if not request and not ip :
            err_msg = 'request or ip and should be provided'
            raise Exception(err_msg)

        if not self.ip:
            self.ip = get_client_ip(request)

        if not self.user and request.user.is_authenticated():
            self.user = request.user

        if self.user:
            self.log_data = {
                'user': self.user,
                'ip': self.ip,
                'action': self.action
            }

    def create_log(self, type, metadata):
        if self.log_data:
            log_data = self.log_data.copy()
            log_data['type'] = type
            log_data['metadata'] = metadata
            return UserLog.objects.create(**log_data)
        return False

    def check_ip(self, flag="m", subdomain=settings.GETIPNET_SUBDOMAIN):
        url = 'http://%s.getipintel.net/check.php?ip=%s&contact=%s&flags=%s'
        response = requests.get(
            url % (subdomain, self.ip, settings.GETIPNET_CONTACT, flag)
        )
        if response.status_code == 200:
            value = float(response.content)
            result = True if value < settings.GETIPNET_NORMAL else False
            msg = '' if result else 'Your ip to risky, or VPN used'
            self.create_log(UserLog.CHECK_IP, 'Access Grunted: %s, Risky value: %s' % (result, value))
            return result, msg
        # in case of out of limit
        elif response.status_code == 429:
            return self.check_ip(subdomain=settings.GETIPNET_DEFAULT_SUBDOMAIN)
        #service not working
        else:
            return True, ''

    @property
    def check_location_country(self):
        country = self.geo_ip.country(self.ip)
        result = True if country.get('country_code') not in settings.BLOCKED_COUNTRIES_CODES else False
        msg = '' if result else 'Your country in blocked list'
        self.create_log(UserLog.CHECK_COUNTRY, 'Access Grunted: %s, Country: %s' % (result, country.get('country_code')))
        return result, msg

    @property
    def check_location_city(self):
        city = self.geo_ip.city(self.ip)
        result = True if city.get('city') not in settings.BLOCKED_CITIES else False
        msg = '' if result else 'Your city in blocked list'
        self.create_log(UserLog.CHECK_CITY, 'Access Grunted: %s, City: %s' % (result, city.get('city')))
        return result, msg

    @property
    def check_access(self):
        # do it one by one because it doesn't make a sense to check ip if country or city already blocked
        access, msg = self.check_location_country
        if not access:
            return access, msg
        access, msg = self.check_location_city
        if not access:
            return access, msg
        return self.check_ip()
