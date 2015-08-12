#
# salary/dummy.py

"""
Everything in dummy.py is written for the strict purpose of making it easier
to create fake players, rosters, or anything neccessary to be able to test
salary pools (and this code may also be useful for testing draft groups & lineups...
or anything that interacts with salary stuff.
"""

from collections import OrderedDict
from test.models import PlayerChild, PlayerStatsChild, GameChild, TeamChild
from django.utils import timezone
from .classes import SalaryGenerator
from datetime import date, timedelta
from random import randint
from .models import SalaryConfig, TrailingGameWeight, Pool
from sports.models import SiteSport, Position
from roster.models import RosterSpot, RosterSpotPosition
from sports.classes import SiteSportManager

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

    DEFAULT_SPORT = 'test'

    DEFAULT_ROSTER_MAP = {

        ('QB',1,0,True)     :['QB'],
        ('WR',1,1,True)     :['WR'],
        ('FLEX',1,2,False)  :['RB','WR','TE']
    }

    # this class will iterate these to create dummy teams
    # if game or player objects need foreign keys to them
    DEFAULT_TEAMS = [
        ('away','AWAY'),
        ('home','HOME')
    ]

    def __init__(self, sport):
        """
        Create dummy objects. This could interfere with the live site,
        and is strictly meant for testing environments, and specifically
        the "./manage.py test" tool
        """
        self.ssm        = SiteSportManager()
        self.site_sport = self.ssm.get_site_sport( sport )

    def generate(self):
        """
        essentially does what generate_salaries() does, but for the
        sport this class was instantiated with, whereas generate_salaries()
        is a static method which uses the default sport and
        GameChild / PlayerChild tables.

        Use to this to make more realistic instances in the database
        of players/games/playerstats/salaries/etc...
        """
        # prerequisite calls to create_roster(), create_player_stats_list()
        Dummy.create_roster(sport=self.site_sport.name)
        Dummy.create_player_stats_list(site_sport=self.site_sport)
        #players = Dummy.create_players(n=players, site_sport=site_sport)   #  -done
        #games   = Dummy.create_games(n=games, site_sport=site_sport)       #  -done
        #create_player_stats_model( players,games)                          #  -done

        salary_conf = Dummy.create_salary_config()   #  -done no changes

        pool                = Pool()                #  -done no changes
        pool.site_sport     = self.site_sport       #  -done use member variable
        pool.salary_config  = salary_conf           #  -done no changes
        pool.active         = True                  #  -done default True so its useable
        pool.save()

        Dummy.create_trailing_game_weight(salary_conf, 3,  3)   # -done
        Dummy.create_trailing_game_weight(salary_conf, 7,  2)   # -done
        Dummy.create_trailing_game_weight(salary_conf, 10, 1)   # -done

        #
        # the SiteSportManager.get_player_stats_class()
        # method actually returns a list of sport.<sport>.PlayerStats subclasses for the sport
        player_stats_classes = self.ssm.get_player_stats_class( self.site_sport ) # -done

        generator = SalaryGenerator( player_stats_classes, pool )   # -done
        generator.generate_salaries()                               # -done
        return generator                                            # -done

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
            >>> site_sport = Dummy.create_roster(sport='mysport', roster=roster ) #example!

        :param sport:
        :param roster:
        :return:
        """

        ret_roster_spot_position_list = []

        # order the incoming roster dict by the idx
        ordered_roster = OrderedDict(sorted(roster.items(), key=lambda k: k[0][2]))

        site_sport, created = SiteSport.objects.get_or_create(name=sport)
        #print(site_sport, 'site_sport')

        # create the roster spot mappings
        for rs_tuple, pos_names_list in ordered_roster.items():
            roster_spot_name    = rs_tuple[0]
            roster_spot_amount  = rs_tuple[1]
            roster_spot_idx     = rs_tuple[2]
            primary             = rs_tuple[3]
            # print('roster spot: %s, amount:%s, idx:%s, is_primary:%s' % (roster_spot_name,
            #                         roster_spot_amount, roster_spot_idx, primary))
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
                    #print('    ', roster_spot_position)
        #print('...created!')
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

        ssm = SiteSportManager()
        site_sport = ssm.get_site_sport( sport )
        game    = Dummy.create_game(srid='game'+unix_ts, site_sport=site_sport)

        player  = Dummy.create_player(srid='player'+unix_ts,
                         position=position, team=game.home, site_sport=site_sport)

        if sport == Dummy.DEFAULT_SPORT:
            site_sport = None # hack for backwards compatability, to not break older code
        player_stats = Dummy.create_player_stats_model(game, player, site_sport)

        return player_stats

    @staticmethod
    def create_team(srid, alias, site_sport=None):
        if site_sport is None:
            t, created = TeamChild.objects.get_or_create(srid=srid, alias=alias)
        else:
            ssm = SiteSportManager()
            team_model = ssm.get_team_class( site_sport )
            t, created = team_model.objects.get_or_create(srid=srid, alias=alias)
        return t

    @staticmethod
    def create_game(srid=None, status='scheduled', away=None, home=None, site_sport=None):
        #site_sport, created = SiteSport.objects.get_or_create(name=sport)

        if away is None:
            away    = Dummy.create_team('away', 'AWAY', site_sport)
        if home is None:
            home    = Dummy.create_team('home', 'HOME', site_sport)

        dt_now = timezone.now()
        if site_sport is None:
            game                    = GameChild()
        else:
            ssm = SiteSportManager()
            game_model = ssm.get_game_class( site_sport )
            game = game_model()

        game.srid               = srid
        game.start              = dt_now
        game.status             = status

        game.away               = away
        game.home               = home

        game.save()
        return game

    @staticmethod
    def create_player(srid, position, team, site_sport=None):

        player                          = PlayerChild()
        player.srid                     = srid
        player.first_name               = "Jon"
        player.last_name                = "Doe"
        player.position                 = position

        player.team                     = team

        player.save()
        return player

    @staticmethod
    def create_player_stats_model(game, player, site_sport=None):
        """
        If site_sport is not specified, defaults to use PlayerStatsChild model

        may not work to well for baseball since there
        are 2 PlayerStats types (hitter/pitcher)
        """
        if site_sport is None:
            player_stats = PlayerStatsChild()
        else:
            ssm = SiteSportManager()
            player_stats_model_list = ssm.get_player_stats_class( site_sport )
            player_stats_model = player_stats_model_list[0]
            player_stats = player_stats_model()

        player_stats.fantasy_points     = randint(0, 100)
        player_stats.game               = game
        player_stats.player             = player
        player_stats.srid_game          = game.srid
        player_stats.srid_player        = player.srid
        player_stats.position           = player.position
        player_stats.save()
        return player_stats

    @staticmethod
    def create_games(n=20, site_sport=None):
        #site_sport, created = SiteSport.objects.get_or_create(name=sport)
        dt_now  = timezone.now()
        unix_ts = int(dt_now.strftime('%s')) # unix timestamp as srid ... not bad
        games = []
        for x in range(0, n):
            games.append( Dummy.create_game(srid='%s' % (unix_ts+x), site_sport=site_sport ) )
        return games

    @staticmethod
    def create_players(n=20, teams=DEFAULT_TEAMS, site_sport=None):
        """
        calls Dummy.create_roster() and then creates X players using the positions from the roster
        """
        team_list = []
        for t in teams:
            team, create = TeamChild.objects.get_or_create( srid=t[0], alias=t[1] )
            team_list.append( team )
        n_teams = len(team_list)

        dt_now = timezone.now()
        unix_ts = int(dt_now.strftime('%s'))
        if site_sport is None:
            Dummy.create_roster()
        else:
            Dummy.create_roster( sport = site_sport.name )
        positions = Position.objects.all()
        size = len(positions)
        players = []
        for x in range(0, n):
            pos_idx = x % (size)
            players.append( Dummy.create_player(srid='%s' % (unix_ts+x),
                                                position=positions[ pos_idx ],
                                                team=team_list[ x % n_teams ],
                                                site_sport=site_sport ) )
        return players

    @staticmethod
    def create_player_stats_list(players=20, games=20, site_sport=None):
        """
        calls Dummy.create_roster() as a preqrequisite

        'players' is the number of players we want to create
        'games' is the number of games for which we will generate player stats for each player for

        :param players:
        :param games:
        :return:
        """

        player_stats_list = []
        players = Dummy.create_players(n=players, site_sport=site_sport)    # n=20 is the default argument which creates 20 players
        games   = Dummy.create_games(n=games, site_sport=site_sport)      # n=20 is default for game as well
        for game in games:
            for player in players:
                player_stats_list.append( Dummy.create_player_stats_model( game, player, site_sport ) )
        #print(len(player_stats_list), 'player_stats objects created. here are the first 15...')
        # for ps in player_stats_list[:15]:
        #     print('    ', str(ps))
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
        internally, in this order, calls:
            - create_roster()
            - create_player_stats_list()

        returns the SalaryGenerator which created the salaries.
        """

        # prerequisite calls to create_roster(), create_player_stats_list()
        Dummy.create_roster(sport=sport)
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