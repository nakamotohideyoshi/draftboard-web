from __future__ import absolute_import

#
# tasks.py

from django.core.cache import cache
from mysite.celery_app import app
from swish.classes import (
    PlayerUpdateManager,
    SwishNFL,
)

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
            swish = SwishNFL() # TODO other sports, not just NFL
            updates = swish.get_updates()
            for u in updates:
                try:
                    update_model = player_update_manager.update(u)
                except PlayerUpdateManager.PlayerDoesNotExist:
                    pass
            num_players_not_found = len(player_update_manager.players_not_found)
            print('%s | [%s] swish players not found:' % (sport, str(num_players_not_found)),
                                                str(player_update_manager.players_not_found))

        finally:
            release_lock()
