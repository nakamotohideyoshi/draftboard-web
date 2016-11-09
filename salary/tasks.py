from __future__ import absolute_import
from raven.contrib.django.raven_compat.models import client
from mysite.celery_app import app
import sports.classes
from django.conf import settings
from celery import task
from django.core.cache import cache
from hashlib import md5
from statscom.classes import (
    FantasyProjectionsNFL,
    FantasyProjectionsNBA,
    ProjectionsWeekWebhook,
)
from salary.classes import (
    SalaryGeneratorFromProjections,
    SalaryGenerator,
    PlayerProjection,
    PlayerFppgGenerator,
)
from salary.models import Pool
from logging import getLogger

logger = getLogger('salary.tasks')


@app.task(bind=True)
def check_current_projections_week(self):
    api = FantasyProjectionsNFL()
    data = api.get_projections()
    week = data.get('week')

    # send slack webhook with the week
    webhook = ProjectionsWeekWebhook()
    webhook.send(str(week))


@app.task(bind=True)
def generate_salaries_from_statscom_projections_nfl(self):
    """ NFL """
    # from statscom.classes import FantasyProjectionsNFL
    api = FantasyProjectionsNFL()
    # projections = api.get_projections(week=1)
    # player_projections = api.get_player_projections(week=1)
    player_projections = api.get_player_projections()

    Pool.objects.all().count()
    pool = Pool.objects.get(site_sport__name='nfl')
    # salary_generator = SalaryGeneratorFromProjections(
    #   player_projections, PlayerProjection, pool, slack_updates=settings.SLACK_UPDATES)
    # salary_generator.generate_salaries()

    sport_md5 = md5(str('nfl').encode('utf-8')).hexdigest()
    lock_id = '{0}-LOCK-generate-salaries-for-sport-{1}'.format(self.name, sport_md5)

    # cache.add fails if the key already exists
    acquire_lock = lambda: cache.add(lock_id, 'true', LOCK_EXPIRE)
    # advantage of using add() for atomic locking
    release_lock = lambda: cache.delete(lock_id)

    if acquire_lock():
        try:
            # start generating the salary pool, time consuming...
            salary_generator = SalaryGeneratorFromProjections(
                player_projections, PlayerProjection, pool, slack_updates=settings.SLACK_UPDATES)
            salary_generator.generate_salaries()

        finally:
            release_lock()

    else:
        err_msg = 'a task is already generating salaries for sport: nfl (stats.com)'
        print(err_msg)
        # raise Exception(err_msg)


@app.task(bind=True)
def generate_salaries_from_statscom_projections_nba(self):
    """
    NBA

     This task is kicked off from the django admin panel by pressing the
     'Generate Salaries using STATS.com projections` button here: /admin/salary/pool/

     First it runs FantasyProjectionsNBA to fetch all of tomorrow's NBA game projections from STATS.com,
     then generates salaries based on those projections in SalaryGeneratorFromProjections.
    """
    logger.info('action: generate_salaries_from_statscom_projections_nba')
    sport = 'nba'

    api = FantasyProjectionsNBA()
    player_projections = api.get_player_projections()
    logger.info('FINAL player_projections count: %s' % len(player_projections))
    Pool.objects.all().count()
    pool = Pool.objects.get(site_sport__name=sport)

    sport_md5 = md5(str(sport).encode('utf-8')).hexdigest()
    lock_id = '{0}-LOCK-generate-salaries-for-sport-{1}'.format(self.name, sport_md5)

    logger.info('action: generate_salaries_from_statscom_projections_nba - acquiring lock')
    # cache.add fails if the key already exists
    acquire_lock = lambda: cache.add(lock_id, 'true', LOCK_EXPIRE)
    # advantage of using add() for atomic locking
    release_lock = lambda: cache.delete(lock_id)

    if acquire_lock():
        try:
            # start generating the salary pool, time consuming...
            salary_generator = SalaryGeneratorFromProjections(
                player_projections, PlayerProjection, pool, slack_updates=settings.SLACK_UPDATES)
            salary_generator.generate_salaries()
        except Exception as e:
            logger.error(e)
            client.captureException()
        finally:
            logger.info('action: generate_salaries_from_statscom_projections_nba - releasing lock')
            release_lock()

    else:
        msg = (
            'action: generate_salaries_from_statscom_projections_nba - a task is already'
            'generating salaries for sport: %s (stats.com)' % sport)
        logger.error(msg)
        client.captureMessage(msg)

LOCK_EXPIRE = 60 * 10  # Lock expires in 10 minutes


@app.task(bind=True)
def generate_salaries_for_sport(self, sport):
    ssm = sports.classes.SiteSportManager()
    site_sport = ssm.get_site_sport(sport)
    pool = Pool.objects.get(site_sport=site_sport, active=True)
    player_stats_class = ssm.get_player_stats_class(pool.site_sport)
    # The cache key consists of the task name and the MD5 digest of the sport
    sport_md5 = md5(str(sport).encode('utf-8')).hexdigest()
    lock_id = '{0}-LOCK-generate-salaries-for-sport-{1}'.format(self.name, sport_md5)

    # cache.add fails if the key already exists
    acquire_lock = lambda: cache.add(lock_id, 'true', LOCK_EXPIRE)
    # advantage of using add() for atomic locking
    release_lock = lambda: cache.delete(lock_id)

    if acquire_lock():
        try:
            # start generating the salary pool, time consuming...
            sg = SalaryGenerator(player_stats_class, pool, slack_updates=settings.SLACK_UPDATES)
            sg.generate_salaries()
        finally:
            release_lock()
        return sport
    else:
        err_msg = 'a task is already generating salaries for sport: %s' % sport
        print(err_msg)
        #raise Exception(err_msg)

# @app.task
# def generate_salary(pool):
#     # ssm = sports.classes.SiteSportManager()
#     # player_stats_class = ssm.get_player_stats_class(pool.site_sport)
#     # sg = SalaryGenerator(player_stats_class, pool)
#     # sg.generate_salaries()
#     sport = pool.site_sport.name
#     generate_salaries_for_sport.delay(sport)


@app.task
def generate_season_fppgs(sport=None):
    """
    calculates and sets 'season_fppg' for all sports
    """

    season_fppg_generator = PlayerFppgGenerator()
    if sport is None:
        # updates all sports in SiteSportManager.SPORTS
        season_fppg_generator.update()
    elif sport in sports.classes.SiteSportManager.SPORTS:
        # update specific sports season_fppg
        season_fppg_generator.update_sport(sport)
    else:
        raise Exception('salary.tasks.generate_season_fppgs() - unknown sport[%s]' % str(sport))
