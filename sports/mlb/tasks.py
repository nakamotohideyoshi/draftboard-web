#
# mlb/tasks.py

from mysite.celery_app import app
from sports.mlb.parser import DataDenMlb

@app.task(bind=True)
def update_injuries(self):
    """
    dataden will be actively parsing in the injury data, but occasionally we need
    to clean it up (remove players who are no longer injured!)

    :return:
    """
    parser = DataDenMlb()
    parser.cleanup_injuries()