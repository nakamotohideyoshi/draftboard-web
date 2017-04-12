import logging
from datetime import timedelta, time

from django.db.transaction import atomic
from django.utils import timezone
from pytz import timezone as pytz_timezone
from raven.contrib.django.raven_compat.models import client

from contest.classes import ContestPoolCreator
from prize.models import PrizeStructure
from sports.classes import SiteSportManager
from util.dfsdate import DfsDate
from .models import (
    Block,
    UpcomingBlock,  # proxy model for upcoming Block (all sports)
    BlockGame,
    DefaultPrizeStructure,
    BlockPrizeStructure,
)

logger = logging.getLogger('contest.schedule.classes')


class ScheduleManager(object):
    pass
    # deleted a lot of deprecated code from here


class ScheduleDay(object):
    """
    This is a factory that produces SportDays for each type of sport (MlbDay, NhlDay, etc). A SportDay is an object
    that has some properties that tell us when games for that sport usually start.

    With this info a Block is created. A block is a group of IRL games.
    """
    tzinfo_est = pytz_timezone('America/New_York')
    datetime_format_date = '%Y-%m-%d'
    datetime_format_time = '%I:%M %p'

    default_season_types = ['reg', 'pst']

    class SportDay(object):

        tzinfo_est = pytz_timezone('America/New_York')
        datetime_format_date = '%Y-%m-%d'
        datetime_format_time = '%I:%M %p'

        weekday = None
        saturday = None
        sunday = None

        weekday_values = [0, 1, 2, 3, 4]
        saturday_values = [5]
        sunday_values = [6]

        def __init__(self, site_sport, datetime_obj, games):
            self.site_sport = site_sport
            self.the_datetime = datetime_obj
            self.games = games

            # self.get_data()

            self.data = {
                'weekday': None,
                'type': None,
                'total': None,
                'include': None,
                'exclude': None,
                'include_times': None,
                'exclude_times': None,
                'include_pct': None,
            }

            self.get_data()

        def get_excluded_game_ids(self):
            return self.data['exclude']

        def get_excluded_games(self):
            return self.games.filter(pk__in=self.get_excluded_game_ids())

        def get_included_game_ids(self):
            return self.data['include']

        def get_included_games(self):
            return self.games.filter(pk__in=self.get_included_game_ids())

        def get_cutoff(self):
            """ get the 'cutoff_time' from the internal data """
            return self.data['cutoff_time']

        # def get_cutoff_datetime(self):
        #     return self.data['cutoff_datetime']

        def get_data(self):
            if self.games.count() == 0:
                return None

            weekday = None  # 0 - 6 day index.  its poorly named, but its NOT the self.weekday time() cutoff
            include = []
            exclude = []
            include_times = []
            exclude_times = []
            for game in self.games:

                if weekday is None:
                    # weekday = game.start.weekday()
                    #    ... i think its actually this:
                    weekday = self.get_local_datetime(game.start).weekday()

                datetime_start_est = self.get_local_datetime(game.start)
                if weekday in [0, 1, 2, 3, 4] and self.include_in_weekday_block(datetime_start_est):
                    include.append(game.pk)
                    include_times.append(self.get_str_local_time(game.start))
                elif weekday in [5] and self.include_in_saturday_block(datetime_start_est):
                    include.append(game.pk)
                    include_times.append(self.get_str_local_time(game.start))
                elif weekday in [6] and self.include_in_sunday_block(datetime_start_est):
                    include.append(game.pk)
                    include_times.append(self.get_str_local_time(game.start))
                else:
                    exclude.append(game.pk)
                    exclude_times.append(self.get_str_local_time(game.start))

            # self.data = {
            #     'weekday'       : weekday,
            #     'type'          : self.weekday_to_str(weekday),
            #     'total'         : self.games.count(),
            #     'include'       : include,
            #     'exclude'       : exclude,
            #     'include_times' : include_times,
            #     'exclude_times' : exclude_times,
            #     'include_pct'   : float(float(len(include)) / float(self.games.count()))
            # }
            self.save_internal_data(weekday, self.weekday_to_str(weekday), self.games.count(),
                                    include, exclude, include_times, exclude_times)

            return self.data

        def save_internal_data(self, weekday, type, total, include, exclude, include_times,
                               exclude_times):
            self.data = {
                'weekday': weekday,
                'type': type,
                'total': total,
                'include': include,
                'exclude': exclude,
                'include_times': include_times,
                'exclude_times': exclude_times,
                'include_pct': float(float(len(include)) / float(total)),
                'cutoff_time': self.get_weekday_cutoff_time(weekday),
            }

        def __str__(self):
            include_pct = self.data['include_pct']
            if include_pct is None:
                include_pct = 0.0
            else:
                include_pct = int(include_pct * 100.0)

            included = self.data['include']
            if included is None:
                included = 0
            else:
                included = len(included)

            return 'type: %s, weekday:%s, included games:%s pct   (%s of %s) >>> included times %s  ((excluded times %s))' \
                   '' % (self.data['type'], self.data['weekday'], include_pct,
                         included, str(self.data['total']), str(self.data['include_times']),
                         str(self.data['exclude_times']))

        def weekday_to_str(self, weekday):
            if weekday in self.weekday_values:
                return 'Weekday'
            elif weekday in self.saturday_values:
                return 'Saturday'
            elif weekday in self.sunday_values:
                return 'Sunday'

        def get_weekday_cutoff_time(self, weekday):
            """
            this is an internal method.

            use method get_cutoff() to retrieve the datetime.time()
            specifically related to the day of this instance
            after this sportday  has been updated
            """

            if weekday in self.weekday_values:
                return self.weekday
            elif weekday in self.saturday_values:
                return self.saturday
            elif weekday in self.sunday_values:
                return self.sunday

        def get_local_datetime(self, utc_datetime_obj):
            return utc_datetime_obj.astimezone(self.tzinfo_est)

        def get_str_local_time(self, datetime_obj):
            local_dt = datetime_obj.astimezone(self.tzinfo_est)
            return local_dt.strftime(self.datetime_format_time)

        def get_str_local_date(self, datetime_obj):
            local_dt = datetime_obj.astimezone(self.tzinfo_est)
            return local_dt.strftime(self.datetime_format_date)

        def include_in_weekday_block(self, datetime_obj):
            return datetime_obj.time() >= self.weekday

        def include_in_saturday_block(self, datetime_obj):
            return datetime_obj.time() >= self.saturday

        def include_in_sunday_block(self, datetime_obj):
            return datetime_obj.time() >= self.sunday

    class MlbDay(SportDay):

        weekday = time(19, 0)  # 7pm +
        saturday = time(16, 0)  # 4pm +
        sunday = time(13, 0)  # 1pm +

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

    class NhlDay(SportDay):

        weekday = time(19, 0)  # 7pm +
        saturday = time(19, 0)  # 7pm +
        sunday = time(15, 0)  # 3pm +

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

    class NbaDay(SportDay):

        weekday = time(19, 0)  # 7pm +
        saturday = time(19, 0)  # 7pm +
        sunday = time(18, 0)  # 6pm +

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

    class NflDay(SportDay):

        weekday = time(19, 0)  # 7pm +  (thursday night games)
        saturday = time(13, 0)  # 1pm +  (saturday games)
        sunday = time(13, 0)  # 1pm +  (sunday games)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

    @staticmethod
    def factory(sport):
        if sport == 'nba':
            return ScheduleDay.NbaDay
        if sport == 'nhl':
            return ScheduleDay.NhlDay
        if sport == 'mlb':
            return ScheduleDay.MlbDay
        if sport == 'nfl':
            return ScheduleDay.NflDay

        else:
            raise Exception('ScheduleDay for sport: %s - UNIMPLEMENTED' % sport)
            # def get_data(self):
            #     if self.games.count() == 0:
            #         return None
            #
            #     weekday = None
            #     include = []
            #     exclude = []
            #     include_times = []
            #     exclude_times = []
            #     for game in self.games:
            #
            #         if weekday is None:
            #             weekday = game.start.weekday()
            #
            #         datetime_start_est = self.get_local_datetime(game.start)
            #         if weekday in [0,1,2,3,4] and self.include_in_weekday_block(datetime_start_est):
            #             include.append(game.pk)
            #             include_times.append(self.get_str_local_time(game.start))
            #         elif weekday in [5] and self.include_in_saturday_block(datetime_start_est):
            #             include.append(game.pk)
            #             include_times.append(self.get_str_local_time(game.start))
            #         elif weekday in [6] and self.include_in_sunday_block(datetime_start_est):
            #             include.append(game.pk)
            #             include_times.append(self.get_str_local_time(game.start))
            #         else:
            #             exclude.append(game.pk)
            #             exclude_times.append(self.get_str_local_time(game.start))
            #
            #     self.data = {
            #         'weekday'       : weekday,
            #         'type'          : self.weekday_to_str(weekday),
            #         'total'         : self.games.count(),
            #         'include'       : include,
            #         'exclude'       : exclude,
            #         'include_times' : include_times,
            #         'exclude_times' : exclude_times,
            #         'include_pct'   : float(float(len(include)) / float(self.games.count()))
            #     }
            #
            #     return self.data

    def __init__(self, sport, season=None, season_types=None):
        self.data = None
        self.sport = sport
        self.sport_day_class = ScheduleDay.factory(self.sport)
        self.site_sport_manager = SiteSportManager()
        self.site_sport = self.site_sport_manager.get_site_sport(self.sport)
        self.game_model_class = self.site_sport_manager.get_game_class(self.site_sport)
        self.season = season  # season is None, only get games for the season type after 'now'
        self.season_types = season_types
        if self.season_types is None:
            self.season_types = self.default_season_types

        # setup the datetime range with a start and end
        self.start = None
        self.end = None

    def get_data(self):
        return self.data

    def update_range(self, days_ago):
        """
        add timedelta(days=days) to the start and end datetime object

        :param days_ago:
        :return:
        """
        dfs_date_range = DfsDate.get_current_dfs_date_range()
        # set our dfsday range to start on the first day of the games we found
        self.start = dfs_date_range[0] - timedelta(days=days_ago)
        self.end = dfs_date_range[1] - timedelta(days=days_ago)

    def get_day_range(self):
        return self.start, self.end

    def get_days_since(self, datetime_obj):
        td = (timezone.now() - datetime_obj)
        return abs(td.days) + 1

    def increment_day_range(self):
        self.start = self.start + timedelta(days=1)
        self.end = self.end + timedelta(days=1)

    def update(self, verbose=False):
        """
        update the list of dfs days, with tuples of the start times
        and lists of all the games with their own unique start times
        """
        # if running for the first time, its very likely you wont want to add 1 day to start time
        # dfs_date_tomorrow = DfsDate.get_current_dfs_date_range()[0] + timedelta(days=1)
        dfs_date_tomorrow = DfsDate.get_current_dfs_date_range()[0]

        games = []  # default
        self.data = []
        if self.season is None:
            # we are going to have to find the following dfs day... and check gte its start time
            games = self.game_model_class.objects.filter(
                start__gt=dfs_date_tomorrow,
                season__season_type__in=self.season_types).order_by('start')  # oldest first
        else:
            games = self.game_model_class.objects.filter(
                season__season_year=self.season,
                season__season_type__in=self.season_types).order_by('start')  # oldest first

        if games.count() <= 0:
            logger.info('0 games found. exiting...')
            return
        else:
            logger.info('%s games found, as old as %s' % (games.count(), games[0].start))

        #
        days_ago = self.get_days_since(games[0].start)
        self.update_range(days_ago)
        day_range = self.get_day_range()

        # logger.info('first day (dt range)', str(day_range))

        # Weekdays@7pm or later
        # Saturdays@7pm or later
        # Sundays@6pm or later

        # idx = 0
        while games.filter(start__gt=self.get_day_range()[0]).count() > 0:
            # get all the games for the dfs day
            daily_games = games.filter(start__range=self.get_day_range())

            if daily_games.count() >= 2:
                # there must be more than 2 games for DFS!
                dt = self.get_day_range()[0]
                date_str = self.get_str_local_date(dt)
                self.data.append((date_str, self.sport_day_class(self.site_sport, dt, daily_games)))

            #
            self.increment_day_range()

    def get_str_local_time(self, datetime_obj):
        local_dt = datetime_obj.astimezone(self.tzinfo_est)
        return local_dt.strftime(self.datetime_format_time)

    def get_str_local_date(self, datetime_obj):
        local_dt = datetime_obj.astimezone(self.tzinfo_est)
        return local_dt.strftime(self.datetime_format_date)

    def show_time_blocks(self):
        self.update()

        for date_str, sport_day in self.data:
            print(date_str, str(sport_day))


