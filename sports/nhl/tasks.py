#
# nhl/tasks.py

from mysite.celery_app import app
from sports.nhl.parser import DataDenNhl

@app.task(bind=True)
def update_injuries(self):
    """
    dataden will be actively parsing in the injury data, but occasionally we need
    to clean it up (remove players who are no longer injured!)

    :return:
    """
    parser = DataDenNhl()
    parser.cleanup_injuries()