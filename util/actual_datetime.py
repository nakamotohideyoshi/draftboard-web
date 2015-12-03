#
# util/actual_datetime.py

import subprocess
from redis import Redis
from django.utils import timezone
from datetime import datetime, timedelta

def now():
    """
    returns the actual datetime.

    adds DATETIME_DELTA (from Redis) to the servers current time (ie: django.utils.timezone.now())

    :return: datetime.datetime() object
    """
    ad = ActualDatetime()
    return ad.actual_now()

def set_system_time(datetime_object):
    """
    calculates the offset from the target datetime_object and the current time, and saves
    the different, in seconds to Redis.

    then sets the system time to the specified target datetime

    :param datetime_object:
    :return:
    """
    ad = ActualDatetime()
    ad.set_time( datetime_object )

def reset_system_time():
    """
    set the server time back to the actual time
    wrapper for:

        >>> ad = ActualDatetime()
        >>> ad.reset_time()

    :return:
    """
    ad = ActualDatetime()
    ad.reset_time()

class ActualDatetime:

    DATETIME_DELTA_SECONDS = 'DATETIME_DELTA_SECONDS'
    # DATETIME_DELTA_EXPIRES = 4*60 # in seconds

    def __init__(self):
        self.redis          = Redis()

    def set_time(self, datetime):
        """
        calculates the offset from the target datetime and the current time, and saves
        the different, in seconds to Redis.

        then sets the system time to the specified target datetime

        :param target_datetime:
        :return:
        """
        now     = timezone.now()
        unix_ts = int(now.strftime('%s'))
        unix_ts_target = int(datetime.strftime('%s'))
        delta_seconds = unix_ts - unix_ts_target
        # save the delta seconds value in REdis
        self.set_delta(delta_seconds)
        # actuall change the server clock
        self.__set_system_time( datetime )

    def reset_time(self):
        """
        reset the stored delta seconds value to 0 and
        change the time back to the real world current time
        """
        self.set_delta( 0 )
        self.__reset_system_time()

    def __set_system_time(self, dt):
        """
        set the system time to the datetime obj
        """
        dt2  = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, tzinfo=dt.tzinfo )
        #proc    = subprocess.call(['sudo','hwclock','--set','--date',str(dt2)])
        proc   = subprocess.call(['sudo','date','-s',str(dt2)])

    def __reset_system_time(self):
        """
        sets the system time back to whatever the hardware clock time is
        """
        proc = subprocess.call(['sudo','hwclock','-s'])

    def get_delta(self):
        sec = self.redis.get(self.DATETIME_DELTA_SECONDS)
        #print( type(sec), int(sec), str(sec) )
        if sec is None:
            return 0
        return int(sec)

    def set_delta(self, seconds):
        #self.redis.setex(self.DATETIME_DELTA_SECONDS, seconds, self.DATETIME_DELTA_EXPIRES) # expire in 4 hours
        self.redis.set(self.DATETIME_DELTA_SECONDS, seconds)

    def actual_now(self):
        return timezone.now() + timedelta(seconds=self.get_delta())