class ScheduleWeek(ScheduleDay):
    default_season_types = ['reg']

    def update_range(self, days_ago):
        """
        add timedelta(days=days) to the start and end datetime object

        :param days:
        :return:
        """
        dfs_date_range = DfsDate.get_current_nfl_date_range()
        # set our dfsday range to start on the first day of the games we found
        self.start = dfs_date_range[0] - timedelta(days=days_ago)
        self.end = dfs_date_range[1] - timedelta(days=days_ago)

    def increment_day_range(self):
        """
        increment the weekly range by adding 7
        """
        self.start = self.start + timedelta(days=7)
        # self.end = self.end + timedelta(days=7)
        self.end = self.start + timedelta(days=3)


class ContestPoolScheduleManager(object):
    """
    This class takes over all the duties of ensuring that ContestPools are created at the proper
    times.
    """

    class ActiveBlockNotFoundException(Exception):
        pass

    max_days_upcoming = 10

    def __init__(self, sport):
        self.sport = sport

        # testing
        self.sport_day = None

    def get_active_block(self):
        """
        helper method to return the first UpcomingBlock

        note: this "active" block may or may not have
        its ContestPools created -- but if it hasnt,
        its certainly likely you will want to create them
        because this block is slated to be drafting
        on the front of the site (in all likelihood).
        """

        upcoming_blocks = UpcomingBlock.objects.filter(site_sport__name=self.sport)
        if upcoming_blocks.count() == 0:
            err_msg = '[%s] ContestPoolScheduleManager an active block could not be found!' % self.sport
            logger.error(err_msg)
            raise self.ActiveBlockNotFoundException(err_msg)

        # return the first UpcomingBlock
        return upcoming_blocks[0]

    @atomic
    def create_upcoming_contest_pools(self):
        """
        attempts to create Contest Pools for the active block (if they havent been created).
        """
        active_block = self.get_active_block()
        if active_block.contest_pools_created is False:
            self.create_contest_pools(active_block)

    @atomic
    def create_contest_pools(self, block):
        """
        this will create ContestPools which should
        appear on the website and be active right now.
        """

        #
        ##################################################
        # this method should probably not automatically
        # try to determine which block should have its
        # ContestPools created. it should simply use the
        # 'block' argument specified!
        ##################################################

        # use the blockmanager to create all necessary ContestPools
        block_manager = BlockManager(block)
        block_manager.create_contest_pools()

    @atomic
    def run(self, now=None):
        """
        create the Blocks for the admin to see what ContestPools
        are currently planned to be created in the upcoming days.
        """
        if now is None:
            now = timezone.now()

        # create a ScheduleDay object and call update() to load real-time
        # information about the actual live games for the sport.
        schedule_day = ScheduleDay(self.sport)
        schedule_day.update()

        # create any necessary blocks
        for date_str, sport_day in schedule_day.get_data()[:self.max_days_upcoming]:
            logger.info('Creating Blocks for %s - %s' % (sport_day, date_str))
            self.sport_day = sport_day
            # use the BlockCreator to make new blocks
            # which will have all teh default prize structures
            # and display the included/excluded games currently included/excluded
            block_creator = BlockCreator(sport_day)

            # creates the block (although we dont do anything with the new block, it is returned)
            block = block_creator.create()


