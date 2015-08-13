#
# roster/classes.py

from collections import OrderedDict
from .models import RosterSpot, RosterSpotPosition
from mysite.classes import AbstractManagerClass
from sports.models import SiteSport, Player, Position

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
            if player.position == position.position:
                return True
        return False

    def get_roster_spots_count(self):
        return len(self.roster_spot_arr)

    def get_roster_spot_for_index(self, index):
        return self.roster_spot_arr[index][0].roster_spot

class Initial(object):
    """
    has methods to create the default underlying rosters of the site.

    methods setup_all() & setup() have no effect if
    rosters for the sport exist.
    """

    DEFAULT_ROSTER_MAP_NFL = {
        ('QB',1,0,True)     :['QB'],
        ('RB',2,1,True)     :['RB','FB'],
        ('WR',2,3,True)     :['WR'],
        ('TE',1,5,True)     :['TE'],
        ('FLEX',2,6,False)  :['RB','FB','WR','TE'],
        ('DST',1,8,True)    :['DST']
    }

    ROSTERS = {
        'nfl' : DEFAULT_ROSTER_MAP_NFL,
        # 'nhl' : DEFAULT_ROSTER_MAP_NHL, # TODO
        #  ... TODO add mlb and nba
    }

    def __init__(self):
        site_sports = SiteSport.objects.all()
        if len(site_sports) <= 0:
            raise Exception('there are no SiteSport objects in the database!')
        self.sports = [x.name for x in site_sports] # get list of string names

    def setup_all(self):
        for sport in self.sports:
            self.setup( sport )

    def setup(self, sport):
        roster_map = self.ROSTERS.get(sport, None)
        if roster_map is None:
            raise Exception('the default roster map for [%s] does not exist. add it in roster.classes.Initial class!')

        # order the incoming roster dict by the idx
        ordered_roster = OrderedDict(sorted(roster_map.items(), key=lambda k: k[0][2]))

        site_sport, created = SiteSport.objects.get_or_create(name=sport)
        print(site_sport)

        # create the roster spot mappings
        for rs_tuple, pos_names_list in ordered_roster.items():
            roster_spot_name    = rs_tuple[0]
            roster_spot_amount  = rs_tuple[1]
            roster_spot_idx     = rs_tuple[2]
            primary             = rs_tuple[3]
            # print('roster spot: %s, amount:%s, idx:%s, is_primary:%s' % (roster_spot_name,
            #                                 roster_spot_amount, roster_spot_idx, primary))
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
                #ret_roster_spot_position_list.append(roster_spot_position)
                print('    ', roster_spot_position)
        print('...created!')
        #return ret_roster_spot_position_list