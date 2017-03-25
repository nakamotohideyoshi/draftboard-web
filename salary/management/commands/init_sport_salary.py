from django.core.management.base import BaseCommand, CommandError
import sports.models
import sports.classes
from salary.models import Pool
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from logging import getLogger

from salary.models import Salary
logger = getLogger('management')


class Command(BaseCommand):
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('pool_id', nargs='+', type=int)

    def handle(self, *args, **options):
        """
        If for some reason you can't spawn contests because you have a SalaryPool without 
        player Salaries, this will run through all of the <sport>.Player objects we have
        and create Salary models for them with the salary.amount set to whatever the
        sport's minimum salary is.
        
        You probably won't need to run this except for when a brand new sport needs to be
        added.


        :param args:
        :param options:
        :return:
        """
        for pool_id in options['pool_id']:
            salary_pool = Pool.objects.get(id=pool_id)
            site_sport = salary_pool.site_sport
            ssm = sports.classes.SiteSportManager()
            player_class = ssm.get_player_class(site_sport)
            player_type = ContentType.objects.get_for_model(player_class)
            sport_players = player_class.objects.all()
            salary_conf = salary_pool.salary_config
            # roster_spots = RosterSpot.objects.filter(site_sport=site_sport)

            print('site_sport:', site_sport)
            print('player_class: ', player_class)
            print('player_type: ', player_type)
            print('sport_players count: ', sport_players.count())

            for player in sport_players:
                print('--------------')
                try:
                    Salary.objects.get(
                        pool=salary_pool, player_type=player_type, player_id=player.id)
                    print('Salary object exists in this pool for player: %s' % player)
                    pass
                except Salary.DoesNotExist:
                    print('Player has no Salary in this pool, creating one. %s' % player)
                    print('rosterspots: ', player.position.rosterspotposition_set.all())
                    player_primary_roster = player.position.rosterspotposition_set.all()
                    if player_primary_roster.count():

                        # If a player has no Salary, create one.
                        salary = Salary.objects.create(
                            pool=salary_pool,
                            player_type=player_type,
                            player_id=player.id,
                            amount=salary_conf.min_player_salary,
                            primary_roster=player_primary_roster[0].roster_spot
                        )
                        print(salary)
                    else:
                        print('Player has no roster spot, they are likely NFL defense, or '
                              'MLB relief pitcher')
