from .models import RosterSpot, RosterSpotPosition
from mysite.classes import AbstractManagerClass
from sports.models import SiteSport, Player

class RosterManager(AbstractManagerClass):
    def __init__(self, site_sport):
        self.validate_variable(SiteSport, site_sport)
        self.site_sport = site_sport

        self.roster_spot_arr = []
        rosterspots = RosterSpot.objects.filter(site_sport=site_sport)
        for roster_spot in rosterspots:
            spots = list(RosterSpotPosition.objects.filter(roster_spot=roster_spot))
            for i in range(0, roster_spot.amount):
                self.roster_spot_arr.append(spots)


    def player_matches_spot(self, player, spot_index):
        """
        Method to verify the player can be drafted for the Roster Spot Index
        :param player: The :class:`sports.models.Player` to be drafted into
            the spot_index
        :param spot_index: The roster spot index
        :return: True if the player matches and False if not
        """
        self.validate_variable(Player, player)

        #
        # Gets the position array for the spot index and looks for a match
        position_arr = self.roster_spot_arr[spot_index]

        for position in position_arr:
            print("position_class "+str(position.position.site_sport.name)+ " "+str(player.position.site_sport.name))
            if player.position == position.position:
                return True
        return False

    def get_roster_spots_count(self):
        return len(self.roster_spot_arr)

    def get_roster_spot_for_index(self, index):
        return self.roster_spot_arr[index][0].roster_spot