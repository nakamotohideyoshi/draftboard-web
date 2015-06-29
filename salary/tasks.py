from __future__ import absolute_import

from mysite.celery_app import app
from .classes import SalaryGenerator
import sports.classes


@app.task
def generate_salary(pool):
    ssm = sports.classes.SiteSportManager()
    player_stats_class = ssm.get_player_stats_class(pool.site_sport)
    sg = SalaryGenerator(player_stats_class, pool)
    sg.generate_salaries()



