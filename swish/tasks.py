from __future__ import absolute_import
from django.core.cache import cache
from mysite.celery_app import app
from draftgroup.models import PlayerUpdate, PlayerStatus
from swish.classes import (
    PlayerUpdateManager,
    SwishAnalytics,
    RotoWire,
)
from logging import getLogger
from draftgroup.serializers import PlayerUpdateSerializer
from django.db import transaction

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
            rotowire = RotoWire(sport)
            updates = rotowire.get_updates()
            with transaction.atomic():
                for player_update in updates:
                    pid = player_update.get_pid()
                    name = player_update.get_player_name()
                    player_srid = player_update_manager.get_srid_for(pid=pid, name=name)
                    status, created = PlayerStatus.objects.get_or_create(
                        player_id=pid,
                        sport=sport,
                        player_srid=player_srid,
                    )
                    status.status = player_update.get_injury_status()
                    status.save()
            for u in updates:
                try:
                    update_model = player_update_manager.update(u)
                except PlayerUpdateManager.PlayerDoesNotExist:
                    pass
            if player_update_manager.players_not_found:
                num_players_not_found = len(player_update_manager.players_not_found)
                logger.warning('%s | [%s] rotowire players not found:' % (sport, num_players_not_found))

                for player in player_update_manager.players_not_found:
                    logger.warning('%s | rotowire player not found: %s' % (sport, player))
            else:
                updates = PlayerUpdate.objects.filter(sport=sport).order_by('-updated_at')
        finally:
            release_lock()
