import ast
import json

from django.conf import settings
from django.core.cache import caches
from django.core.management.base import BaseCommand

from replayer.models import Update
from sports.classes import SiteSportManager
from sports.parser import DataDenParser


class Command(BaseCommand):
    """
    NOTE: Make sure you have Celery running before doing this, it won't work if you don't.
     
    Write a text file of all pbp events of a single game. This is used to test out the web
    client frontend debugger thing.
    
    As of now, we only save dataden events for 2 days, so the game must be from the past 2 days
    in order to get any json output.
    
    You can also use this with a replayer dump in order to dump out all of the events we sent
    to Pusher.
    
    If you get a JSON file writer error, you probably need to create a `tmp` directory in the 
    project root.

    Be careful doing this command twice. it simply appends to the output file, so you'll end
    up with a big file containing the output of all the commands you ran.

    Usage:

        $> ./manage.py export_pusher_events <sport> <game_srid>
        
    Example:
        python manage.py export_pusher_events nba 79d732e3-c5b2-4a32-9ec7-5267dfc856f2
    """

    # help is a Command inner variable
    help = 'usage: ./manage.py export_pusher_events <sport nba|nfl|mlb|nhl> <game_srid>'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('sport', nargs='+', type=str)
        parser.add_argument('srid', nargs='+', type=str)

    def handle(self, *args, **options):
        for name in settings.CACHES.keys():
            cache = caches[name]
            cache.clear()
            self.stdout.write('[%s] cache cleared!\n' % name)

        ssm = SiteSportManager()
        game_class = None
        sport = None
        pbp_list = []

        for sport_string in options['sport']:
            sport = sport_string
            game_class = ssm.get_game_class(sport_string)

        for game_srid in options['srid']:
            # Since we can't query by game_srid, we need to grab all events that are timestamped
            # after the game began, then loop though them trying to match game_srid in order
            # to determine if they are for the specified game or not.

            # Get the Game model.
            print('Getting Game for srid: %s' % game_srid)
            game = game_class.objects.get(srid=game_srid)

            print("Game found: %s" % game)

            # Find any dataden Updates that might be for that game, based on the timestamp.
            updates = Update.objects.filter(
                ts__gte=game.start
            )
            print(
                'Found %s potential PBP events. (not all of these are matches)' % updates.count())

            for update in updates:
                # The actual data is stored as a string'd python object. Eval it so we can check
                # it's game_srid.
                update_data = ast.literal_eval(update.o)
                game_id = update_data.get('game__id')
                if not game_id:
                    game_id = update_data.get('id')

                if game_id and game_id == game_srid:
                    pbp_list.append(update_data)

                    # send it through parser!

                    # Ideally we'd take the output of the parser here and output it to a file,
                    # but the system isn't setup like that. Instead I made an optional setting
                    # that will pipe anything we'd normally send to Pusher and output it to
                    # a text file. You can see that in `push.classes`, look
                    # for: settings.PUSHER_OUTPUT_TO_FILE to see the logic.
                    parser = DataDenParser()
                    ns_parts = update.ns.split('.')  # split namespace on dot for db and coll
                    db = ns_parts[0]
                    collection = ns_parts[1]
                    parser.parse_obj(db, collection, ast.literal_eval(update.o), async=False)

            # If you want to dump out the objects we got from Dataden, before they were run
            # through the parsers, uncomment these lines.
            #
            # file_path = 'tmp/dataden_events--%s_game__%s.json' % (sport, game_srid)

            # print("Writing out %s Dataden PBP events for this game to `%s`" % (
            #     len(pbp_list), file_path))
            #
            # with open(file_path, 'w') as outfile:
            #     json.dump(pbp_list, outfile)

            print('Done!')
