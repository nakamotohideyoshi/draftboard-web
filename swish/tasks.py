from __future__ import absolute_import

from logging import getLogger

from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.db import transaction

import sports.classes
from draftgroup.models import PlayerStatus
from mysite.celery_app import app
from statscom.models import PlayerLookup
from swish.classes import (
    PlayerUpdateManager,
    RotoWire,
)
from swish.exception import RotowireDownException

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

            news = rotowire.get_news()
            for u in news:
                try:
                    update_model = player_update_manager.update(u)
                except PlayerUpdateManager.PlayerDoesNotExist:
                    pass
            if player_update_manager.players_not_found:
                num_players_not_found = len(player_update_manager.players_not_found)
                logger.warning(
                    '%s | [%s] rotowire players not found:' % (sport, num_players_not_found))

                for player in player_update_manager.players_not_found:
                    logger.warning('%s | rotowire player not found: %s' % (sport, player))
        except RotowireDownException as e:
            logger.warning('%s | rotowire api is down, url: %s' % (sport, e.response.url))
        finally:
            release_lock()


@app.task(bind=True)
def update_lookups(self, sport):
    """
    Rotowire provides us with a service that matches sportsradar SRIDs with stats.com's StatsGlobalId
    so that we don't have to do linking manually. This task will call that service and create
    PlayerLookup objects.
    """
    players_not_found = []
    # Keep track of how many we've created.
    lookups_created = 0
    try:
        rotowire = RotoWire(sport)
        players_data = rotowire.get_players()

        for p in players_data:
            if p.get('StatsGlobalId'):
                site_sport_manager = sports.classes.SiteSportManager()
                site_sport = site_sport_manager.get_site_sport(sport)
                player_model_class = site_sport_manager.get_player_class(site_sport)
                lookup = PlayerLookup.objects.filter(pid=p.get('StatsGlobalId'))

                try:
                    """
                    There should ONLY be 1 lookup for each player. If we have less than one
                    or more than one, delete any existing and create a new one.
                    """
                    if lookup.count() > 1:
                        raise IndexError('More than 1 lookup exist!')
                    # Grab the first one! (this will error out and proceed to create one if
                    # one does not exist.
                    lookup = lookup[0]

                    if not lookup.player_id and (lookup.sport == sport.upper() or not lookup.sport):
                        lookup.player_id = player_model_class.objects.get(srid=p.get('SportsDataId')).id
                        lookup.player_type = ContentType.objects.get_for_model(player_model_class)
                        if not lookup.sport:
                            lookup.sport = sport.upper()
                        lookup.save()
                # If there is none, or more than one lookup, delete any existing and make a new one.
                except (PlayerLookup.DoesNotExist, IndexError):
                    lookup.delete()
                    try:
                        player = player_model_class.objects.get(srid=p.get('SportsDataId'))
                        PlayerLookup.objects.create(
                            sport=sport.upper(),
                            player_type=ContentType.objects.get_for_model(player_model_class),
                            player_id=player.id,
                            pid=p.get('StatsGlobalId'),
                            first_name=player.first_name,
                            last_name=player.last_name
                        )
                        logger.info('Created lookup for: %s' % player)
                        # Increase the counter.
                        lookups_created = lookups_created + 1
                    except player_model_class.DoesNotExist:
                        players_not_found.append(p)

                except player_model_class.DoesNotExist:
                    players_not_found.append(p)

    except RotowireDownException as e :
        logger.warning('%s | rotowire api is down, url: %s' % (sport, e.response.url))

    for player in players_not_found:
        logger.info('%s | player not found: %s %s' % (
            sport, player.get('FirstName'), player.get('LastName')))

    # Summary of task.
    msg = {
        "task": "update_lookups - %s" % sport,
        "lookups created": lookups_created,
        "players not found": len(players_not_found),
    }

    logger.info(msg)
    return msg
