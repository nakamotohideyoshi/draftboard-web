#
# salary/management/commands/salaryplayer.py

from django.core.management.base import (
    BaseCommand,
)
from sports.classes import SiteSportManager
from salary.classes import (
    SportSalaryGenerator,
)

class Command(BaseCommand):

    # help is a Command inner variable
    help = 'usage: ./manage.py salaryplayer <player-srid>'

    def add_arguments(self, parser):
        parser.add_argument('player', nargs='+', type=str)

    def handle(self, *args, **options):
        """
        calculate a single players salary (for debugging purposes) using
        the sports main salary algorithm.

        this command will infer the sport using SiteSportManager
        so all that needs to be specified is the player srid!
        """

        # collect the player srids passed as arguments
        player_srids = []
        for srid in options['player']:
            player_srids.append(srid)

        player_srid = player_srids[0] # get the first one
        print('looking for player:', str(player_srid))

        # find the sports.<sport>.models.Player object
        ssm = SiteSportManager()
        player = None
        site_sport = None # the sport (the string name) of the sport the player was found in
        for sport in SiteSportManager.SPORTS:
            site_sport = ssm.get_site_sport(sport)
            player_class = ssm.get_player_class(site_sport)
            try:
                player = player_class.objects.get(srid=player_srid)
                break
            except player_class.DoesNotExist:
                self.stdout.write('checked %s for Player object but they werent found'%sport)
                pass

        # hopefully we found the player by now
        if player is None:
            self.stdout.write('player [%s] not found in any sport!' % player_srid)
            return
        # else:
        #     self.stdout.write('player:', str(player))

        # generate the salary for this player specifically, printing out all the player stats
        # objects used and the weighting involved in the calculations for debugging purposes.
        sg = SportSalaryGenerator(sport=site_sport.name, debug_srid=player_srid)
        sg.generate_salaries()


