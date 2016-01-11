#
# sports/classes.py

from django.contrib.contenttypes.models import ContentType

from .models import (
    SiteSport,
    PlayerStats,
    Player,
    Game,
    Team,
    GameBoxscore,
    PbpDescription,
    Injury,

    # tsx content related
    TsxNews,
    TsxInjury,
    TsxTransaction,

    # tsx objects which reference the content objects
    TsxTeam,
    TsxPlayer,
)

from .exceptions import (
    GameBoxscoreClassNotFoundException,
    SiteSportWithNameDoesNotExistException,
    GameClassNotFoundException,
    TeamClassNotFoundException,
    PbpDescriptionClassNotFoundException,
    InjuryClassNotFoundException,
    InjurySerializerClassNotFoundException,
    TeamSerializerClassNotFoundException,
    PlayerSerializerClassNotFoundException,
    GameSerializerClassNotFoundException,
    BoxscoreSerializerClassNotFoundException,
    PlayerHistorySerializerClassNotFoundException,
    TsxModelClassNotFoundException,
    TsxSerializerClassNotFoundException,
)

from mysite.exceptions import IncorrectVariableTypeException
import dataden.classes

import sports.nfl.serializers
import sports.nhl.serializers
import sports.nba.serializers
import sports.mlb.serializers

import sports.nfl.models
import sports.nhl.models
import sports.nba.models
import sports.mlb.models

class AbstractGameManager(object):
    """
    Parent class with common behavior of GameManager classes.
    """

    class MethodNotImplementedException(Exception): pass

    def __init__(self, game_model):
        self.game_model = game_model

    def get_daily_games_gte(self, start):
        """
        get games relevant to daily fantasy contests
        at or after the start.time() on the start.date()
        """
        raise self.MethodNotImplementedException('method ' + self.get_daily_games_gte.__name__ + '()')

class NhlGameManager(AbstractGameManager):
    """
    NHL games database wrapper
    """
    def __init__(self):
        super().__init__(sports.nhl.models.Game)

    def get_daily_games_gte(self, start):
        """
        get the relevant games for daily fantasy on the start.date() on or after start.time()
        """
        pass # TODO

class NflGameManager(AbstractGameManager):
    """
    NFL games database wrapper
    """
    def __init__(self):
        super().__init__(sports.nfl.models.Game)

class NbaGameManager(AbstractGameManager): pass # TODO - implement

class MlbGameManager(AbstractGameManager): pass # TODO - implement

