#
# salary/dummy.py

"""
Everything in dummy.py is written for the strict purpose of making it easier
to create fake players, rosters, or anything neccessary to be able to test
salary pools (and this code may also be useful for testing draft groups & lineups...
or anything that interacts with salary stuff.
"""
from collections import OrderedDict
from test.models import PlayerChild, PlayerStatsChild, GameChild
from django.utils import timezone
from .classes import SalaryGenerator
from datetime import date, timedelta
from random import randint
from .models import SalaryConfig, TrailingGameWeight, Pool
from sports.models import SiteSport, Position
from roster.models import RosterSpot, RosterSpotPosition

#
# THIS CLASS SHOULD ONLY BE USED ON THE TEST DATABASE!
# IT WILL ADD TEMPORARY/FAKE DATA YOU DONT WANT IN PRODUCTION.

# EXAMPLE USAGE:
#
# from salary.dummy import Dummy
# class SomeTest(AbstractTest):
#     def setUp(self):
#         Dummy.create_sport_and_rosters()
#         self.player_stats = Dummy.create_basic_player_stats()

class Dummy(object):

    DEFAULT_SPORT = 'testsport'

    DEFAULT_ROSTER_MAP = {

        ('QB',1,0,True)     :['QB'],
        ('WR',1,1,True)     :['WR'],
        ('FLEX',1,2,False)  :['RB','WR','TE']
    }

    # Shared setup methods for the test cases
    @staticmethod
    def create_roster(sport=DEFAULT_SPORT, roster=DEFAULT_ROSTER_MAP):
        """
        example usage: the top level keys are tuples, the lists contain positions,
        each tuple key has the form: ('roster spot name',amount,idx,is_primary_boolean)
            >>> roster = {
            ...     ('QB',1,0,True)     :['QB'],
            ...     ('WR',1,1,True)     :['WR'],
            ...     ('FLEX',1,1,False)  :['RB','WR','TE']
            ... }
            >>> site_sport = Dummy.create_roster(sport='mysport', roster=roster )

        :param sport:
        :param roster:
        :return:
        """

        ret_roster_spot_position_list = []

        # order the incoming roster dict by the idx
        ordered_roster = OrderedDict(sorted(roster.items(), key=lambda k: k[0][2]))

        site_sport, created = SiteSport.objects.get_or_create(name=sport)
        print(site_sport, 'site_sport')

        # create the roster spot mappings
        for rs_tuple, pos_names_list in ordered_roster.items():
            roster_spot_name    = rs_tuple[0]
            roster_spot_amount  = rs_tuple[1]
            roster_spot_idx     = rs_tuple[2]
            primary             = rs_tuple[3]
            print('roster spot: %s, amount:%s, idx:%s, is_primary:%s' % (roster_spot_name,
                                    roster_spot_amount, roster_spot_idx, primary))
            for pos_name in pos_names_list:
                    #
                    # 'c' is a boolean indicating whether the object was created or not
                    position, c             = Position.objects.get_or_create(name=pos_name,
                                                                             site_sport=site_sport)
                    #print('    ', position)
                    roster_spot, c          = RosterSpot.objects.get_or_create(name=roster_spot_name,
                                                                       amount=roster_spot_amount,
                                                                       idx=roster_spot_idx,
                                                                       site_sport=site_sport)
                    #print('    ', roster_spot)
                    roster_spot_position, c = RosterSpotPosition.objects.get_or_create(position=position,
                                                                               roster_spot=roster_spot,
                                                                               is_primary=primary)
                    ret_roster_spot_position_list.append(roster_spot_position)
                    print('    ', roster_spot_position)
        print('...created!')
        return ret_roster_spot_position_list

    @staticmethod
    def create_player_stats(sport=DEFAULT_SPORT):
        """
        return a newly created player who could fit in the default roster.

        if 'roster' is None, we will call Dummy.create_roster() and use that data

        :param sport:
        :param roster:
        :return:
        """

        # ('QB',1,0,True)     :['QB'],
        position = None
        for rs_tuple, pos_list in Dummy.DEFAULT_ROSTER_MAP.items():
            for pos_name in pos_list:
                site_sport, c = SiteSport.objects.get_or_create(name=sport)
                position, c = Position.objects.get_or_create(name=pos_name,
                                                          site_sport=site_sport)
                break
            break
        if position is None:
            raise Exception('>>>>> Dummy.create_player_stats() couldnt find any positions in roster')

        dt_now  = timezone.now()
        unix_ts = dt_now.strftime('%s') # unix timestamp as srid ... not bad

        game    = Dummy.create_game(srid='game'+unix_ts)
        player  = Dummy.create_player(srid='player'+unix_ts, position=position)

        player_stats = Dummy.create_player_stats_model(game, player)

        return player_stats

    @staticmethod
    def create_game(srid, status='closed'):
        dt_now = timezone.now()
        game                            = GameChild()
        game.srid                       = srid
        game.start                      = dt_now
        game.status                     = status
        game.save()
        return game

    @staticmethod
    def create_player(srid, position):
        player                          = PlayerChild()
        player.srid                     = srid
        player.first_name               = "Jon"
        player.last_name                = "Doe"
        player.position                 = position
        player.save()
        return player

    @staticmethod
    def create_player_stats_model(game, player):
        player_stats                    = PlayerStatsChild()
        player_stats.fantasy_points     = randint(0, 100)
        player_stats.game               = game
        player_stats.player             = player
        player_stats.srid_game          = game.srid
        player_stats.srid_player        = player.srid
        player_stats.position           = player.position
        player_stats.save()
        return player_stats

    @staticmethod
    def create_games(n=20):
        dt_now  = timezone.now()
        unix_ts = int(dt_now.strftime('%s')) # unix timestamp as srid ... not bad
        games = []
        for x in range(0, n):
            games.append( Dummy.create_game(srid='%s' % (unix_ts+x)))
        return games

    @staticmethod
    def create_players(n=20):
        """
        calls Dummy.create_roster() and then creates X players using the positions from the roster
        """
        dt_now = timezone.now()
        unix_ts = int(dt_now.strftime('%s'))
        Dummy.create_roster()
        positions = Position.objects.all()
        size = len(positions)
        players = []
        for x in range(0, n):
            pos_idx = x % (size)
            players.append( Dummy.create_player(srid='%s' % (unix_ts+x), position=positions[pos_idx]))
        return players

    @staticmethod
    def create_player_stats_list(players=20, games=20):
        """
        calls Dummy.create_roster() as a preqrequisite

        'players' is the number of players we want to create
        'games' is the number of games for which we will generate player stats for each player for

        :param players:
        :param games:
        :return:
        """
        player_stats_list = []
        players = Dummy.create_players(n=players)    # n=20 is the default argument which creates 20 players
        games   = Dummy.create_games(n=games)      # n=20 is default for game as well
        for game in games:
            for player in players:
                player_stats_list.append( Dummy.create_player_stats_model( game, player ) )
        print(len(player_stats_list), 'player_stats objects created. here are the first 15...')
        for ps in player_stats_list[:15]:
            print('    ', str(ps))
        return player_stats_list

    @staticmethod
    def create_salary_config():
        salary_conf                                    = SalaryConfig()
        salary_conf.trailing_games                     = 10
        salary_conf.days_since_last_game_flag          = 10
        salary_conf.min_games_flag                     = 7
        salary_conf.min_player_salary                  = 3000
        salary_conf.max_team_salary                    = 50000
        salary_conf.min_avg_fppg_allowed_for_avg_calc  = 5
        salary_conf.save()
        return salary_conf

    @staticmethod
    def generate_salaries(sport=DEFAULT_SPORT, pool_active=True):
        """
        it is a prerequisite that create_roster() and create_player_stats_list() have been called first

        returns the SalaryGenerator which created the salaries.
        """

        # prerequisite calls to create_roster(), create_player_stats_list()
        Dummy.create_roster()
        Dummy.create_player_stats_list()

        #
        # create the config and the pool
        site_sport, c = SiteSport.objects.get_or_create(name=sport)

        salary_conf = Dummy.create_salary_config()

        pool                = Pool()
        pool.site_sport     = site_sport
        pool.salary_config  = salary_conf
        pool.active         = pool_active
        pool.save()

        Dummy.create_trailing_game_weight(salary_conf, 3,  3)
        Dummy.create_trailing_game_weight(salary_conf, 7,  2)
        Dummy.create_trailing_game_weight(salary_conf, 10, 1)

        #
        # now use SalaryGenerator class on these objects
        player_stats_classes = [
            PlayerStatsChild
        ]
        generator = SalaryGenerator( player_stats_classes, pool )
        generator.generate_salaries()
        return generator

    @staticmethod
    def create_trailing_game_weight(salary_config, through, weight):
        trailing_game_weight                        = TrailingGameWeight()
        trailing_game_weight.salary                 = salary_config
        trailing_game_weight.through                = through
        trailing_game_weight.weight                 = weight
        trailing_game_weight.save()