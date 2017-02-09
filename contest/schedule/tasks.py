from __future__ import absolute_import

#
# contest/schedule/tasks.py

from mysite.celery_app import app
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from contest.schedule.classes import ContestPoolScheduleManager
from contest.schedule.models import UpcomingBlock
from logging import getLogger

logger = getLogger('contest.schedule.tasks')
LOCK_EXPIRE = 60  # lock expires in X seconds
SHARED_LOCK_NAME = 'contest_pool_schedule_manager'


@app.task(bind=True)
def contest_pool_schedule_manager(self, sport):
    """
    This creates the daily game block schedules for each sport that can be seen here: /admin/schedule/upcomingblock/

    uses the ScheduleManager to create scheduled contests by calling
    ScheduleManager.run( td = td ).

    :param sport
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


@app.task(bind=True)
def create_scheduled_contest_pools(self, sport):
    """
    uses the ScheduleManager to create scheduled contest pools by calling
    ScheduleManager.create_upcoming_contest_pools.

    :param sport
    :return:
    """

    lock_expire = 60  # lock expires in X seconds
    lock_name = 'create_scheduled_contest_pools'

    # unique per sport, ie: task-LOCK--nfl--contest_pool_schedule_manager'
    lock_id = 'task-LOCK--%s--%s' % (sport, lock_name)

    acquire_lock = lambda: cache.add(lock_id, 'lock', lock_expire)
    release_lock = lambda: cache.delete(lock_id)

    if acquire_lock():
        try:
            #
            scheduler = ContestPoolScheduleManager(sport=sport)
            scheduler.create_upcoming_contest_pools()

        except ContestPoolScheduleManager.ActiveBlockNotFoundException:
            logger.warning('No Block was found for %s', scheduler)
            pass

        finally:
            release_lock()


@app.task(bind=True)
def send_upcoming_issues(self):
    """
    sending email with upcoming issues

    """
    sports = ['nba', 'nfl', 'mlb', 'nhl']
    data = {}
    for sport in sports:
        blocks = UpcomingBlock.objects.get_tomorrow_blocks().filter(site_sport__name=sport)

        if blocks.exists():
            data[sport] = blocks
    subject = 'Upcoming issues'
    ctx = {
        'data': data
    }

    message = render_to_string('emails/upcoming_games.html', ctx)
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, settings.SITE_ADMIN_EMAIL)
