#
# schedule/management/commands/contestpool.py

from django.core.management.base import NoArgsCommand
from contest.schedule.classes import ScheduleManager
from contest.schedule.classes import ContestPoolCreator
from prize.models import PrizeStructure
from sports.classes import SiteSportManager

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
        prize_structure = PrizeStructure.objects.all()[5]

        #
        contest_pool_creator = ContestPoolCreator(the_sport, prize_structure, game.start, 500)
        contest_pool = contest_pool_creator.get_or_create()