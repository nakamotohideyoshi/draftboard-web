from __future__ import absolute_import

from mysite.celery_app import app
from .classes import SalaryGenerator, PlayerFppgGenerator
import sports.classes


@app.task
def generate_salary(pool):
    ssm = sports.classes.SiteSportManager()
    player_stats_class = ssm.get_player_stats_class(pool.site_sport)
    sg = SalaryGenerator(player_stats_class, pool)
    sg.generate_salaries()

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