class BlockCreator(object):
    """
    Given a sport, create a Block
    """

    class BlockExistsException(Exception):
        """
        Exception raised when attempting to create a Block that already exists.

        Attributes:
            message -- Details of the block.
        """

        def __init__(self, message):
            logger.warning('Block already exists! %s' % message)
            pass

    def __init__(self, sport_day):
        self.sport_day = sport_day

    def create_block(self):
        """
        TODO - this creates DAILY blocks, and will need a tweak for NFL weekly stuff
             UPDATE - This appear to be implemented below in BlockCreatorMulti

        :return: the newly created Block
        """
        #
        # raise an exception if the block already exists
        site_sport = self.sport_day.site_sport
        start = self.sport_day.the_datetime
        end = start + timedelta(hours=24)
        cutoff_time = self.sport_day.get_cutoff()  # datetime.time() object
        logger.info('Attempting to create Block sport: %s | start: %s | end: %s' % (
            site_sport, start, end
        ))

        try:
            #
            # set fields: dfsday_start (datetime), dfsday_end (datetime), cutoff_time (time object)
            # Update: We're not filtering dupes by cutoff_time. This was causing multiple Blocks
            # to be created for a day if the schedule is manually changed.
            # We only ever want 1 Block per day, per sport, this should account for that.
            err_msg = 'A %s scheduled block already exists for dfsday: start: %s | end: %s' % (
                site_sport.name, start, end)

            block = Block.objects.get(
                site_sport=site_sport,
                dfsday_start=start,
                dfsday_end=end)

            logger.warning(err_msg)
            # Create any BlockPrizeStructure for this existing Block. If we don't do this, any new
            # prize structures will not be created to existing Blocks and thus will not spawn
            # contests.
            BlockPrizeStructureCreator(block).create()

            # The block already exists, exit out of here instead of creating one.
            raise self.BlockExistsException(err_msg)

        # There is already More than one block for this day!
        except Block.MultipleObjectsReturned:
            raise self.BlockExistsException(err_msg)

        # If the block doesn't exist, keep going and create one.
        except Block.DoesNotExist:
            pass

        # create it
        block = Block.objects.create(
            site_sport=self.sport_day.site_sport,
            dfsday_start=start,
            dfsday_end=end,
            cutoff_time=cutoff_time)
        return block

    @staticmethod
    def create_block_games(block, games):
        block_games = []
        for game in games:
            logger.info('creating a BlockGame for %s' % game)
            block_game = BlockGame()
            block_game.block = block
            block_game.name = game.get_home_at_away_str()
            block_game.srid = game.srid
            block_game.game = game
            block_game.save()

            block_games.append(block_game)
        return block_games

    def create(self):
        """
        create the block, its block games from the SportDay instance information,
        as well as the block prize structures.

        keep in mind this creates the Blocks -- NOT the actual ContestPools themselves.

        returns the Block created
        """

        # create a new block
        try:
            block = self.create_block()
        except self.BlockExistsException:
            logger.warning('Existing block for day - skipping it.')
            return

        # create the BlockGames (both included & excluded)
        included_games = self.sport_day.get_included_games()
        excluded_games = self.sport_day.get_excluded_games()
        all_games = list(included_games) + list(excluded_games)
        block_games = self.create_block_games(block, all_games)  # returns the created BlockGames
        logger.info('Block Created %s' % block)

        # create the block prize structures
        block_prize_structure_creator = BlockPrizeStructureCreator(block)
        block_prize_structure_creator.create()
        return block


