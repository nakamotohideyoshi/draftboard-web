from __future__ import absolute_import
from django.core.cache import cache
from mysite.celery_app import app
from draftgroup.models import PlayerUpdate, PlayerStatus
from swish.classes import (
    PlayerUpdateManager,
    SwishAnalytics,
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
            swish = SwishAnalytics(sport)
            updates = swish.get_updates()
            player_ids = [str(upd.data.get('playerId')) for upd in updates]
            player_ids_str = ",".join(player_ids)
            player_extra_data = swish.get_player_extra_data_multiple(player_id=player_ids_str)
            with transaction.atomic():
                for p in player_extra_data:
                    status, created =PlayerStatus.objects.get_or_create(
                        player_id=p.get('playerId'),
                        sport=sport,
                        player_srid=player_update_manager.get_srid_for(pid=p.get('playerId'), name=p.get('playerName')),
                        status=p.get('playerStatus'),
                        updated_at=p.get('lastTextReportedAt'))
                    if not created:
                        status.status = p.get('playerStatus')
                        status.save()
            for u in updates:
                try:
                    update_model = player_update_manager.update(u)
                except PlayerUpdateManager.PlayerDoesNotExist:
                    pass
            if player_update_manager.players_not_found:
                num_players_not_found = len(player_update_manager.players_not_found)
                logger.warning('%s | [%s] swish players not found:' % (sport, num_players_not_found))

                for player in player_update_manager.players_not_found:
                    logger.warning('%s | swish player not found: %s' % (sport, player))
            else:
                updates = PlayerUpdate.objects.filter(sport=sport).order_by('-updated_at')
        finally:
            release_lock()
