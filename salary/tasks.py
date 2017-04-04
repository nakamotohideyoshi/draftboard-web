from __future__ import absolute_import

from hashlib import md5
from logging import getLogger

from django.conf import settings
from django.core.cache import cache
from raven.contrib.django.raven_compat.models import client

import sports.classes
from mysite.celery_app import app
from salary.models import Pool

"""
Note: Many imports happen at the task level because of circular import issues.
"""

logger = getLogger('salary.tasks')


@app.task(name='salary.tasks.check_current_projections_week', bind=True)
def check_current_projections_week(self):
    from statscom.classes import (
        ProjectionsWeekWebhook,
    )
    from statscom.sports.nfl import FantasyProjectionsNFL

    api = FantasyProjectionsNFL()
    data = api.get_projections()
    week = data.get('week')

    # send slack webhook with the week
    webhook = ProjectionsWeekWebhook()
    webhook.send(str(week))


@app.task(name='salary.tasks.generate_salaries_from_statscom_projections_nfl', bind=True)
def generate_salaries_from_statscom_projections_nfl(self):
    from salary.classes import (
        SalaryGeneratorFromProjections,
        PlayerProjection,
    )
    from statscom.sports.nfl import FantasyProjectionsNFL

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


@app.task(name='salary.tasks.generate_salaries_from_statscom_projections_nba', bind=True)
def generate_salaries_from_statscom_projections_nba(self):
    """
    NBA

     This task is kicked off from the django admin panel by pressing the
     'Generate Salaries using STATS.com projections` button here: /admin/salary/pool/

     First it runs FantasyProjectionsNBA to fetch all of tomorrow's NBA game projections from STATS.com,
     then generates salaries based on those projections in SalaryGeneratorFromProjections.
    """
    from statscom.sports.nba import FantasyProjectionsNBA
    from salary.classes import (
        SalaryGeneratorFromProjections,
        PlayerProjection,
    )

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
        print(msg)
        client.captureMessage(msg)


LOCK_EXPIRE = 60 * 10  # Lock expires in 10 minutes


@app.task(name='salary.tasks.generate_salaries_from_statscom_projections_mlb', bind=True)
def generate_salaries_from_statscom_projections_mlb(self):
    """
    MLB

     This task is kicked off from the django admin panel by pressing the
     'Generate Salaries using STATS.com projections` button here: /admin/salary/pool/

     First it runs FantasyProjectionsNBA to fetch all of tomorrow's NBA game projections from STATS.com,
     then generates salaries based on those projections in SalaryGeneratorFromProjections.
    """
    from statscom.sports.mlb import FantasyProjectionsMLB
    from salary.classes import (
        SalaryGeneratorFromProjections,
        PlayerProjection,
    )

    logger.info('action: generate_salaries_from_statscom_projections_mlb')
    sport = 'mlb'

    api = FantasyProjectionsMLB()
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
            logger.info('action: generate_salaries_from_statscom_projections_mlb - releasing lock')
            release_lock()

    else:
        msg = (
            'action: generate_salaries_from_statscom_projections_mlb - a task is already'
            'generating salaries for sport: %s (stats.com)' % sport)
        logger.error(msg)
        print(msg)
        client.captureMessage(msg)


LOCK_EXPIRE = 60 * 10  # Lock expires in 10 minutes


@app.task(name='salary.tasks.generate_salaries_for_sport', bind=True)
def generate_salaries_for_sport(self, sport):
    from salary.classes import SalaryGenerator

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
        # raise Exception(err_msg)


# @app.task
# def generate_salary(pool):
#     # ssm = sports.classes.SiteSportManager()
#     # player_stats_class = ssm.get_player_stats_class(pool.site_sport)
#     # sg = SalaryGenerator(player_stats_class, pool)
#     # sg.generate_salaries()
#     sport = pool.site_sport.name
#     generate_salaries_for_sport.delay(sport)


@app.task(name='salary.tasks.generate_season_fppgs')
def generate_season_fppgs(sport=None):
    """
    calculates and sets 'season_fppg' for all sports
    """
    from salary.classes import PlayerFppgGenerator

    season_fppg_generator = PlayerFppgGenerator()
    if sport is None:
        # updates all sports in SiteSportManager.SPORTS
        season_fppg_generator.update()
    elif sport in sports.classes.SiteSportManager.SPORTS:
        # update specific sports season_fppg
        season_fppg_generator.update_sport(sport)
    else:
        raise Exception('salary.tasks.generate_season_fppgs() - unknown sport[%s]' % sport)


@app.task(name='salary.tasks.clear_salary_locked_flags_for_draftgroup')
def clear_salary_locked_flags_for_draftgroup(draft_group=None):
    from salary.models import Salary
    from draftgroup.models import Player as DraftgroupPlayer

    if draft_group is None:
        client.captureMessage('No draft_group was supplied!')
        logger.error('No draft_group was supplied!')

    # Find all players in the draftgroup that have salaries. Return it in a flat list Salary IDs
    player_ids = DraftgroupPlayer.objects.filter(
        draft_group=draft_group,
        salary_player__isnull=False
    ).values_list('salary_player', flat=True)

    # Find all of matching Salary objects for thees players and reset
    # their `salary_locked` flags.
    salaries = Salary.objects.filter(id__in=player_ids).update(salary_locked=False)

    logger.info('%s of %s players have had their salary locks reset. DraftGroup: %s' % (
        len(player_ids), salaries, draft_group))
