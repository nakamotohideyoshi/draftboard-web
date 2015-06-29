#
# dataden/util/timestamp.py

from datetime import datetime, time, date, timedelta
from pytz import timezone as pytz_timezone

class Parse(object):

    @staticmethod
    def from_string(s):
        """
        parse a timestamp from sportsradar feeds of the form: 2015-04-18T16:30:00+00:00

        :return:
        """

        DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
        dt_str = s.split('+')[0]
        dt = datetime.strptime( dt_str, DATETIME_FORMAT )
        int_val = int(dt.strftime('%s'))
        #return datetime.datetime.fromtimestamp( int_val, tz=timezone.utc )
        return datetime.fromtimestamp( int_val, tz=pytz_timezone('UTC'))

class DfsDateTimeUtil(object):
    """
    This class provides methods for translating UTC datetimes
    to EST, and vice versa.

    This is useful, because the "day's games" for many sports appear
    to span multiple days when looked at in UTC.

    From the perspective of Daily Fantasy, this class
    considers a "day" to be the 24 hours in the EST timezone.
    (In our implementation we use pytz.timezone('US/Eastern'))

    All methods of this class expect UTC timezone aware datetime objects,
    and will raise NotUtcTimezoneException in all other cases.

    """

    class NotUtcTimezoneException(Exception): pass

    UTC_TIMEZONE = pytz_timezone('UTC')
    DFS_TIMEZONE = pytz_timezone('US/Eastern')

    # datetime.weekday() constants
    MON = 0
    TUE = 1
    WED = 2
    THR = 3
    FRI = 4
    SAT = 5
    SUN = 6

    def __init__(self, dfs_timezone=DFS_TIMEZONE):
        """
        All major U.S. sports post their game start times in EST.

        :param dfs_timezone: the pytz.timezone object of the Daily Fantasy site (default: EST)
        """
        self.dfs_timezone = dfs_timezone

    def __valid_utc(self, dt):
        if dt.tzinfo is not self.UTC_TIMEZONE:
            raise self.NotUtcTimezoneException('the supplied datetime object must be in utc')

    # def get_(self, dt):
    #     """
    #     For the given datetime 'dt', return a new datetime object
    #     which represents the current day at 12 AM
    #
    #     :param dt: datetime object - tzinfo set to UTC
    #     :return:
    #     """
    #     time_am = datetime.time(0, 0) # 12 AM
    #     return datetime.combine( dt.date(), time_am )

    # @staticmethod
    # def start_of_tomorrow(self, dt):
    #     """
    #     For the given datetime 'dt', return a new datetime object
    #     which represents the following day at 12 AM. (ie: the instant
    #     of the next day).
    #
    #     :param dt: a datetime object
    #     :return: datetime representing 12AM on the following day.
    #     """
    #     one_day = datetime.timedelta(days=1)
    #     return DateTimeUtil.start_of_day( dt + one_day )

    # @staticmethod
    # def start_of_next_tuesday( dt ):
    #     """
    #     For the given datetime 'dt', return a new datetime object
    #     which represents the closest TUESDAY in the future at
    #     12 AM (the first instant of tuesday in the morning.)
    #
    #     :param dt: a datetime object
    #     :return: new datetime object of the next tuesday at 12 AM
    #     """