class SiteSportManager(object):
    """
    SiteSportManager helps get the model classes related to a sport.

    SiteSportManager.SPORTS is used in a migration file to
    automatically create the initial SiteSport entries in the database.
    Modify it at your own risk.
    """

    #
    # there should exist a single sports.models.SiteSport for these strings!
    SPORTS = [
        'nfl',
        'mlb',
        'nba',
        'nhl'
    ]

    def __init__(self):
        super().__init__()
        self.sports = []

    @staticmethod
    def get_site_sport(sport):
        """
        :param sport: the string name of the sport, must be in SiteSportManager.SPORTS.
        :return:
        """
        return SiteSport.objects.get(name=sport)

    @staticmethod
    def get_sport_names():
        """
        :return: a list of the string names of the sports predefined in this object.
        """
        return list(SiteSportManager.SPORTS)

    def __get_site_sport_from_str(self, sport):
        """
        :param sport: a string like 'nfl' or 'mlb'
        :return: the corresponding SiteSport instance if it exists,
            otherwise returns the value passed into method
        """
        if isinstance( sport, str ):
            try:
                return SiteSport.objects.get(name=sport)
            except SiteSport.DoesNotExist:
                raise SiteSportWithNameDoesNotExistException(type(self).__name__, sport)

        # default: return parameter passed into this method
        return sport

    def __check_sport(self, sport):
        """
        Validates the sport exists

        :param sport: the string representation of a specified sport

        :raises :class:`sports.exceptions.SportNameException`: when the string sport
            does not match a sport in the sports array
        """
        #
        # Makes sure the player_stats_object is an instance
        # of the subclass PlayerStats
        if not isinstance(sport, SiteSport):
            raise IncorrectVariableTypeException(type(self).__name__,
                                                 type(sport).__name__)

    def __get_array_of_classes(self, sport, filter_string, parent_class):
        content_types = ContentType.objects.filter(app_label=sport.name,
                                             model__icontains=filter_string)
        #
        # Iterates through all of the content_types that contain the filter
        # string and adds them to the matching_arr array if they are a
        # subclass of the parent_class argument
        matching_arr = []
        for content_type in content_types:
            content_class = content_type.model_class()
            if issubclass(content_class, parent_class):
                #print( content_class )
                matching_arr.append(content_class)

        return matching_arr

    #########
    #########   this method returns a list()
    #########
    def get_player_stats_class(self, sport):
        """
        Class that fetches the class or classes required for the specified
        sports player_stats_class

        :param sport: SiteSport used

        :return: an array of classes (models) that represent the sports
            :class:`sports.models.PlayerStats` class.

        :raises :class:`sports.exceptions.SportNameException`: when the string sport
            does not match a sport in the sports array
        """
        self.__check_sport(sport)
        return self.__get_array_of_classes(sport, 'playerstats', PlayerStats)

    def get_player_class(self, sport):
        """
        Class that fetches the class or classes required for the specified
        sports player_class

        :param sport: SiteSport used

        :return: an array of classes (models) that represent the sports
            :class:`sports.models.PlayerStats` class.

        :raises :class:`sports.exceptions.SportNameException`: when the string sport
            does not match a sport in the sports array
        """
        self.__check_sport(sport)
        arr = self.__get_array_of_classes(sport, 'player', Player)
        return arr[0]

    def get_player_classes(self):
        """
        Class that fetches an array of Classes that represent all instances of
            :class:`sports.models.Player` class.

        :return: an array of Classes that represent all instances of
            :class:`sports.models.Player` class.
        """
        content_types = ContentType.objects.filter(model__icontains='player')
        matching_arr = []
        for content_type in content_types:
            content_class = content_type.model_class()
            if content_class is None:
                continue
            #print( content_class )
            if issubclass(content_class, Player):
                matching_arr.append(content_class)

        return matching_arr

    def get_game_class(self, sport):
        """
        Class that fetches the class that inherits sports.models.Game for the sport

        :param sport: string OR SiteSport. method is intelligent about the runtime type of 'sport'

        :return: the sport's
            :class:`sports.models.Game` class.

        :raises :class:`sports.exceptions.SportNameException`: when the string sport
            does not match a sport in the sports array
        """
        sport = self.__get_site_sport_from_str(sport)
        self.__check_sport(sport)
        arr = self.__get_array_of_classes(sport, 'game', Game)
        if len(arr) >= 1:
            return arr[0]

        # by default raise an exception if we couldnt return a game class
        raise GameClassNotFoundException(type(self).__name__, sport)

    def get_team_class(self, sport):
        """
        Class that fetches the Team that inherits sports.models.Team for the sport

        :param sport: string OR SiteSport. method is intelligent about the runtime type of 'sport'

        :return: the sport's
            :class:`sports.models.Team` class.

        :raises :class:`sports.exceptions.SportNameException`: when the string sport
            does not match a sport in the sports array
        """
        sport = self.__get_site_sport_from_str(sport)
        self.__check_sport(sport)
        arr = self.__get_array_of_classes(sport, 'team', Team)
        if len(arr) >= 1:
            return arr[0]

        # by default raise an exception if we couldnt return a game class
        raise TeamClassNotFoundException(type(self).__name__, sport)

    def get_pbp_description_class(self, sport):
        """
        Class that fetches the class that inherits sports.models.Game for the sport

        :param sport: string OR SiteSport. method is intelligent about the runtime type of 'sport'

        :return: the sport's
            :class:`sports.models.Game` class.

        :raises :class:`sports.exceptions.SportNameException`: when the string sport
            does not match a sport in the sports array
        """
        sport = self.__get_site_sport_from_str(sport)
        self.__check_sport(sport)
        arr = self.__get_array_of_classes(sport, 'pbpdescription', PbpDescription)
        if len(arr) >= 1:
            return arr[0]

        # by default raise an exception if we couldnt return a game class
        raise PbpDescriptionClassNotFoundException(type(self).__name__, sport)

    def get_game_boxscore_class(self, sport):
        """
        Class that fetches the class that inherits sports.models.Game for the sport

        :param sport: string OR SiteSport. method is intelligent about the runtime type of 'sport'

        :return: the sport's
            :class:`sports.models.Game` class.

        :raises :class:`sports.exceptions.SportNameException`: when the string sport
            does not match a sport in the sports array
        """
        sport = self.__get_site_sport_from_str(sport)
        self.__check_sport(sport)
        arr = self.__get_array_of_classes(sport, 'gameboxscore', GameBoxscore)
        if len(arr) >= 1:
            return arr[0]

        # by default raise an exception if we couldnt return a game class
        raise GameBoxscoreClassNotFoundException(type(self).__name__, sport)

    def get_injury_class(self, sport):
        """
        Class that fetches the class that inherits sports.models.Injury for the sport

        :param sport: string OR SiteSport. method is intelligent about the runtime type of 'sport'

        :return: the sport's
            :class:`sports.models.Injury` class.

        :raises :class:`sports.exceptions.SportNameException`: when the string sport
            does not match a sport in the sports array
        """
        sport = self.__get_site_sport_from_str(sport)
        self.__check_sport(sport)
        arr = self.__get_array_of_classes(sport, 'injury', Injury)
        if len(arr) >= 1:
            return arr[0]

        # by default raise an exception if we couldnt return a game class
        raise InjuryClassNotFoundException(type(self).__name__, sport)

    def get_game_serializer_class(self, sport):
        """
        get the sport specific serializer for the 'sport' param

        :param sport:
        :return:
        """
        sport = self.__get_site_sport_from_str(sport)
        self.__check_sport(sport)
        try:
            return eval( 'sports.%s.serializers.GameSerializer' % sport.name)
        except:
            #
            raise GameSerializerClassNotFoundException(type(self).__name__, sport)

    def get_boxscore_serializer_class(self, sport):
        """
        get the sport specific serializers for the 'sport' param

        :param sport:
        :return:
        """
        sport = self.__get_site_sport_from_str(sport)
        self.__check_sport(sport)

        try:
            return eval( 'sports.%s.serializers.BoxscoreSerializer' % sport.name)
        except:
            # by default raise an exception if we couldnt return a game class
            raise BoxscoreSerializerClassNotFoundException(type(self).__name__, sport)

    def get_team_serializer_class(self, sport):
        """
        get the sport specific serializer for the sports.<sport>.Team model

        :param sport:
        :return:
        """
        sport = self.__get_site_sport_from_str(sport)
        self.__check_sport(sport)

        try:
            return eval( 'sports.%s.serializers.TeamSerializer' % sport.name)
        except:
            # by default raise an exception if we couldnt return a game class
            raise TeamSerializerClassNotFoundException(type(self).__name__, sport)

    def get_player_serializer_class(self, sport):
        """
        get the sport specific serializer for the sports.<sport>.Team model

        :param sport:
        :return:
        """
        sport = self.__get_site_sport_from_str(sport)
        self.__check_sport(sport)

        try:
            return eval( 'sports.%s.serializers.PlayerSerializer' % sport.name)
        except:
            # by default raise an exception if we couldnt return a game class
            raise PlayerSerializerClassNotFoundException(type(self).__name__, sport)

    def get_injury_serializer_class(self, sport):
        """

        :param sport:
        :return:
        """
        sport = self.__get_site_sport_from_str(sport)
        self.__check_sport(sport)

        try:
            return eval( 'sports.%s.serializers.InjurySerializer' % sport.name)

        except:


            # by default raise an exception if we couldnt return a game class
            raise InjurySerializerClassNotFoundException(type(self).__name__, sport)

    def get_fantasypoints_serializer_class(self, sport):
        """
        """
        sport = self.__get_site_sport_from_str(sport)
        self.__check_sport(sport)

        try:
            return eval( 'sports.%s.serializers.FantasyPointsSerializer' % sport.name)
        except:
            # by default raise an exception if we couldnt return a game class
            raise InjurySerializerClassNotFoundException(type(self).__name__, sport)

    def get_playerhistory_serializer_class(self, sport):
        """
        """
        sport = self.__get_site_sport_from_str(sport)
        self.__check_sport(sport)

        try:
            return eval( 'sports.%s.serializers.PlayerHistorySerializer' % sport.name)
        except:
            #
            raise PlayerHistorySerializerClassNotFoundException(type(self).__name__, sport)

    def __get_tsx_model_class(self, sport, model_name, model_parent_class):
        """
        helper function to combine a bunch of common functionality
        for getting & validating the site_sport, as well as
        returning the model class for the specified model_name who
        is a child of model_parent_class.

        :param sport: examples: 'nba', 'nfl'
        :param model_name: example: 'tsxcontent'
        :param model_parent_class: ex: sports.sport.TsxContent
        :return:
        """
        sport = self.__get_site_sport_from_str(sport)
        self.__check_sport(sport)
        arr = self.__get_array_of_classes(sport, model_name, model_parent_class)
        if len(arr) >= 1:
            return arr[0]

        # couldnt find one? raise a relevant exception
        msg_fmt = 'No sports.%s.models modelclass found named [%s] with parent [%s]'
        msg = msg_fmt % (sport, model_name, str(model_parent_class))
        raise TsxModelClassNotFoundException(msg)

    def get_tsxnews_class(self, sport):
        """

        :param sport: the string name of the sport, examples: 'nba', 'nfl'
        :return: the TsxNews model class for this sport
        """
        return self.__get_tsx_model_class(sport, 'tsxnews', TsxNews)

    def get_tsxnews_serializer_class(self, sport):
        sport = self.__get_site_sport_from_str(sport)
        self.__check_sport(sport)

        try:
            return eval( 'sports.%s.serializers.TsxNewsSerializer' % sport.name)
        except:
            # raise generic TsxSerializer exception
            raise TsxSerializerClassNotFoundException(type(self).__name__, sport)

    def get_tsxplayer_serializer_class(self, sport):
        sport = self.__get_site_sport_from_str(sport)
        self.__check_sport(sport)

        try:
            return eval( 'sports.%s.serializers.TsxPlayerSerializer' % sport.name)
        except:
            # raise generic TsxSerializer exception
            raise TsxSerializerClassNotFoundException(type(self).__name__, sport)

    def get_tsxinjury_class(self, sport):
        """

        :param sport: the string name of the sport, examples: 'nba', 'nfl'
        :return: the TsxInjury model class for this sport
        """
        return self.__get_tsx_model_class(sport, 'tsxinjury', TsxInjury)

    def get_tsxtransaction_class(self, sport):
        """

        :param sport: the string name of the sport, examples: 'nba', 'nfl'
        :return: the TsxTransaction model class for this sport
        """
        return self.__get_tsx_model_class(sport, 'tsxtransaction', TsxTransaction)

    def get_tsxteam_class(self, sport):
        """

        :param sport: the string name of the sport, examples: 'nba', 'nfl'
        :return: the TsxTeam model class for this sport
        """
        return self.__get_tsx_model_class(sport, 'tsxteam', TsxTeam)

    def get_tsxplayer_class(self, sport):
        """

        :param sport: the string name of the sport, examples: 'nba', 'nfl'
        :return: the TsxPlayer model class for this sport
        """
        return self.__get_tsx_model_class(sport, 'tsxplayer', TsxPlayer)