class BlockCreatorMulti(BlockCreator):
    # TODO: for things like nfl's Thursday - Monday slate, we need to implement this class

    def __init__(self, sport_days):
        """
        :param sport_days: a list of 'sport_day' objects
        """
        self.sport_days = sport_days

    def get_site_sport(self):
        if len(self.sport_days) == 0:
            raise Exception('empty sport_days list')
        # otherwise
        return self.sport_days[0].site_sport

    def get_cutoff(self):
        """
        get the cutoff of the first day in the sport_days list.

        :return: a datetime.time() object
        """
        return self.sport_days[0].get_cutoff()

    def get_start(self):
        return self.sport_days[0].the_datetime

    def get_end(self):
        return self.sport_days[-1].the_datetime

    def create_block(self):
        """
        creates a multi day block

        :return: the newly created Block
        """
        #
        # raise an exception if the block already exists
        site_sport = self.get_site_sport()
        start = self.get_start()
        end = self.get_end()
        cutoff_time = self.get_cutoff()  # datetime.time() object
        logger.info('Attempting to create Multi Block sport: %s | start: %s | end: %s' % (
            site_sport, start, end
        ))

        try:
            #
            # set fields: dfsday_start (datetime), dfsday_end (datetime), cutoff_time (time object)
            Block.objects.get(site_sport=site_sport,
                              dfsday_start=start,
                              dfsday_end=end,
                              cutoff_time=cutoff_time)
            err_msg = 'a %s scheduled block already exists' % site_sport.name
            logger.warning(err_msg)
            raise self.BlockExistsException(err_msg)
        except Block.DoesNotExist:
            pass

        # create it
        block = Block.objects.create(site_sport=site_sport,
                                     dfsday_start=start,
                                     dfsday_end=end,
                                     cutoff_time=cutoff_time)
        return block


