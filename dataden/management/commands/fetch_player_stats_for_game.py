from logging import getLogger

import pymongo
from django.conf import settings
from django.core.management.base import BaseCommand

from dataden.cache.caches import LiveStatsCache
from dataden.watcher import UpdateWorker, OpLogObj

logger = getLogger()


class Command(BaseCommand):
    """
    In the off chance that we don't have final player stats for a game, due to a crashing trigger
    or something like that, this command will query the mongodb directly and parse the latest
    stats.

    It takes the supplied `game_srid` and queries the proper `sport` table in mongo, runs the
    results through the UpdateWorker, which then sends the events off to be parsed and saved.

    This should result in all final PlayerStats being up-to-date. Once this is done, we can
    manually close a game by setting it's status to closed, then paying out the contest.

    Usage:

        $> ./manage.py fetch_player_stats_for_game <sport> <game_srid>

    Example:
        python manage.py fetch_player_stats_for_game nba 79d732e3-c5b2-4a32-9ec7-5267dfc856f2
    """

    # help is a Command inner variable
    help = 'usage: ./manage.py fetch_player_stats_for_game <sport nba|nfl|mlb|nhl> <game_srid>'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('sport', nargs=1, type=str)
        parser.add_argument('game_srid', nargs=1, type=str)

    def handle(self, *args, **options):
        if options['sport'][0] == 'nfl':
            logger.warning("\n\nYou inputted 'nfl'. you probably mean 'nflo'!\n")
        # Disable any pusher updates. We don't want to send parsed events to any connected clients.
        settings.PUSHER_ENABLED = False
        # Run celery in synchronous mode so we don't need to fire up a celery worker to run this.
        # NOTE: if one of the stat_update jobs fail, we can disable these lines to run it in async
        # mode, which won't kill the process due to one bad task.
        settings.CELERY_ALWAYS_EAGER = True
        settings.CELERY_TASK_ALWAYS_EAGER = True
        settings.CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

        # Get our input arguments straight.
        sport = options['sport'][0]
        game_srid = options['game_srid'][0]
        logger.info('Connecting to mongo db...')

        # Our mongo databases are named after the sport they contain, connect to the specified DB.
        client = pymongo.MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
        db = client[sport]
        # Where the player stats are kept in the sport database
        collection = db.player

        logger.info('Querying stats... (this can take a while)')

        # Grab stats from the specified game. We sort them ascending so that they are parsed in the
        # order they happened, the final ones parsed last.
        game_player_stats = collection.find(
            {
                'game__id': game_srid,
                # MLB stats come from a differnet sportsradar api.
                "$or": [{
                    # NBA, NHL, & NFL
                    "parent_api__id": 'stats'
                }, {
                    # MLB
                    "parent_api__id": "summary"
                }]
            }
        ).sort('dd_updated__id', pymongo.ASCENDING)

        logger.info("%s items found" % game_player_stats.count())

        # An empty object list that we will stuff events into.
        obj_list = []

        # Loop through the mongo cursor and stuff our event list.
        for player_stat in game_player_stats:
            # We have to massage the data a little bit because the UpdateWorker is expecting a
            # mongo oplog object which is slightly different than what a normal mongo query
            # result looks like.
            obj_list.append({
                'o': player_stat,
                'ns': '%s.player' % sport
            })

        logger.info("Preparing to parse events...")

        # Start our worker thread that will run through each event in the list and have it parsed
        # by celery.. kinda... this is run synchronously so there is no need for a celery worker.
        live_stats_cache = LiveStatsCache('default', clear=False)
        worker = UpdateWorker(obj_list, OpLogObj, live_stats_cache)
        worker.start()
