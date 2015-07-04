#
# util/timesince.py

from datetime import datetime, timedelta
from pytz import timezone as pytz_timezone
from util.utctime import UtcTime

class TimeSince(UtcTime):

    @staticmethod
    def get_str( dt, tzinfo=None, suffix=' ago...' ):
        """
        Return the minutes since the datetime 'dt' passed in.

        If its been more than  60 minutes, return a very succinct string formatted datetime.

        :param dt:
        :return:
        """
        if tzinfo is None:
            tzinfo = UtcTime.TZ_UTC

        tmp = datetime.utcnow()
        now = datetime( tmp.year, tmp.month, tmp.day,
                        tmp.hour, tmp.minute, tmp.second, tzinfo=tzinfo )
        dlta = now - dt
        seconds = dlta / timedelta(seconds = 1)
        minutes = seconds / 60
        if minutes < 1:
            return '%sec%s' % (str(int(seconds)), suffix)
        elif minutes < 60:
            return '%sm%s' % (str(int(minutes)), suffix)
        else:
            return dt.strftime('%d %b %Y')

timesince = TimeSince.get_str