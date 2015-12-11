#
# util/timeshift.py

#
############################################################
# "Sets the system time" without an operating system method.
#
# NOTE: The explicit purpose of delta_now() is
# so we can override django.utils.timezone.now with it
# in the django settings -- this will cause a seamless
# use of django.utils.timezone.now() ... except that
# it will now return the time +/- the delta seconds
# as set in the cache's django.conf.settings.DATETIME_DELTA_SECONDS_KEY
############################################################

from django.utils import timezone
from django.utils.timezone import utc
from django.conf import settings
from django.core.cache import caches
from datetime import datetime, timedelta

def set_system_time(datetime):
    """
    Sets the system time to match the datetime param
    by calculating the difference in seconds from
    the actual real world current time, and then by
    storing that delta_seconds value internally so that
    subsequent calls for the time will have the delta seconds
    added/subtracted.

    Note: django.utils.timezone.now() will return objects
    that reflect the new time after set_system_time() is called
    up until the point that the internally cached delta_seconds
    value expires (a timeout of a couple hours), or until
    reset_system_time() is called.

    :param datetime: a python datetime.datetime() object
    :return:
    """

    #
    # stores the difference between the actual_now and the datetime specified
    set_delta( int(actual_now().timestamp()) - int(datetime.timestamp()) )

def reset_system_time():
    """
    Zeroes out any timeshift by simply calling set_delta( 0 ).

    After calling this method, django.utils.timezone.now()
    should return the real world UTC time.

    :return:
    """
    set_delta( 0 )

def set_delta(seconds, expire_seconds=8*24*60*60):
    """
    This method will side effect django.utils.timezone.now()
    such that it will now have a hidden timedelta(seconds=seconds) added!

    :param seconds: the integer seconds we wish to apply to the system time
    :param expire_seconds: length of time the cache will hold the delta seconds value. default: 8*24*60*60,  (8 hours!)
    :return:
    """
    c = caches['default']
    c.set(settings.DATETIME_DELTA_SECONDS_KEY, seconds, expire_seconds)

def get_delta():
    """
    get the current delta value (seconds of timeshift)
    :return: integer
    """
    c = caches['default']
    delta_seconds = c.get(settings.DATETIME_DELTA_SECONDS_KEY)
    if delta_seconds is None:
        delta_seconds = 0
    return delta_seconds

def actual_now():
    """
    Get the server time, with no shift -- this gets the hardware time.

    :return:
    """
    return datetime.utcnow().replace(tzinfo=utc)

def delta_now():
    """
    Override the django.timezone.now() method in the a
    specific django settings.py file like this:

        >>> from django.utils import timezone
        >>> from util.timeshift import delta_now
        >>> timezone.now = delta_now

    ... and voila, from here on out, django.timezone.now()
    will actually call the method delta_now().

    :return:
    """
    c = caches['default']
    delta_seconds = c.get(settings.DATETIME_DELTA_SECONDS_KEY)
    if delta_seconds is None:
        delta_seconds = 0
    else:
        delta_seconds = int(delta_seconds)

    #
    return actual_now() - timedelta(seconds=delta_seconds)

