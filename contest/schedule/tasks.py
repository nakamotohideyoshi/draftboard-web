from __future__ import absolute_import

from logging import getLogger

from django.conf import settings
from django.core.cache import cache
from django.template.loader import render_to_string

from contest.schedule.classes import ContestPoolScheduleManager
from contest.schedule.models import UpcomingBlock
from draftgroup.exceptions import NotEnoughGamesException
from mysite.celery_app import app
from mysite.utils import send_email

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
    logger.info('Creating contest pools for sport: %s' % sport)
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

        except NotEnoughGamesException as e:
            logger.warning(e)
            pass

        finally:
            release_lock()
    else:
        logger.info('task-LOCK exists for this task.')

@app.task(bind=True)
def send_upcoming_contest_schedule_email(self):
    """
    send email with upcoming contest schedules to site admins.
    """
    sports = ['nba', 'nfl', 'mlb', 'nhl']
    data = {}
    for sport in sports:
        blocks = UpcomingBlock.objects.get_tomorrow_blocks().filter(site_sport__name=sport)

        if blocks.exists():
            data[sport] = blocks
    ctx = {
        'data': data
    }

    message = render_to_string('emails/upcoming_games.html', ctx)
    send_email(
        title="Draftboard Contest Schedule",
        subject="Today's Draftboard Games",
        message=message,
        recipients=settings.SITE_ADMIN_EMAIL
    )
