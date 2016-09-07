#
# schedule/management/commands/contestpool.py

from django.core.management.base import NoArgsCommand
from contest.schedule.classes import ScheduleManager
from contest.schedule.classes import ContestPoolCreator
from prize.models import PrizeStructure
from sports.classes import SiteSportManager
from random import Random

class Command(NoArgsCommand):

    help = "create a ContestPool using a Game SRID (any sport)"

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('values', nargs='+', type=str)

    def handle(self, *args, **options):

        values = []
        for x in options['values']:
            values.append( x )

        game_srid = values[0]
        duration = 500
        try:
            duration = int(values[1]) # defaults to
        except IndexError:
            pass # there wasnt a duration specified, just use the default

        # find the Game -- check all sports
        ssm = SiteSportManager()
        game = None
        the_sport = None
        for sport in SiteSportManager.SPORTS:
            game_class = ssm.get_game_class(sport)
            try:
                game = game_class.objects.get(srid=game_srid)
                the_sport = sport
                break
            except game_class.DoesNotExist:
                pass
            self.stdout.write('checked %s for Game but it wasnt found'%sport)

        if game is None or the_sport is None:
            self.stdout.write('No game found for any sport '
                              '%s matching srid: %s\n' % (SiteSportManager.SPORTS, game_srid))

        # get a prize structure that hopefully exists
        prize_structures = PrizeStructure.objects.all()
        count = prize_structures.count()
        r = Random()
        prize_structure = prize_structures[r.randint(0, count-1)]
        self.stdout.write('randomly chosen prize structure: %s' % str(prize_structure))

        #
        contest_pool_creator = ContestPoolCreator(the_sport, prize_structure, game.start, duration)
        contest_pool = contest_pool_creator.get_or_create()