class PlayerNamesCsv(object):

    def __init__(self, sport='nfl', positions=None, filename=None):

        self.sports = ['nfl','nba','mlb','nhl']     # dataden four major sports

        self.site_sport = self.__validate_site_sport(sport)

        self.positions = positions

        if filename:
            self.filename = filename
        else:
            self.filename = '%s_playernames_%s.csv' % (sport, '_'.join( self.positions ))

        self.f                  = None                      # dont create the file yet
        self.dataden            = dataden.classes.DataDen() # access dataden/mongo player data

        self.player_collection  = 'player'
        self.parent_api         = 'rosters'         # for nfl. other classes may override this

        self.key_fullname       = 'name_full'       # for nfl. other classes may override this
        self.key_position       = 'position'        # for nfl. other classes may override this

    def __validate_site_sport(self, sport):
        if isinstance(sport, str):          # sport is a string
            if sport not in self.sports:
                raise Exception('sport [%s] is not a valid sport in %s' % (sport, self.sports))
            return SiteSport.objects.get(name=sport)

        elif isinstance(sport, SiteSport):  # sport is an instance of sports.models.SiteSport
            return sport
        else:
            raise Exception('sport needs to be a string in %s, or an instance of SiteSport' % str(self.sports))

    def get_players(self):
        """
        get the cursor of players from dataden from their respective sport
        """
        if self.positions is None:
            raise Exception('self.positions is None (ie: you need to set it to a list of the string positions ie: ["QB","RB"]')
        target = {self.key_position : {'$in':self.positions}}
        return self.dataden.find(self.site_sport.name, self.player_collection, self.parent_api, target)

    def get_row_str(self, p):
        return '%s, %s, "%s", %s,\n' % (self.site_sport.name,
                    p.get('id'), p.get(self.key_fullname), p.get(self.key_position))
    def generate(self):
        """
        generate the csv file with the params this object was constructed with
        """
        self.f = open(self.filename,'w') # open the file with the filename and overwrite it
        players = self.get_players()
        print(players.count(), 'players')
        for p in players:
            # self.f.write('%s, %s, "%s", %s,\n' % (self.site_sport.name,
            #         p.get('id'),p.get(self.key_fullname),p.get(self.key_position)))
            self.f.write( self.get_row_str( p ) )
        self.f.close()
        print('...generated file: ', self.filename)

    def get_rows(self):
        rows = []
        for p in self.get_players():
            rows.append( self.get_row_str( p ) )
        return rows

