#
# classes.py

import time
import requests
import json
from django.conf import settings
from datetime import datetime, date, timedelta

#
# ex: https://api.swishanalytics.com/nfl/players/injuries?date=2016-08-15,2016-08-16&team=ne&apikey=e7ec4ca5fca54a01ac0038205b8235e9

class SwishAnalytics(object):

    class SwishApiException(Exception): pass

    api_base_url = 'https://api.swishanalytics.com'
    api_injuries = '/players/injuries'

    api_key = settings.SWISH_API_KEY

    sport = None

    def __init__(self):
        # create the Session object for performing the api calls
        self.session = requests.Session()
        # always hold onto the last http response
        self.r = None

    def call_api(self, url):
        """ retrieve the api as json """
        self.r = self.session.get(url)
        status_code = self.r.status_code
        if status_code >= 300:
            err_msg = 'http [%s]' % str(status_code)
            raise self.SwishApiException(err_msg)

        # otherwise convert it to JSON and return the the data
        return json.loads(self.r.text)

    def get_formatted_date(self):
        """ returns a formatted date string like: '2016-08-16' """
        now = datetime.now()
        return str(now.date())

    def get_injuries(self):
        formatted_date = self.get_formatted_date()
        url = '%s/%s%s?date=%s&apikey=%s' % (self.api_base_url, self.sport,
                                            self.api_injuries, formatted_date, self.api_key)
        return self.call_api(url)

class SwishNFL(SwishAnalytics):
    sport = 'nfl'


