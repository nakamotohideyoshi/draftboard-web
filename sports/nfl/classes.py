from logging import getLogger

from dataden.classes import (
    RecentGamePlayerStats,
)
from sports.classes import (
    SiteSportManager,
)

logger = getLogger('sports.nfl.classes')


class MyPlayerStats:
    """
    this class can dynamically add the properties passed to it as a list.

    for this class to be able to properly copy its values into
    a sports.<sport>.models.PlayerStats instance, the fields need to
    be the same!
    """

    def __init__(self, fieldnames):
        # add all the fielnames with values that default to 0
        # For example, setattr(x, 'foobar', 123) is equivalent to x.foobar = 123.

        for fieldname in fieldnames:
            setattr(self, fieldname, 0)

    def __str__(self):
        return str(self.get_vars())

    def get_vars(self):
        # get all class variables names
        members = vars(self)  # get the dict of variable name to values
        return members


class NflRecentGamePlayerStats(RecentGamePlayerStats):
    """
    abstract parent for getting all player stats for
    specified games based on the most recently parsed data.
    """

    collection = 'player'  # the mongo collection name to query from.
    parent_api = 'stats'  # the dataden name of the raw stats feed where player game stats are found.
    game_id_field = 'game__id'  # the mongo object field name of the game srid.

    sport = 'nfl'  # draftboard sport name
    db = 'nflo'  # mongo db name

    def __init__(self):
        super().__init__(self.db)

    def get_player_stats_model_class(self):
        site_sport_manager = SiteSportManager()
        site_sport = site_sport_manager.get_site_sport(self.sport)
        player_stats_model_classes = site_sport_manager.get_player_stats_classes(site_sport)
        return player_stats_model_classes[0]  # return first element - nfl only has 1

    def get_my_player_stats_instance(self):
        """
        return fresh instance of MyPlayerStats with the custom properties
        """
        player_stats_model_class = self.get_player_stats_model_class()
        fieldnames = player_stats_model_class.SCORING_FIELDS
        # debug print the 'defaults' -- the zeroed out initial fields that represent the player stats
        mps = MyPlayerStats(fieldnames)
        # print('new MyPlayerStats() instance. (shows default fields):', str(mps)) # TODO remove debug
        return mps

    def update(self, game_srid):
        """
        update PlayerStats models for this sport using recent parse of the stats
        in order to clean up stat corrections, or changes in the raw data
        that could lead to "dangling" stats like the Joe Mixon / Andy Dalton issue from 2017 preseaon

        this method will potentially compete with the
        asynchornous, individual real-time triggered PlayerStats updates, but so
        long as you run it occasionally, and then before doing payouts it will
        clean up an issues caused by dangling stats
        """

        # build most up-to-date data using dataden's find_recent()
        player_stats_data = self.build_data(game_srid)

        # query django models for this sports PlayerStats models for this game
        player_stats_model_class = self.get_player_stats_model_class()
        player_stats_models = player_stats_model_class.objects.filter(srid_game=game_srid)

        # update any of them that have more recent changes
        for player_stats_model in player_stats_models:
            player_srid = player_stats_model.srid_player

            my_player_stats = player_stats_data.get(player_srid, None)
            if my_player_stats is not None:
                # save() model to django backend if there are any changes
                self.update_player_stats_model(my_player_stats, player_stats_model)

        logger.info('Player stat correction sync complete for game: %s', game_srid)

    def build_data(self, game_srid):
        """
        build a dictionary of player stats objects which very closely resemble
        the sports.<sport>.models.PlayerStats objects from the most recent parse of the stats feed.

        :param game_srid:
        :return: a dictionary of player stats objects built from the most recent parse of the feed
        """

        player_stats_dict = {}  # we will add player_stats_data dicts to this object using the players srid as the key

        mongo_objects = self.get_player_stats_for(game_srid)
        logger.info('%s player stats found in the MongoDB for game %s' % (
            mongo_objects.count(), game_srid))

        # iterate all the objects and compile all the stats for each player
        for o in mongo_objects:
            # print(str(o)) # debug print if you want to see each mongo object

            player_srid = o.get('id')
            player_stats = player_stats_dict.get(player_srid)
            if player_stats is None:
                # create it if it doesnt exist
                player_stats = self.get_my_player_stats_instance()

                # player_name = ''
                # try:
                #     # its not required to get, but helps when/if debug printing
                #     player_name = o.get('name', '')
                # except:
                #     pass
                # setattr(player_stats, 'who_am_i', player_name)

                # stash it in the dict of all players we've come accross having stats
                player_stats_dict[player_srid] = player_stats

            ##################################################################
            # the code below needs to do the same thing as
            # the parser for this sport when it updates PlayerStats models
            ##################################################################

            # set the appropriate stats for this object 'o's parent_list__id
            parent_list = o.get('parent_list__id')

            if parent_list == "passing__list":
                # print('passing__list', str(o))
                player_stats.pass_td = o.get('touchdowns', 0)
                player_stats.pass_yds = o.get('yards', 0)
                player_stats.pass_int = o.get('interceptions', 0)

            elif parent_list == "rushing__list":
                # print('rushing__list', str(o))
                player_stats.rush_td = o.get('touchdowns', 0)
                player_stats.rush_yds = o.get('yards', 0)

            elif parent_list == "receiving__list":
                # print('receiving__list', str(o))
                player_stats.rec_td = o.get('touchdowns', 0)
                player_stats.rec_yds = o.get('yards', 0)
                player_stats.rec_rec = o.get('receptions', 0)

            elif parent_list == "punt_returns__list":
                # print('punt_returns__list', str(o))
                player_stats.ret_punt_td = o.get('touchdowns', 0)

            elif parent_list == "kick_returns__list":
                # print('kick_returns__list', str(o))
                player_stats.ret_kick_td = o.get('touchdowns', 0)

            elif parent_list == "fumbles__list":
                # print('fumbles__list', str(o))
                player_stats.off_fum_lost = o.get('lost_fumbles', 0)
                player_stats.off_fum_rec_td = o.get('own_rec_tds', 0)

            elif parent_list == "conversions__list":
                player_stats.two_pt_conv = o.get('successes', 0)

                ##################################################################
                ##################################################################

        # return the complete player data
        return player_stats_dict
