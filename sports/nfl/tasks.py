#
# nfl/tasks.py

from mysite.celery_app import app
from sports.nfl.parser import DataDenNfl
from sports.nfl.classes import (
    NflRecentGamePlayerStats,
)
from sports.nfl.models import (
    Game,
)

@app.task(bind=True)
def update_injuries(self):
    """
    dataden will be actively parsing in the injury data, but occasionally we need
    to clean it up (remove players who are no longer injured!)

    :return:
    """
    parser = DataDenNfl()
    parser.cleanup_injuries()

@app.task(bind=True)
def cleanup_rosters(self):
    """
    dataden will be actively parsing in the injury data, but occasionally we need
    to clean it up (remove players who are no longer injured!)

    :return:
    """
    parser = DataDenNfl()
    parser.cleanup_rosters()

@app.task(bind=True)
def update_nfl_recent_game_player_stats_task(self, game_statuses=[]):

    # TODO get a lock? idk - this wont be running _that_ often

    # get relevant games (inprogress) so we can run this updater live games
    statuses = list(game_statuses)
    if len(statuses) == 0:
        # if no statuses are passed in, assume this is for INPROGRESS GAMES ONLY
        statuses = [
            Game.STATUS_INPROGRESS,
        ]

    # get the relevant games specified by a list of target statuses
    relevant_games = Game.objects.filter(status__in=statuses)

    # get instance of updater outside of the loop
    nfl_recent_game_player_stats = NflRecentGamePlayerStats()

    for game in relevant_games:
        nfl_recent_game_player_stats.update(game.srid)