#
# mlb/tasks.py

from mysite.celery_app import app
from sports.mlb.parser import DataDenMlb
from dataden.classes import MlbSeason

@app.task(bind=True)
def update_season_fppg(self, season):
    """

    :param season: the "season
    :return:
    """
    season = MlbSeason()
    game_ids = season.get_game_ids_regular_season( season )
    # TODO

@app.task(bind=True)
def update_injuries(self):
    """
    dataden will be actively parsing in the injury data, but occasionally we need
    to clean it up (remove players who are no longer injured!)

    :return:
    """
    parser = DataDenMlb()
    parser.cleanup_injuries()