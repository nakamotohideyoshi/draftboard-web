from __future__ import absolute_import

#
# contest/schedule/tasks.py

from datetime import timedelta

from mysite.celery_app import app
from django.core.cache import cache
from contest.schedule.classes import (
    ContestPoolScheduleManager,
)

LOCK_EXPIRE         = 60  # lock expires in 30 seconds
SHARED_LOCK_NAME    = 'contest_pool_schedule_manager'

@app.task
def contest_pool_schedule_manager(sport):
    """
    uses the ScheduleManager to create scheduled contests by calling
    ScheduleManager.run( td = td ).

    :param td: datetime.timedelta object representing the
                amount of time in the future from now to schedule for
    :return:
    """

    # unique per sport, ie: task-LOCK--nfl--contest_pool_schedule_manager'
    lock_id = 'task-LOCK--%s--%s' % (sport, SHARED_LOCK_NAME)

    acquire_lock = lambda: cache.add(lock_id, 'lock', LOCK_EXPIRE)
    release_lock = lambda: cache.delete(lock_id)

    if acquire_lock():
        try:
            scheduler = ContestPoolScheduleManager(sport=sport)
            scheduler.run()

        finally:
            release_lock()
