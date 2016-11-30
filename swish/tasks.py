from __future__ import absolute_import
from django.core.cache import cache
from mysite.celery_app import app
from swish.classes import (
    PlayerUpdateManager,
    SwishAnalytics,
)
from logging import getLogger

logger = getLogger('swish.tasks')
LOCK_EXPIRE = 59


@app.task(bind=True)
def update_injury_feed(self, sport):
    """
    update Swish Analytics injury feed and add PlayerUpdate(s) to our backend
    """
    lock_id = 'task-LOCK-update_injury_feed_%s' % sport
    acquire_lock = lambda: cache.add(lock_id, 'true', LOCK_EXPIRE)
    release_lock = lambda: cache.delete(lock_id)

    if acquire_lock():
        try:
            player_update_manager = PlayerUpdateManager(sport)
            swish = SwishAnalytics(sport)
            updates = swish.get_updates()
            for u in updates:
                try:
                    update_model = player_update_manager.update(u)
                except PlayerUpdateManager.PlayerDoesNotExist:
                    pass
            if player_update_manager.players_not_found:
                num_players_not_found = len(player_update_manager.players_not_found)
                logger.info('%s | [%s] swish players not found:' % (sport, num_players_not_found),
                            player_update_manager.players_not_found)

        finally:
            release_lock()
