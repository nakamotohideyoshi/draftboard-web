#
# util/dfsdate.py

import pytz
from django.utils import timezone
from datetime import timedelta, datetime
from dateutil import tz

def timestamp_to_utc_datetime(unix_ts):
    """
    convert a unix timestamp into a datetime object with tzinfo=<UTC> !

    you must know that datetime.utcfromtimestamp() alone is nough enough!

    :param unix_ts:
    :return:
    """
    return datetime.utcfromtimestamp(unix_ts).replace(tzinfo=pytz.utc)

class DfsDate(object):

    est_tz = tz.gettz('America/New_York')

    nfl_weekdays_active     = [3,4,5,6,0]       # thursday thru monday. order MATTERS. do not re-order.
    nfl_weekdays_inactive   = [1,2]             # tuesday, wednesday. order MATTERS. do not re-order.

    @staticmethod
    def get_current_dfs_date():
        now = timezone.now()
        now_est = now.replace(tzinfo=DfsDate.est_tz)
        timedelta_est = now_est.dst()

        # if this is non-zero, add it to the amount of
        # seconds we subtract from the UTC time to get the EST time
        dst_seconds = timedelta_est.seconds
        total_seconds = 4*3600 + dst_seconds
        # ts = int(now.strftime('%s'))
        # ts -= ((4*3600) + dst_seconds)

        # subtract the 'total_seconds' from the original 'now' utc datetime.
        # that datetimes's date() should be the DFS "day".
        dfs_dt = now - timedelta(seconds=total_seconds)
        print('dfsdate date():', str(dfs_dt.date()))

        # We need to
        # get all the games on that day even
        # if they span over into the following day
        # in utc.
        return dfs_dt # TODO return just a date() object?

    @staticmethod
    def get_current_dfs_date_range(offset_hours=0):
        """
        return a tuple of (start_datetime, end_datetime) that are the boundaries
        of the current DFS day in UTC.

        :return:
        """

        td_offset = timedelta(hours=offset_hours)
        now = timezone.now()
        now_date = now.date()
        now_est = now.replace(tzinfo=DfsDate.est_tz)
        timedelta_est = now_est.dst()

        # if this is non-zero, add it to the amount of
        # seconds we subtract from the UTC time to get the EST time
        dst_seconds = timedelta_est.seconds
        total_seconds = 4*3600 + dst_seconds

        # subtract the 'total_seconds' from the original 'now' utc datetime.
        # that datetimes's date() should be the DFS "day".
        dfs_dt = DfsDate.get_current_dfs_date()
        #print('dfsdate date():', str(dfs_dt.date()))
        dfs_date = dfs_dt.date()

        # We need to get all the games on that day even
        # if they span over into the following day in utc.
        start = dfs_dt.replace(dfs_date.year, dfs_date.month, dfs_date.day, 5, 0, 0, 0)
        end = start + timedelta(days=1)

        # incoporate offset
        start = start + td_offset
        end = end + td_offset

        return (start, end)

    @staticmethod
    def get_current_nfl_date_range():
        """
        returns a tuple of (start

        :return:
        """

        # DfsDate.nfl_weekdays_active     # [3,4,5,6,0]
        # DfsDate.nfl_weekdays_inactive   # [1,2]

        rng = DfsDate.get_current_dfs_date_range()
        today_dt = rng[0]
        # print('rng.weekday():', rng[0].weekday())

        if today_dt.weekday() not in DfsDate.nfl_weekdays_active:
            while not (today_dt.weekday() == DfsDate.nfl_weekdays_active[0]):
                #
                # decrement 'today_dt' until its the desired day.
                # we will use 'today_dt' for the start of the week range
                today_dt = today_dt + timedelta(days=1)

        if today_dt.weekday() in DfsDate.nfl_weekdays_active:
            #
            # although its in the range, we want to return
            # the range that encompasses the week we are in.
            # subtract 1 days at a time while start.weekday() is not equal to 3
            while not (today_dt.weekday() == DfsDate.nfl_weekdays_active[0]):
                #
                # decrement 'today_dt' until its the desired day.
                # we will use 'today_dt' for the start of the week range
                today_dt = today_dt - timedelta(days=1)

            #
            # set end_dt to be +5 days from the new 'today_dt',
            # since the start has now been set to the thursday
            # we can easily add to get the following monday.
            end_dt = today_dt + timedelta(days=5)

            # print final date range for active nfl week
            print('get_current_nfl_date_range():', str(today_dt), str(end_dt))

        else:
            raise Exception('get_current_nfl_date_range() - today_dt.weekday() wasnt '
                            'in DfsDate.nfl_weekdays_active even after adjustment!')

        #
        # we used 'today_dt' for the start
        return (today_dt, end_dt)
