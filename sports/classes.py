from logging import getLogger

from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache

import dataden.classes
import dataden.classes
import scoring.classes
import sports.mlb.models
import sports.mlb.serializers
import sports.nba.models
import sports.nba.serializers
import sports.nfl.models
import sports.nfl.serializers
import sports.nhl.models
import sports.nhl.serializers
from mysite.exceptions import IncorrectVariableTypeException
from util.dfsdate import DfsDate
from .exceptions import (
    GameBoxscoreClassNotFoundException,
    SiteSportWithNameDoesNotExistException,
    SeasonClassNotFoundException,
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
    PlayerNewsSerializerClassNotFoundException,
)
from .models import (
    SiteSport,
    PlayerStats,
    Player,
    Season,
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

logger = getLogger('sports.classes')


class AbstractGameManager(object):
    """
    Parent class with common behavior of GameManager classes.
    """

    class MethodNotImplementedException(Exception):
        pass

    def __init__(self, game_model):
        self.game_model = game_model

    def get_daily_games_gte(self, start):
        """
        get games relevant to daily fantasy contests
        at or after the start.time() on the start.date()
        """
        raise self.MethodNotImplementedException(
            'method ' + self.get_daily_games_gte.__name__ + '()')


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
        pass  # TODO


class NflGameManager(AbstractGameManager):
    """
    NFL games database wrapper
    """

    def __init__(self):
        super().__init__(sports.nfl.models.Game)


class NbaGameManager(AbstractGameManager):
    pass  # TODO - implement


class MlbGameManager(AbstractGameManager):
    pass  # TODO - implement


class SiteSportManager(object):
    """
    SiteSportManager helps get the model classes related to a sport.

    SiteSportManager.SPORTS is used in a migration file to
    automatically create the initial SiteSport entries in the database.
    Modify it at your own risk.
    """

    #
    # there should exist a single sports.models.SiteSport for these strings!
    NFL = 'nfl'
    MLB = 'mlb'
    NBA = 'nba'
    NHL = 'nhl'

    SPORTS = [
        NFL,
        MLB,
        NBA,
        NHL,
    ]

    def __init__(self):
        super().__init__()
        self.sports = []

    @staticmethod
    def buildSpecialAliasMetaClass(class_string, class_name, prefix):
        '''
        Builds a Dynamic Class for Aliasing any Class to work with Swagger
        :param class_string:
        :param class_name:
        :param prefix:
        :return:
        '''
        newClassName = "{0}{1}".format(prefix.upper(), class_name)
        my_class = eval(class_string)
        return type(newClassName, (my_class,), {})

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
        if isinstance(sport, str):
            try:
                return SiteSport.objects.get(name=sport)
            except SiteSport.DoesNotExist:
                raise SiteSportWithNameDoesNotExistException(
                    type(self).__name__, sport)

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

    def get_score_system_class(self, sport):
        """
        get the scoring.classes "score system" class for the sport (ie: the scoring metrics)

        :param sport: can be the string name ('nfl', etc... ) or the SiteSport for the sport.
        :return: scoring.classes.<Sport>SalaryScoreSystem class
        """
        site_sport = self.__get_site_sport_from_str(sport)
        self.__check_sport(site_sport)

        if site_sport.name == self.NFL:
            return scoring.classes.NflSalaryScoreSystem
        elif site_sport.name == self.NBA:
            return scoring.classes.NbaSalaryScoreSystem
        elif site_sport.name == self.MLB:
            return scoring.classes.MlbSalaryScoreSystem
        elif site_sport.name == self.NHL:
            return scoring.classes.NhlSalaryScoreSystem

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
                # print( content_class )
                matching_arr.append(content_class)

        return matching_arr

    #########
    # this method returns a list()
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

    def get_player_stats_classes(self, sport):
        """
        wrapper for calling the ill-named self.get_player_stats_class(sport) which returns a list
        """
        return self.get_player_stats_class(sport)

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
            # print( content_class )
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
        arr = self.__get_array_of_classes(
            sport, 'pbpdescription', PbpDescription)
        if len(arr) >= 1:
            return arr[0]

        # by default raise an exception if we couldnt return a game class
        raise PbpDescriptionClassNotFoundException(type(self).__name__, sport)

    def get_scoreboard_games(self, sport):
        """
        get the current daily games (or current/upcoming weekly games for nfl)

        :param sport:
        :return:
        """
        site_sport = self.__get_site_sport_from_str(sport)
        game_class = self.get_game_class(site_sport)
        # get the date_range tuple so we can filter the games !
        if sport == 'nfl':
            dt_range = DfsDate.get_current_nfl_date_range(offset_hours=6)
        else:
            # offset_hours = 6 shifts the 24 window into the next day
            # so that we get all the games
            dt_range = DfsDate.get_current_dfs_date_range(offset_hours=6)

        # games = game_class.objects.filter( start__range=dt_range )
        start = dt_range[0]
        end = dt_range[1]
        # print('get_scoreboard_games:', 'start[%s]'%str(start), start,
        # 'end[%s]'%str(end), end, str(dt_range))
        games = game_class.objects.filter(start__gt=start,
                                          start__lte=end)
        # tab_width = '    '
        # for g in games:
        #     print(tab_width, g.srid, str(g.start))
        return games

    def __add_to_dict(self, target, extras, exclude_fields=[]):
        for k, v in extras.items():
            if k in exclude_fields:
                continue  # dont add this one
            target[k] = v
        return target

    def get_serialized_scoreboard_data(self, sport):
        # boxscore_exclude_fields = ['status']

        site_sport = self.__get_site_sport_from_str(sport)
        boxscore_class = self.get_game_boxscore_class(site_sport)
        # boxscore_serializer_class = self.get_boxscore_serializer_class(sport)
        game_serializer_class = self.get_game_serializer_class(sport)
        games = self.get_scoreboard_games(sport)
        game_srids = [g.srid for g in games]
        boxscores = boxscore_class.objects.filter(srid_game__in=game_srids)

        data = {}
        for game in games:
            # initial inner_data
            inner_data = {}

            # add the game data
            g = game_serializer_class(game).data

            logger.debug(g)
            self.__add_to_dict(inner_data, g)

            # add the home/away scores to the inner data
            inner_data['home_score'] = None  # default
            inner_data['away_score'] = None  # default
            try:
                boxscore = boxscores.get(srid_game=game.srid)
                inner_data['home_score'] = boxscore.home_score
                inner_data['away_score'] = boxscore.away_score
            except:
                pass

            # finish it by adding the game data to the return data dict
            data[game.srid] = inner_data

        # return the json data
        return data

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

    def get_season_class(self, sport):
        """
        get the sports.<sport>.models.Season class for the sport

        :param sport:
        :return:
        """
        sport = self.__get_site_sport_from_str(sport)
        self.__check_sport(sport)
        arr = self.__get_array_of_classes(sport, 'season', Season)
        if len(arr) >= 1:
            return arr[0]

        # by default raise an exception if we couldnt return a game class
        raise SeasonClassNotFoundException(type(self).__name__, sport)

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
            class_string = 'sports.%s.serializers.GameSerializer' % sport.name
            return SiteSportManager.buildSpecialAliasMetaClass(class_string, "GameSerializer",
                                                               sport.name)
        except:
            #
            raise GameSerializerClassNotFoundException(
                type(self).__name__, sport)

    def get_boxscore_serializer_class(self, sport):
        """
        get the sport specific serializers for the 'sport' param

        :param sport:
        :return:
        """
        sport = self.__get_site_sport_from_str(sport)
        self.__check_sport(sport)

        try:
            class_string = 'sports.%s.serializers.BoxscoreSerializer' % sport.name
            return SiteSportManager.buildSpecialAliasMetaClass(class_string, "BoxscoreSerializer",
                                                               sport.name)
        except:
            # by default raise an exception if we couldnt return a game class
            raise BoxscoreSerializerClassNotFoundException(
                type(self).__name__, sport)

    def get_team_serializer_class(self, sport):
        """
        get the sport specific serializer for the sports.<sport>.Team model

        :param sport:
        :return:
        """
        sport = self.__get_site_sport_from_str(sport)
        self.__check_sport(sport)

        try:
            class_string = 'sports.%s.serializers.TeamSerializer' % sport.name
            return SiteSportManager.buildSpecialAliasMetaClass(class_string, "TeamSerializer",
                                                               sport.name)
        except:
            # by default raise an exception if we couldnt return a game class
            raise TeamSerializerClassNotFoundException(
                type(self).__name__, sport)

    def get_player_serializer_class(self, sport):
        """
        get the sport specific serializer for the sports.<sport>.Team model

        :param sport:
        :return:
        """
        sport = self.__get_site_sport_from_str(sport)
        self.__check_sport(sport)

        try:
            class_string = 'sports.%s.serializers.PlayerSerializer' % sport.name
            return SiteSportManager.buildSpecialAliasMetaClass(class_string, "PlayerSerializer",
                                                               sport.name)
        except:
            # by default raise an exception if we couldnt return a game class
            raise PlayerSerializerClassNotFoundException(
                type(self).__name__, sport)

    def get_injury_serializer_class(self, sport):
        """

        :param sport:
        :return:
        """
        sport = self.__get_site_sport_from_str(sport)
        self.__check_sport(sport)

        try:
            class_string = 'sports.%s.serializers.InjurySerializer' % sport.name
            return SiteSportManager.buildSpecialAliasMetaClass(class_string, "InjurySerializer",
                                                               sport.name)
        except:

            # by default raise an exception if we couldnt return a game class
            raise InjurySerializerClassNotFoundException(
                type(self).__name__, sport)

    def get_fantasypoints_serializer_class(self, sport):
        """
        """
        sport = self.__get_site_sport_from_str(sport)
        self.__check_sport(sport)

        try:
            class_string = 'sports.%s.serializers.FantasyPointsSerializer' % sport.name
            return SiteSportManager.buildSpecialAliasMetaClass(class_string,
                                                               "FantasyPointsSerializer",
                                                               sport.name)
        except:
            # by default raise an exception if we couldnt return a game class
            raise InjurySerializerClassNotFoundException(
                type(self).__name__, sport)

    def get_playerhistory_serializer_class(self, sport):
        """
        """
        sport = self.__get_site_sport_from_str(sport)
        self.__check_sport(sport)

        try:
            class_string = 'sports.%s.serializers.PlayerHistorySerializer' % sport.name
            return SiteSportManager.buildSpecialAliasMetaClass(class_string,
                                                               "PlayerHistorySerializer",
                                                               sport.name)
        except:
            #
            raise PlayerHistorySerializerClassNotFoundException(
                type(self).__name__, sport)

    def get_playernews_serializer_class(self, sport):
        """
        :param sport: either the string name, or the SiteSport instance for the actual sport
        :return: the sports.<sport>.serializers.PlayerNewsSerializer class for the sport
        """
        sport = self.__get_site_sport_from_str(sport)
        self.__check_sport(sport)

        try:
            class_string = 'sports.%s.serializers.PlayerNewsSerializer' % sport.name
            return SiteSportManager.buildSpecialAliasMetaClass(class_string, "PlayerNewsSerializer",
                                                               sport.name)
        except:
            #
            raise PlayerNewsSerializerClassNotFoundException(
                type(self).__name__, sport)

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
        arr = self.__get_array_of_classes(
            sport, model_name, model_parent_class)
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
            class_string = 'sports.%s.serializers.TsxNewsSerializer' % sport.name
            return SiteSportManager.buildSpecialAliasMetaClass(class_string, "TsxNewsSerializer",
                                                               sport.name)
        except:
            # raise generic TsxSerializer exception
            raise TsxSerializerClassNotFoundException(
                type(self).__name__, sport)

    def get_tsxplayer_serializer_class(self, sport):
        sport = self.__get_site_sport_from_str(sport)
        self.__check_sport(sport)

        try:
            class_string = 'sports.%s.serializers.TsxPlayerSerializer' % sport.name
            return SiteSportManager.buildSpecialAliasMetaClass(class_string, "TsxPlayerSerializer",
                                                               sport.name)
        except:
            # raise generic TsxSerializer exception
            raise TsxSerializerClassNotFoundException(
                type(self).__name__, sport)

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

        # dataden four major sports
        self.sports = ['nfl', 'nba', 'mlb', 'nhl']

        self.site_sport = self.__validate_site_sport(sport)

        self.positions = positions

        if filename:
            self.filename = filename
        else:
            self.filename = '%s_playernames_%s.csv' % (
                sport, '_'.join(self.positions))

        self.f = None  # dont create the file yet
        # access dataden/mongo player data
        self.dataden = dataden.classes.DataDen()

        self.player_collection = 'player'
        # for nfl. other classes may override this
        self.parent_api = 'rosters'

        # for nfl. other classes may override this
        self.key_fullname = 'name_full'
        # for nfl. other classes may override this
        self.key_position = 'position'

    def __validate_site_sport(self, sport):
        if isinstance(sport, str):  # sport is a string
            if sport not in self.sports:
                raise Exception(
                    'sport [%s] is not a valid sport in %s' % (sport, self.sports))
            return SiteSport.objects.get(name=sport)

        # sport is an instance of sports.models.SiteSport
        elif isinstance(sport, SiteSport):
            return sport
        else:
            raise Exception(
                'sport needs to be a string in %s, or an instance of SiteSport' % str(self.sports))

    def get_players(self):
        """
        get the cursor of players from dataden from their respective sport
        """
        if self.positions is None:
            raise Exception(
                ('self.positions is None (ie: you need to set it to a list of the string positions '
                 'ie: ["QB","RB"]'))
        target = {self.key_position: {'$in': self.positions}}
        return self.dataden.find(self.site_sport.name, self.player_collection, self.parent_api,
                                 target)

    def get_row_str(self, p):
        return '%s, %s, "%s", %s,\n' % (self.site_sport.name,
                                        p.get('id'), p.get(self.key_fullname),
                                        p.get(self.key_position))

    def generate(self):
        """
        generate the csv file with the params this object was constructed with
        """
        self.f = open(
            self.filename, 'w')  # open the file with the filename and overwrite it
        players = self.get_players()
        print(players.count(), 'players')
        for p in players:
            # self.f.write('%s, %s, "%s", %s,\n' % (self.site_sport.name,
            #         p.get('id'),p.get(self.key_fullname),p.get(self.key_position)))
            self.f.write(self.get_row_str(p))
        self.f.close()
        print('...generated file: ', self.filename)

    def get_rows(self):
        rows = []
        for p in self.get_players():
            rows.append(self.get_row_str(p))
        return rows


class NflPlayerNamesCsv(PlayerNamesCsv):
    """
    get a csv list of the nfl players names
    """
    DEFAULT_SPORT = 'nfl'
    DEFAULT_POSITIONS = ['QB', 'RB', 'FB', 'WR', 'TE']

    def __init__(self, sport=DEFAULT_SPORT, positions=DEFAULT_POSITIONS):
        super().__init__(sport, positions)


class NhlPlayerNamesCsv(PlayerNamesCsv):
    """
    get a csv list of the nfl players names
    """
    DEFAULT_SPORT = 'nhl'
    DEFAULT_POSITIONS = ['G', 'LW', 'RW', 'C', 'D']

    def __init__(self, sport=DEFAULT_SPORT, positions=DEFAULT_POSITIONS):
        super().__init__(sport, positions)

        # override
        self.key_fullname = 'full_name'
        self.key_position = 'primary_position'


class NbaPlayerNamesCsv(PlayerNamesCsv):
    """
    get a csv list of the nfl players names
    """
    DEFAULT_SPORT = 'nba'
    DEFAULT_POSITIONS = ['PG', 'SG', 'PF', 'SF', 'C']

    def __init__(self, sport=DEFAULT_SPORT, positions=DEFAULT_POSITIONS):
        super().__init__(sport, positions)

        # override
        self.key_fullname = 'full_name'
        self.key_position = 'primary_position'


class MlbPlayerNamesCsv(PlayerNamesCsv):
    """
    get a csv list of the nfl players names
    """
    DEFAULT_SPORT = 'mlb'
    DEFAULT_POSITIONS = [
        'P', 'C', '1B', '2B', 'SS', '3B', 'LF', 'CF', 'RF', 'DH']

    def __init__(self, sport=DEFAULT_SPORT, positions=DEFAULT_POSITIONS):
        super().__init__(sport, positions)

        # override
        self.parent_api = 'rostersfull'
        self.key_fullname = 'full_name'
        self.key_position = 'primary_position'


# class Fppg(object):
#
#     def __init__(self):
#         pass
#
#     def get_player_stats(self):
#         raise Exception('Fppg.get_player_stats() - must be overridden in inheriting class')
#
# class NbaFppg(dataden.classes.NbaSeasonGames):
#
#     def get_player_stats(self):
#         ssm = SiteSportManager()
#         site_sport = ssm.get_site_sport(self.sport) # self.sport is from inherited class
#         game_class = ssm.get_game_class(site_sport)
#         player_stats_class_list = ssm.get_player_stats_class(site_sport)
#         now = timezone.now()
#         game_ids = self.get_game_ids_regular_season()
#
#         games = game_class.objects.filter(srid__in=game_ids, start__lt=timezone.now())
#         history_game_ids = [ g.srid for g in games ]
#
#         for player_stats_class in player_stats_class_list:
#             player_stats = player_stats_class.objects.filter( srid_game__in=history_game_ids )
#             # these player stats objects should have scoreable data we can calculate FPPGs on
#
#             # get the unique players
#             distinct_players = player_stats.distinct('player_id')
#
#             # TODO - sum and average their fppgs
#             players_with_stats = 0
#             for player in distinct_players:
#                 #print('player id', str(player.pk))
#                 single_player_stats = player_stats.filter(player_id=player.pk)
#                 if single_player_stats.count() > 0:
#                     players_with_stats += 1
#                     print('player id', str(player.pk))
#                     print('    %s playerStats objects' % str(single_player_stats.count()))
#
#             print('')
#             print('%s players without PlayerStats' % (
#               str(distinct_players.count() - players_with_stats)))
#


# just need a method to get the sports games, and PlayerStats.objects.filter(
# start__lte=timezone.now() ).order_by('-start')
#
# then sub filter that list on datadens sport Season classes method
# which gets all the regular season ids.
#
# Voila: we have all the PlayerStats from the current season.
#
# we copuld do another sort on that subfilter .order_by('start')   # ascending!
# and get the first game.
#
# this way we could make a method to parse fppgs( start_dt, end_dt ) which is more
# generic and useful   OR MAY BE EXISTING IN THE SALARY STUFF RYAN WROTE BTW


class TeamNameCache(object):
    """
    This is a cache for all <sport>.Team models. It is an easy and quick way to get team info without
    having to hit the database.
    """
    cache_key = 'team_cache_v1'

    def __init__(self):
        # Fetch teams from the cache (if they exist)
        self.team_cache = cache.get(self.cache_key)

        # If the cache is not populated, fill it up with all teams from all sports!
        if self.team_cache is None:
            teams = {}
            # Get the names of sports we support.
            ssm = SiteSportManager()
            sports = ssm.get_sport_names()

            # Run through each sport and grab its teams.
            for sport in sports:
                sport_teams = ssm.get_team_class(sport).objects.values()
                logger.warning('caching %s %s teams' % (len(sport_teams), sport))
                for team in sport_teams:
                    teams[team['srid']] = team
                    # Add in sport field for easy filtering.
                    teams[team['srid']].update({'sport': sport})

            # Set the teams into the cache
            cache.set(self.cache_key, teams)
            logger.warning(
                'cached %s teams from %s sports into the team cache' % (len(teams), len(sports)))
            self.team_cache = teams

    def get_team_from_srid(self, srid):
        """
        Get a team entry from a team_srid
        Args:
            srid: <sport>.models.Team.team_srid
        """
        return self.team_cache[srid]

    @staticmethod
    def search(values, search_for):
        for k in values:
            for v in values[k]:
                if search_for in v:
                    return k
        return None
