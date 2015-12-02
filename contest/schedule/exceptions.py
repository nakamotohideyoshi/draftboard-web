#
# contest/schedule/exceptions.py

class ScheduleException(Exception):
    """
    generic exception for an exception that would blocked
    the rest of the schedule from running.
    """
    def __init__(self, schedule_name):
        super().__init__('exception with schedule: %s' % schedule_name)

class ScheduleOutOfRangeException(Exception):
    """
    raised if ScheduleManager.run() is equal to or greater than timedelta(days=7)
    """
    def __init__(self):
        super().__init__('timedelta object is invalid. a valid range is between 0 and 6 days inclusive...')
