from __future__ import absolute_import

from mysite.celery_app import app, locking
from .models import Pool
from .classes import SalaryGenerator, PlayerFppgGenerator
import sports.classes
from django.conf import settings
from celery import task
from django.core.cache import cache
from hashlib import md5

LOCK_EXPIRE = 60 * 10 # Lock expires in 10 minutes

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