class BlockManager(object):
    def __init__(self, block):
        self.block = block
        self.cutoff = self.block.get_utc_cutoff()
        self.block_prize_structures = BlockPrizeStructure.objects.filter(block=self.block)
        self.site_sport_manager = SiteSportManager()
        self.game_model_class = self.site_sport_manager.get_game_class(self.block.site_sport)

    def create_contest_pools(self):
        """
        to determine the start of the earliest game in the block, we look for
        all games between the dfsday_start and dfsday_end of the block,
        and get the earliest start time of games after the cutoff.
        this ensures we capture all the games in the range, as opposed
        to relying on the BlockGame objects which have a very low chance
        of not including very recent scheduling changes!
        """

        # If we've already created pools for this block, don't attempt to create more,
        # that would cause us to have multiple slates of pools per day.
        if self.block.contest_pools_created:
            logger.info('Contests pools have already been created for this block, '
                        'not creating more. %s' % self.block)
            return

        # default
        num_contest_pools_created = 0

        # determine the start time
        included_games = self.game_model_class.objects.filter(
            start__gte=self.cutoff,
            start__lt=self.block.dfsday_end
        ).order_by('start')

        # we will not check if there are enough games here, and
        # ultimately let the draft group creator raise an exception
        # if it cant find enough games!
        if included_games.count() >= 1:

            earliest_start_time = included_games[0].start

            # duration is the # of minutes until the end of the Block (dfsday_end)
            td = self.block.dfsday_end - earliest_start_time
            duration = int(td.total_seconds() / 60)  # convert seconds to minutes

            # create all required ContestPools
            logger.info('%s formats based on default %s PrizeStructure(s)' % (
                len(self.block_prize_structures),
                self.block.site_sport)
                        )
            for block_prize_structure in self.block_prize_structures:
                # additional (optional) ContestPoolCreator arguments:
                #  draft_group=None, user_entry_limit=None, entry_cap=None
                contest_pool_creator = ContestPoolCreator(
                    self.block.site_sport.name, block_prize_structure.prize_structure,
                    earliest_start_time, duration, set_name=True)

                # because this method may attempt to create a DraftGroup,
                # we must be able to handle the DraftGroup exceptions that
                # could potentially be thrown.

                contest_pool = contest_pool_creator.get_or_create()
                num_contest_pools_created += 1
                logger.info('creating ContestPool: %s for Block: %s' % (contest_pool, self.block))

                #
                # we really want to let exceptions propagate up to the admin
                # so were not currently catching any in here...

        if num_contest_pools_created != 0:
            self.block.contest_pools_created = True
        self.block.save()

        logger.info(
            '%s ContestPool(s) created for Block: %s' % (num_contest_pools_created, self.block))


