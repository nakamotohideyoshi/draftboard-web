#
# salary/management/commands/salarypool.py

from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
import sports.models
import sports.classes
import salary.models
import salary.classes
import roster.models
import roster.classes
from sports.parser import DataDenParser

class Command(BaseCommand):

    # help is a Command inner variable
    help = 'usage: ./manage.py salarypool <sport>'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('sport', nargs='+', type=str)
        # parser.add_argument('')

        # # Named (optional) arguments
        # parser.add_argument('--config',
        #     action='store_true',
        #     dest='delete',
        #     default=False,
        #     help='Delete poll instead of closing it')

    def handle(self, *args, **options):
        """
        generate a salary pool with a default config

        :param args:
        :param options:
        :return:
        """

        site_sport  = None
        config_name = None # set if site_sport exists
        for sport_name in options['sport']:
            try:
                site_sport = sports.models.SiteSport.objects.get(name=sport_name)
                config_name = sport_name + ' ' + timezone.now().strftime("%Y-%m-%d %H:%M:%S")
                self.ssm = sports.classes.SiteSportManager()
            except sports.models.SiteSport.DoesNotExist:
                raise CommandError('SiteSport "%s" does not exist' % sport_name)

            # check if there are any PlayerStats objects. If there are NOT,
            # then we cant generate salaries
            player_stats_class_list = self.ssm.get_player_stats_class( site_sport )
            for player_stats_model in player_stats_class_list:
                stats = player_stats_model.objects.filter( fantasy_points__gt=0 )
                if len(stats) <= 0:
                    #
                    #
                    p = DataDenParser()
                    p.setup(sport_name)

                stats = player_stats_model.objects.filter( fantasy_points__gt=0 )
                if len(stats) <= 0:
                    raise CommandError('you need to import player stats. try doing a one-time sports.DataDenParser.setup("SPORT")')
                else:
                    self.stdout.write('[%s] valid %s objects for ' % (str(len(stats)), str(player_stats_model.__name__)))

            # if ANY of the roster positions have been created, dont mess with them!
            # however, if NONE for the sport have been created, its reasonable
            # to automatically create them
            roster_spots = roster.models.RosterSpot.objects.filter( site_sport=site_sport )
            if len(roster_spots) > 0:
                #
                # dont modify existing rosters. this is the live site after all.
                self.stdout.write('[yes] roster exists for "%s"' % str(site_sport))

            else:
                self.stdout.write('[yes] creating default roster for "%s"' % str(site_sport))
                initial = roster.classes.Initial()
                initial.setup( site_sport.name )

        self.salary_conf                                    = salary.models.SalaryConfig()
        self.salary_conf.name                               = config_name
        self.salary_conf.trailing_games                     = 10
        self.salary_conf.days_since_last_game_flag          = 10
        self.salary_conf.min_games_flag                     = 7
        self.salary_conf.min_player_salary                  = 3000
        self.salary_conf.max_team_salary                    = 50000
        self.salary_conf.min_avg_fppg_allowed_for_avg_calc  = 7
        self.salary_conf.save()

        self.pool               = salary.models.Pool()
        self.pool.site_sport    = site_sport
        self.pool.salary_config = self.salary_conf
        self.pool.save()

        self.pool.active = True
        self.pool.save()

        self.__createTrailingGameWeight(self.salary_conf, 3,3)
        self.__createTrailingGameWeight(self.salary_conf, 7,2)
        self.__createTrailingGameWeight(self.salary_conf, 10,1)


        self.sg = salary.classes.SalaryGenerator(self.ssm.get_player_stats_class(sport=site_sport), self.pool)

        # can take ~20 seconds
        self.stdout.write('[yes] generating new salaries for "%s"' % str(site_sport))
        try:
            self.sg.generate_salaries()
        except:
            self.stdout.write('ERROR *** generating new salaries for "%s" failed' % str(site_sport))
            self.stdout.write('ERROR *** ... make sure you have run sports.classes.DataDenParser().setup("%s")' % site_sport.name)
            return

        # in Command objects, use stdout.write instead of print()
        self.stdout.write('[yes] created salary pool for "%s"' % str(site_sport))

    def __createTrailingGameWeight(self, salary_config, through, weight):
        trailing_game_weight                        = salary.models.TrailingGameWeight()
        trailing_game_weight.salary                 = salary_config
        trailing_game_weight.through                = through
        trailing_game_weight.weight                 = weight
        trailing_game_weight.save()