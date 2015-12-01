from __future__ import absolute_import

#
# contest/schedule/tasks.py

from datetime import timedelta
from mysite.celery_app import app
from django.core.cache import cache
from contest.schedule.classes import ScheduleManager

LOCK_EXPIRE = 30 # Lock expires in 30 seconds
SHARED_LOCK_NAME = "create_scheduled_contests"

@app.task
def create_scheduled_contests( hours_in_future=None ):
    """
    uses the ScheduleManager to create scheduled contests by calling
    ScheduleManager.run( td = td ).

    :param td: datetime.timedelta object representing the
                amount of time in the future from now to schedule for
    :return:
    """
    lock_id = 'task-LOCK-%s' % SHARED_LOCK_NAME

    acquire_lock = lambda: cache.add(lock_id, 'lock', LOCK_EXPIRE)
    release_lock = lambda: cache.delete(lock_id)

    if acquire_lock():
        try:
            sm = ScheduleManager()
            sm.run( time_delta=timedelta(hours=hours_in_future) )
        finally:
            release_lock()
