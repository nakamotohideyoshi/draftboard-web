#

from dataden.watcher import OpLogObjWrapper
from dataden.classes import Trigger, DataDen
from dataden.signals import Update

import sports.nba.parser
import sports.mlb.parser
import sports.nhl.parser
import sports.nfl.parser

import scoring.classes

import sports.nba.models
import sports.mlb.models
import sports.nhl.models
import sports.nfl.models

class DataDenParser(object):
    """
    returns a parser for a sport
    """
    NAMESPACE = 'ns'

    parsers = {
        'nba' : sports.nba.parser.DataDenNba,
        'mlb' : sports.mlb.parser.DataDenMlb,
        'nhl' : sports.nhl.parser.DataDenNhl,
        'nfl' : sports.nfl.parser.DataDenNfl,
    }

    #
    # list of default triggers for the basic needs of the four major sports
    DEFAULT_TRIGGERS = [
        # mlb
        ('mlb','team','hierarchy'),	        # 1
        ('mlb','game','schedule_pre'),      # 2
        ('mlb','game','schedule_reg'),      # 2
        ('mlb','game','schedule_pst'),      # 2
        ('mlb','player','team_profile'),    # 3
        ('mlb','game','boxscores'),
        ('mlb','home','summary'),
        ('mlb','away','summary'),
        ('mlb','player','summary'),

        # nba
        ('nba','team','hierarchy'),     # 1
        ('nba','game','schedule'),      # 2
        ('nba','player','rosters'),     # 3
        ('nba','game','boxscores'),
        ('nba','team','boxscores'),
        ('nba','player','stats'),

        # nhl
        ('nhl','team','hierarchy'),     # 1
        ('nhl','game','schedule'),      # 2
        ('nhl','player','rosters'),     # 3
        ('nhl','game','boxscores'),
        ('nhl','team','boxscores'),
        ('nhl','player','stats'),

        # nfl
        ('nfl','team','hierarchy'),     # 1
        ('nfl','game','schedule'),     # 2
        ('nfl','player','rosters'),     # 3 ordered for setup priority
        ('nfl','game','boxscores'),
        ('nfl','team','stats'),
        ('nfl','team','boxscores'),
        ('nfl','player','stats')
    ]

    def __init__(self):
        self.sport = None

    @staticmethod
    def get_for_sport(sport):
        """
        get the parser for a specific sport by its string name

        :param sport:
        :return:
        """
        parser = DataDenParser.parsers.get( sport, None )
        if parser is None:
            raise Exception('parser does not exist for sport: ' + str(sport))

        return parser()

    def get_sport_from_namespace(self, obj):
        ns = obj.get_ns()
        return ns.split('.')[0] # sport always on the left side of the dot

    def __get_parser(self, sport):
        dataden_sport_parser = self.parsers[ sport ]
        return dataden_sport_parser()

    def parse(self, obj):
        """
        inspect the namespace of the object, and pass it to the proper sport parser
        """
        self.sport = self.get_sport_from_namespace( obj )
        parser = self.__get_parser( self.sport )
        parser.parse( obj ) # the sub parser will infer what type of object it is

    def setup_triggers(self, sport=None, enable=True):
        """
        Installs the triggers specified by DEFAULT_TRIGGERS to the database.
        Existing triggers will not be modified, so it can be called frequently.

        You can specify a single sport to setup triggers for with 'sport' param.

        By default, a trigger created by this method will be enabled,
        but you can override that with the 'enable' param set to False.

        Does NOT start the process which actual runs the watcher
        which starts sending signals when new objects are parsed!

        :return:
        """
        if sport:
            self.__valid_sport(sport) # exception if it is not valid

        for t in self.DEFAULT_TRIGGERS:
            if sport and sport != t[0]:
                continue # skip all that dont match, if sport is specified
            db          = t[0]
            coll        = t[1]
            parent_api  = t[2]
            trg = Trigger.create( db, coll, parent_api, enable=enable )
        print('created triggers')

    def setup(self, sport, async=False):
        """
        NOTE: This method should ONLY BE CALLED after dataden.jar has run
        and populated its own database for whatever sport you
        are calling setup for!

        This methods goal is to setup the Teams, Games, and Players,
        so that we might start parsing live stats effectively via
        PlayerStats, and GameBoxscore objects.

        This method installs the funadmental triggers required
        for DataDen to signal objects have been parsed.

        Step 1: setup the Team(s) from the hierarchy parent_api
        Step 2: setup the Game(s) from the schedule(s)
        Step 3: setup the Players from the rosters

        ... after step 3 has successfully finished you should
        be able to add whatever dataden triggers you would like.

        :param sport:
        :return:
        """

        self.__valid_sport(sport) # make sure we can set it up
        self.setup_triggers(sport)
        dataden = DataDen()

        #
        # the DEFAULT_TRIGGERS has each sport ordered to initialize it.
        #   parse the teams
        #   parse the schedule for the games
        #   parse the rosters for the players
        for t in self.DEFAULT_TRIGGERS:
            if t[0] != sport:
                continue # skip sports we didnt specify
            #
            # as a debug, print out the 'ns' and the 'parent_api', and count
            db          = t[0]
            coll        = t[1]
            parent_api  = t[2]
            print( 'ns:%s.%s, parent_api:%s' % (db,coll,parent_api) )
            cursor = dataden.find(db,coll,parent_api)
            print( ' ... count: ' + str(cursor.count()))

            for mongo_obj in cursor:
                #
                # create a oplog wrapper with the mongo object and signal it
                # so the parser takes care of the rest!
                self.parse_obj( db, coll, mongo_obj, async=async )

    def setup_score_players_for_sport(self, sport):
        if sport == 'nfl':
            self.setup_score_players(score_system_class=scoring.classes.NflSalaryScoreSystem,
                                            player_stats_model=sports.nfl.models.PlayerStats)
        elif sport == 'nhl':
            self.setup_score_players(score_system_class=scoring.classes.NhlSalaryScoreSystem,
                                            player_stats_model=sports.nhl.models.PlayerStats)
        elif sport == 'nba':
            self.setup_score_players(score_system_class=scoring.classes.NbaSalaryScoreSystem,
                                            player_stats_model=sports.nba.models.PlayerStats)
        elif sport == 'mlb':
            self.setup_score_players(score_system_class=scoring.classes.MlbSalaryScoreSystem,
                                            player_stats_model=sports.mlb.models.PlayerStats)

    def setup_score_players(self, score_system_class, player_stats_model):
        #from scoring.classes import NflSalaryScoreSystem
        #from sports.nfl.models import PlayerStats
        sport_scorer = score_system_class()
        stats = player_stats_model.objects.all()
        size = len(stats)
        for i,s in enumerate(stats):
            #print( '(%s of %s)', i+1, size)
            s.fantasy_points = sport_scorer.score_player( s, verbose=True )
            print('')
            print( '(%s of %s)' % (str(i+1), size), 'total', s.fantasy_points, '|', sport_scorer.get_str_stats() )
            s.save()

    def parse_obj(self, db, coll, mongo_obj, async=False):
        """
        mongo_obj is a dataden object without the oplog wrapper

        this method wraps the mongo_obj so it can be signaled,
        and sends it to the parser to automatically parse it into the django db

        :param db:
        :param coll:
        :param mongo_obj:
        :return:
        """
        Update( OpLogObjWrapper( db, coll, mongo_obj ) ).send( async=async )

    def setup_all(self):
        """
        call setup() on all the sports

        :return:
        """
        sports = self.__get_valid_sports()
        for sport in sports:
            self.setup( sport )

    def __get_valid_sports(self):
        """
        Get a list of the sport names which this class can call setup() for.

        :return:
        """
        l = []
        for tup in self.DEFAULT_TRIGGERS:
            sport = tup[0]
            if sport not in l:
                l.append( sport )
        return l

    def __valid_sport(self, sport):
        """
        return True if sport exists in the DEFAULT_TRIGGERS

        :param sport:
        :return:
        """
        if sport in self.__get_valid_sports():
            return True
        raise Exception('invalid sport >>> %s <<< ! sport must be in: %s' % (sport,
                                                        str(self.__get_valid_sports())))

class ProviderParser(object):
    """
    get an object that can parse our providers objects
    """
    parsers = {
        'dataden' : DataDenParser,

        # ... implement and add more providers here
    }

    @staticmethod
    def get_for_provider(provider):
        provider_parser = ProviderParser.parsers.get(provider, None)
        if provider_parser is None:
            raise Exception('provider_parser [%s] does not exist' % str(provider))

        return provider_parser()
