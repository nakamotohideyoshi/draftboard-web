import ast
import json

from django.core.management.base import BaseCommand

from replayer.models import Update
from sports.classes import SiteSportManager


class Command(BaseCommand):
    """
    Write a json file of all pbp events of a single game. This is used to test out the web
    client frontend debugger thing.
    
    As of now, we only save pbp events for 2 days, so the game must be from the past 2 days
    in order to get any json output.
    
    If you get a JSON file writer error, you probably need to create a `tmp` directory in the 
    project root.

    Usage:

        $> ./manage.py export_game_pbp <sport> <game_srid>
        
    Example:
        python manage.py export_game_pbp nba 79d732e3-c5b2-4a32-9ec7-5267dfc856f2
    """

    # help is a Command inner variable
    help = 'usage: ./manage.py export_game_pbp <sport nba|nfl|mlb|nhl> <game_srid>'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('sport', nargs='+', type=str)
        parser.add_argument('srid', nargs='+', type=str)

    def handle(self, *args, **options):
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

            # Find any pbp event Updates that might be for that game, based on the timestamp.
            updates = Update.objects.filter(
                ts__gte=game.start,
                ns='%s.event' % sport
            )
            print(
                'Found %s potential PBP events. (not all of these are matches)' % updates.count())

            for update in updates:
                # The actual data is stored as a string'd python object. Eval it so we can check
                # it's game_srid.
                update_data = ast.literal_eval(update.o)

                if update_data['game__id'] == game_srid:
                    pbp_list.append(update_data)

                    # send it thru parser!
                    # This doesn't work because parsing an object doesn't return anything, it just
                    # parses and sends on to Pusher :(
                    # parser = DataDenParser()
                    # ns_parts = update.ns.split('.')  # split namespace on dot for db and coll
                    # db = ns_parts[0]
                    # collection = ns_parts[1]
                    # print(
                    # parser.parse_obj(db, collection, ast.literal_eval(update.o), async=False))

            file_path = 'tmp/pbp_events__%s_game__%s.json' % (sport, game_srid)

            print("Writing out %s PBP events for this game to `%s`" % (len(pbp_list), file_path))

            with open(file_path, 'w') as outfile:
                json.dump(pbp_list, outfile)

            print('Done!')