class BlockPrizeStructureCreator(object):
    """
    creates only the BlockPrizeStructures for a Block
    """

    def __init__(self, block):
        self.block = block
        if isinstance(self.block, int):
            # if 'block' is an integer, assume its the pk and get the Block model
            self.block = Block.objects.get(pk=self.block)

        # now self.block should be a Block instance
        if not isinstance(self.block, Block):
            logger.error('"block" is not a Block instance')
            raise Exception('"block" is not a Block instance')

    def create(self):
        """
        Perform the initial creation of all the BlockPrizeStructure(s) by giving the block every
        PrizeStructure from its sports DefaultPrizeStructure table
        """
        logger.info('Creating BlockPrizeStructures for %s' % self.block)

        for default_prize_structure in DefaultPrizeStructure.objects.filter(
                site_sport=self.block.site_sport):
            # If the BlockPrizeStructure for this DefaultPrizeStructure doesn't exist, create it.
            if not BlockPrizeStructure.objects.filter(
                    block=self.block,
                    prize_structure=default_prize_structure.prize_structure
            ).count() > 0:
                logger.info('Creating non-existant BlockPrizeStructure for %s - %s' % (
                    default_prize_structure, self.block))
                try:
                    bps = BlockPrizeStructure()
                    bps.block = self.block
                    bps.prize_structure = default_prize_structure.prize_structure
                    bps.save()

                except Exception as e:
                    # Couldn't create it, but maybe it already existed? Either way, we don't want
                    # this to stop the entire contest pool creation process, so capture the error
                    # and keep chugging.
                    logger.error(e)
                    client.captureException()
                    pass


