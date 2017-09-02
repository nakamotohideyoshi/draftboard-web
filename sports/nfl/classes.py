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

        # were going to keep track of the player srids we've seen for each call to update() for a specific game
        self.mongo_player_srids = []

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

    def update_existing_player_stats(self, game_srid, exclude_player_srids=[]):
        """
        query draftboard Playerstats for this game, and zero the stats for any players NOT FOUND in
        exclude_player_srids

        :param game_srid:
        :return:
        """
        player_stats_model_class = self.get_player_stats_model_class()
        player_stats_models = player_stats_model_class.objects.filter(srid_game=game_srid)
        for player_stats_model in player_stats_models:
            if player_stats_model.srid_player not in exclude_player_srids:
                # zero stats, and call model .save() to fix stats
                # player_stats.pass_td = o.get('touchdowns', 0)
                # player_stats.pass_yds = o.get('yards', 0)
                # player_stats.pass_int = o.get('interceptions', 0)
                # player_stats.rush_td = o.get('touchdowns', 0)
                # player_stats.rush_yds = o.get('yards', 0)
                # player_stats.rec_td = o.get('touchdowns', 0)
                # player_stats.rec_yds = o.get('yards', 0)
                # player_stats.rec_rec = o.get('receptions', 0)
                # player_stats.ret_punt_td = o.get('touchdowns', 0)
                # player_stats.ret_kick_td = o.get('touchdowns', 0)
                # player_stats.off_fum_lost = o.get('lost_fumbles', 0)
                # player_stats.off_fum_rec_td = o.get('own_rec_tds', 0)
                # player_stats.two_pt_conv = o.get('successes', 0)

                # set all properties with these fieldnames to 0
                fieldnames = player_stats_model_class.SCORING_FIELDS
                for fieldname in fieldnames:
                    setattr(player_stats_model, fieldname, 0)
                    player_stats_model.save()

    def create_player_stats_model(self, game_srid, player_srid, my_player_stats_instance):
        """
        create a new PlayerStats model instance from the fields of the 'mongo_obj'
        :param mongo_obj:
        :return:
        """

        #print('find player by srid: ' + str(player_srid))
        site_sport_manager = SiteSportManager()
        site_sport = site_sport_manager.get_site_sport('nfl')
        player_model_class = site_sport_manager.get_player_class(site_sport)
        game_model_class = site_sport_manager.get_game_class(site_sport)

        try:
            player = player_model_class.objects.get(srid=player_srid)
        except player_model_class.DoesNotExist:
            return # if they were never in the database, they wont be in draft group and we should not deal with that here!

        #print('found player: ' + str(player))

        print('create_player_stats_model() for: ' + str(my_player_stats_instance))

        player_stats_model_class = self.get_player_stats_model_class()

        # get new instance
        player_stats = player_stats_model_class()

        # set all properties with these fieldnames to 0
        player_stats.position = player.position # use the position from their Player object
        player_stats.srid_game = game_srid
        player_stats.game = game_model_class.objects.get(srid=game_srid)
        player_stats.srid_player = player_srid
        player_stats.player = player
        for fieldname, var in my_player_stats_instance.get_vars().items():
            #print('    %s : %s' % (str(fieldname), str(var)))
            setattr(player_stats, fieldname, var)
            player_stats.save()

        #logger.info('Wiped all stats for player no longer in SR feed. Player: %s' % (player_stats_model))

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

        # keep track of the draftboard player srids we have a PlayerStats object for
        draftboard_player_srids = []

        # update any of them that have more recent changes
        for player_stats_model in player_stats_models:
            player_srid = player_stats_model.srid_player

            #
            draftboard_player_srids.append(player_srid)

            my_player_stats = player_stats_data.get(player_srid, None)
            if my_player_stats is not None:
                # save() model to django backend if there are any changes
                self.update_player_stats_model(my_player_stats, player_stats_model)

        # we need to create any PlayerStats objects if we have a
        # mongo object for a player but no PlayerStats instance!
        #print('draftboard_player_srids: ' + str(draftboard_player_srids))
        for player_srid, my_player_stats_instance in player_stats_data.items():
            if player_srid not in draftboard_player_srids:
                # create a new PlayerStats object!
                #print('SHOULD CREATE NEW PLAYERSTATS OBJECT FOR: ' + str(srid))
                self.create_player_stats_model(game_srid, player_srid, my_player_stats_instance)

        logger.info('Player stat correction sync complete for game: %s', game_srid)

    def build_data(self, game_srid):
        """
        build a dictionary of player stats objects which very closely resemble
        the sports.<sport>.models.PlayerStats objects from the most recent parse of the stats feed.

        :param game_srid:
        :return: a dictionary of player stats objects built from the most recent parse of the feed
        """

        self.mongo_player_srids = [] # initialization. clear this list each time update() is called
        player_stats_dict = {} # we will add player_stats_data dicts to this object using the players srid as the key

        mongo_objects = self.get_player_stats_for(game_srid)
        logger.info('%s player stats found in the MongoDB for game %s' % (
            mongo_objects.count(), game_srid))

        # iterate all the objects and compile all the stats for each player
        for o in mongo_objects:
            # print(str(o)) # debug print if you want to see each mongo object

            player_srid = o.get('id')

            # add this player_srid to the list of ones we've updated
            self.mongo_player_srids.append(player_srid)

            # update mongo players found
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

        # update to zero out EXISTING non-DST PlayerStats for player srids (for this game)
        # which were not found in mongo -- it means they were removed from the raw feed!
        self.update_existing_player_stats(game_srid, self.mongo_player_srids)

        # return the complete player data
        return player_stats_dict
