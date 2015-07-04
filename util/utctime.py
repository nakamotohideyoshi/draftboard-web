#
# util/utctime.py

from pytz import timezone as pytz_timezone

class UtcTime(object):

    TZ_UTC = pytz_timezone('UTC')