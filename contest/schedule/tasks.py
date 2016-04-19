from __future__ import absolute_import

#
# contest/schedule/tasks.py

from datetime import timedelta

from mysite.celery_app import app
from django.core.cache import cache
from contest.schedule.classes import (
    ContestPoolScheduleManager,
)
from contest.schedule.models import (
    UpcomingBlock,
)

LOCK_EXPIRE         = 60  # lock expires in X seconds
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

@app.task
def create_scheduled_contest_pools(sport):
    """
    uses the ScheduleManager to create scheduled contests by calling
    ScheduleManager.run( td = td ).

    :param td: datetime.timedelta object representing the
                amount of time in the future from now to schedule for
    :return:
    """

    lock_expire  = 60  # lock expires in X seconds
    lock_name    = 'create_scheduled_contest_pools'

    # unique per sport, ie: task-LOCK--nfl--contest_pool_schedule_manager'
    lock_id = 'task-LOCK--%s--%s' % (sport, lock_name)

    acquire_lock = lambda: cache.add(lock_id, 'lock', lock_expire)
    release_lock = lambda: cache.delete(lock_id)

    if acquire_lock():
        try:
            # upcoming_blocks = UpcomingBlock.objects.filter(site_sport__name=sport,
            #                                             contest_pools_created=False)
            scheduler = ContestPoolScheduleManager(sport=sport)
            scheduler.create_upcoming_contest_pools()
            #scheduler.run()

        finally:
            release_lock()
