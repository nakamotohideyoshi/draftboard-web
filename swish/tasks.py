from __future__ import absolute_import

from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
import sports.classes
from draftgroup.classes import AbstractUpdateManager
from mysite.celery_app import app
from draftgroup.models import PlayerUpdate, PlayerStatus
from statscom.models import PlayerLookup
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
            news = rotowire.get_news()
            injuries = rotowire.get_injuries()
            with transaction.atomic():
                PlayerStatus.objects.filter(sport=sport).delete()
                for player_update in injuries:
                    try:
                        update_model = player_update_manager.update(player_update)
                        pid = player_update.get_pid()
                        player_srid = update_model.player_srid
                        status, created = PlayerStatus.objects.get_or_create(
                            player_id=pid,
                            sport=sport,
                            player_srid=player_srid,
                        )

                        status.status = player_update.get_injury_status()
                        status.save()
                    except PlayerUpdateManager.PlayerDoesNotExist:
                        pass

            for u in news:
                try:
                    update_model = player_update_manager.update(u)
                except PlayerUpdateManager.PlayerDoesNotExist:
                    pass
            if player_update_manager.players_not_found:
                num_players_not_found = len(player_update_manager.players_not_found)
                logger.warning('%s | [%s] rotowire players not found:' % (sport, num_players_not_found))

                for player in player_update_manager.players_not_found:
                    logger.warning('%s | rotowire player not found: %s' % (sport, player))
        finally:
            release_lock()


@app.task(bind=True)
def update_lookups(self, sport):
    rotowire = RotoWire(sport)
    players_data = rotowire.get_players()
    players_not_found = []
    for p in players_data:
        if p.get('StatsGlobalId'):
            site_sport_manager = sports.classes.SiteSportManager()
            site_sport = site_sport_manager.get_site_sport(sport)
            player_model_class = site_sport_manager.get_player_class(site_sport)
            try:
                print(p.get('StatsGlobalId'))
                lookup = PlayerLookup.objects.get(pid=p.get('StatsGlobalId'), sport=sport.upper())
                if not lookup.player_id:
                    lookup.player_id = player_model_class.objects.get(srid=p.get('SportsDataId')).id
                    lookup.player_type = ContentType.objects.get_for_model(player_model_class)
                    lookup.save()
            except PlayerLookup.DoesNotExist:
                print(p.get('SportsDataId'))
                try:
                    pid = player_model_class.objects.get(srid=p.get('SportsDataId')).id
                    PlayerLookup.objects.create(
                        sport=sport.upper(),
                        player_type=ContentType.objects.get_for_model(player_model_class),
                        player_id=pid,
                        pid=p.get('StatsGlobalId'),
                        first_name=p.get('StatsGlobalId'),
                        last_name=p.get('StatsGlobalId')
                    )
                except player_model_class.DoesNotExist:
                    players_not_found.append(p)
    for player in players_not_found:
        logger.warning('%s | player not found: %s %s' % (sport, player.get('FirstName'), player.get('LastName')))
