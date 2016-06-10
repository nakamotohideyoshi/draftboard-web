#
# nba/tasks.py

from mysite.celery_app import app
from sports.nba.parser import DataDenNba

@app.task(bind=True)
def update_injuries(self):
    """
    dataden will be actively parsing in the injury data, but occasionally we need
    to clean it up (remove players who are no longer injured!)

    :return:
    """
    parser = DataDenNba()
    parser.cleanup_injuries()

@app.task(bind=True)
def cleanup_rosters(self):
    """
    dataden will be actively parsing in the injury data, but occasionally we need
    to clean it up (remove players who are no longer injured!)

    :return:
    """
    parser = DataDenNba()
    parser.cleanup_rosters()
