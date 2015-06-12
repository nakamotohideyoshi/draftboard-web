from .models import SiteSport, PlayerStats, Player
from django.contrib.contenttypes.models import ContentType
from .exceptions import SportNameException
from mysite.exceptions import IncorrectVariableTypeException

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
        content_types = ct = ContentType.objects.filter(app_label=sport.name,
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
