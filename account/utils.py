import requests
from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2


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
    geo_ip = GeoIP2()

    def __init__(self, request=None, ip=None):
        """

        :param request: user request to detect his ip
        :param ip: ip for validation, in case of validation some ip not from
        request
        """
        if not request and not ip:
            err_msg = 'request or ip should be provided'
            raise Exception(err_msg)
        self.ip = ip
        if not self.ip:
            self.ip = get_client_ip(request)

    def check_ip(self, flag="m", subdomain=settings.GETIPNET_SUBDOMAIN):
        url = 'http://%s.getipintel.net/check.php?ip=%s&contact=%s&flags=%s'
        response = requests.get(
            url % (subdomain, self.ip, settings.GETIPNET_CONTACT, flag)
        )
        if response.status_code == 200:
            value = float(response.content)
            return True if value < settings.GETIPNET_NORMAL else False
        # in case of out of limit
        elif response.status_code == 429:
            return self.check_ip(subdomain=settings.GETIPNET_DEFAULT_SUBDOMAIN)
        #service not working
        else:
            return True

    @property
    def check_location_country(self):
        country = self.geo_ip.country(self.ip)
        return True if country.get('country_code') not in \
                       settings.BLOCKED_COUNTRIES_CODES else False

    @property
    def check_location_city(self):
        country = self.geo_ip.city(self.ip)
        return True if country.get('city') not in \
                       settings.BLOCKED_CITIES else False

    @property
    def check_access(self):
        return self.check_ip() and self.check_location_city and \
               self.check_location_country

