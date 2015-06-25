from .models import SiteSport, PlayerStats, Player
from django.contrib.contenttypes.models import ContentType
from .exceptions import SportNameException
from mysite.exceptions import IncorrectVariableTypeException
import dataden.classes

class SiteSportManager(object):

    def __init__(self):
        self.sports = ['nfl','mlb','nba','nhl']



    def create_or_update_sports(self):
        #
        # updates the databases or creates the rows if they do
        # not exist for each sport
        for sport in self.sports:
            site_sport = None
            try:
                site_sport = SiteSport.objects.get(name = sport)
            except SiteSport.DoesNotExist:
                site_sport = SiteSport()



            #
            # updates the information for each row for the given sport
            for field in self.fields:
                ct = None
                try:
                    ct = ContentType.objects.get(app_label=sport,
                                             model=field)

                except ContentType.DoesNotExist:
                    # meaning the app did not implement this particular
                    # abstract class.
                    print("fail on: "+sport+" "+field)

                setattr(site_sport, field, ct)




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
                matching_arr.append(content_class)

        return matching_arr

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

class PlayerNamesCsv(object):

    def __init__(self, sport='nfl', positions=None, filename=None):

        self.sports     = ['nfl','nba','mlb','nhl']     # dataden four major sports

        if isinstance(sport, str):          # sport is a string
            if sport not in self.sports:
                raise Exception('sport [%s] is not a valid sport in %s' % (sport, str(self.sports)))
            self.site_sport = SiteSport.objects.get(name=sport)

        elif isinstance(sport, SiteSport):  # sport is an instance of sports.models.SiteSport
            self.site_sport = sport
        else:
            raise Exception('sport needs to be a string in %s, or an instance of SiteSport' % str(self.sports))

        if positions is None:
            raise Exception('self.positions is None - you must provide a list of the positions')

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

    def get_players(self):
        """
        get the cursor of players from dataden from their respective sport
        """
        if self.positions is None:
            raise Exception('self.positions is None (ie: you need to set it to a list of the string positions ie: ["QB","RB"]')
        target = {self.key_position : {'$in':self.positions}}
        return self.dataden.find(self.site_sport.name, self.player_collection, self.parent_api, target)

    def generate(self):
        """
        generate the csv file with the params this object was constructed with
        """
        self.f = open(self.filename,'w') # open the file with the filename and overwrite it
        players = self.get_players()
        print(players.count(), 'players')
        for p in players:
            self.f.write('%s, %s, "%s", %s,\n' % (self.site_sport.name,
                    p.get('id'),p.get(self.key_fullname),p.get(self.key_position)))
        self.f.close()
        print('...generated file: ', self.filename)

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