class NflPlayerNamesCsv(PlayerNamesCsv):
    """
    get a csv list of the nfl players names
    """
    DEFAULT_SPORT       = 'nfl'
    DEFAULT_POSITIONS   = ['QB','RB','FB','WR','TE']

    def __init__(self, sport=DEFAULT_SPORT, positions=DEFAULT_POSITIONS):
        super().__init__(sport, positions)

class NhlPlayerNamesCsv(PlayerNamesCsv):
    """
    get a csv list of the nfl players names
    """
    DEFAULT_SPORT       = 'nhl'
    DEFAULT_POSITIONS   = ['G','LW','RW','C','D']

    def __init__(self, sport=DEFAULT_SPORT, positions=DEFAULT_POSITIONS):
        super().__init__(sport, positions)

        # override
        self.key_fullname   = 'full_name'
        self.key_position   = 'primary_position'

class NbaPlayerNamesCsv(PlayerNamesCsv):
    """
    get a csv list of the nfl players names
    """
    DEFAULT_SPORT       = 'nba'
    DEFAULT_POSITIONS   = ['PG','SG','PF','SF','C']

    def __init__(self, sport=DEFAULT_SPORT, positions=DEFAULT_POSITIONS):
        super().__init__(sport, positions)

        # override
        self.key_fullname   = 'full_name'
        self.key_position   = 'primary_position'

class MlbPlayerNamesCsv(PlayerNamesCsv):
    """
    get a csv list of the nfl players names
    """
    DEFAULT_SPORT       = 'mlb'
    DEFAULT_POSITIONS   = ['P','C','1B','2B','SS','3B','LF','CF','RF','DH']

    def __init__(self, sport=DEFAULT_SPORT, positions=DEFAULT_POSITIONS):
        super().__init__(sport, positions)

        # override
        self.parent_api     = 'rostersfull'
        self.key_fullname   = 'full_name'
        self.key_position   = 'primary_position'