class DefaultPrizeStructureManager(object):
    """
    manages each sports default set of prize structures.
    this is the templates from which all new blocks receive
    their BlockPrizeStructures.
    """

    default_buyin_amounts = [1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0]
    default_contest_sizes = [(2, 1), (10, 5), (10, 3)]  # each tuple: (size, payouts)

    @staticmethod
    def create_initial_default_prize_structures():

        site_sport_manager = SiteSportManager()
        for sport in SiteSportManager.SPORTS:
            created_default_prize_structures = 0
            site_sport = site_sport_manager.get_site_sport(sport)
            for buyin in DefaultPrizeStructureManager.default_buyin_amounts:
                for size, payout_spots in DefaultPrizeStructureManager.default_contest_sizes:
                    # get the prize structure based on the buyin and # of payout spots
                    prize_structures = PrizeStructure.objects.filter(
                        generator__buyin=buyin, generator__payout_spots=payout_spots)
                    prize_structure = None  # loop until we find it
                    for ps in prize_structures:
                        if size == ps.get_entries():
                            prize_structure = ps
                            break  # we found it
                    if prize_structure is None:
                        logger.warning(
                            ("No PrizeStructure for buyin: %s payout_spots: %s. You can add them "
                             "manually though!") % (buyin, payout_spots))
                        # raise Exception(err_msg)

                    else:
                        #
                        # create the default prize structures for the SiteSport
                        dps = DefaultPrizeStructure()
                        dps.site_sport = site_sport
                        dps.prize_structure = prize_structure
                        dps.save()
                        created_default_prize_structures += 1

            logger.info("%s created_default_prize_structures for %s" % (
                created_default_prize_structures, sport))
