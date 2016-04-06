#
# contest/schedule/classes.py

from django.conf import settings
from pytz import timezone as pytz_timezone
from datetime import timedelta, datetime, time, date
from django.utils import timezone
from django.db.transaction import atomic
from django.db.models import Q
import contest.models
from draftgroup.classes import DraftGroupManager
from util.slack import WebhookContestScheduler
from mysite.exceptions import (
    NoGamesInRangeException,
)
from draftgroup.exceptions import (
    NotEnoughGamesException,
    EmptySalaryPoolException,
    NoGamesAtStartTimeException,
)
from .exceptions import (
    ScheduleException,
    ScheduleOutOfRangeException,
    SchedulerNumberOfGamesException,
)
from .models import (
    Schedule,
    TemplateContest,
    ScheduledTemplateContest,
    CreatedContest,
    Block,
    BlockGame,
    DefaultPrizeStructure,
    BlockPrizeStructure,
)
from util.midnight import midnight
from sports.classes import (
    SiteSportManager,
)
from prize.models import (
    PrizeStructure,
)
from util.dfsdate import DfsDate

class ScheduleManager(object):
    """
    This class is used to create scheduled contests within the next 7 days.

    These models are used by the schedule to maintain
    what has already been, and what needs to be scheduled:

        Schedule                    - master entry, which many ScheduledTemplateContest(s) point to
        TemplateContest             - information to be able to clone a Contest
        ScheduledTemplateContest    - the map between a TemplateContest + Schedule
        CreatedContest              - an entry that indicates the contest was created

    """

    # TODO throws InvalidDateException if this class is attempted to be used in the past
    #       or more than 1 week from the current datetime.

    NOW_FORMAT = '%Y-%m-%d %H:%M:%S'

    MAX_SKIP_DAYS = 6

    class Schedule(object):

        def __init__(self, schedule_model, dt=None):
            """

            :param schedule_model: the schedule for which we will get
                        TemplateContest objects, and create corresponding Contests if necessary
            :param dt: datetime object, if None we use the current time to decide what to schedule
            :return:
            """
            self.now = dt
            if dt is None:
                self.now = timezone.now()

            self.schedule_model     = schedule_model
            self.scheduled_contests = self.get_scheduled_template_contests( self.now )

            # debug print the scheduled_contests we find
            # for sc in self.scheduled_contests:
            #     print( '    ', sc )

        def get_scheduled_template_contests(self, dt):
            """
            get all the ScheduledTemplateContest objects for the the datetime object dt

            :param dt:
            :return:
            """

            # TODO TODO we need to decide when to schedule upcoming games (~3 hours before start of todays games?)
            weekday = dt.weekday() # the current weekday of the server
            q = None
            if weekday == 0: q = Q(interval__monday=True)
            elif weekday == 1: q = Q(interval__tuesday=True)
            elif weekday == 2: q = Q(interval__wednesday=True)
            elif weekday == 3: q = Q(interval__thursday=True)
            elif weekday == 4: q = Q(interval__friday=True)
            elif weekday == 5: q = Q(interval__saturday=True)
            elif weekday == 6: q = Q(interval__sunday=True)
            else: raise Exception('weekday is not in the range [0-6]!')

            return ScheduledTemplateContest.objects.filter( q, schedule=self.schedule_model )

        def update(self):
            """
            creates new live Contests for scheduled contests which need to be created

            the process is essentially this:

                WE HAVE THEM ALREADY  ->    1) get all the ScheduledTemplateContest objects for the WEEKDAY
                2) for each template
                    a) if there is a record showing we already
                        created it (ScheduledContest entry), do nothing
                    b) else: atomically create a new ScheduledContest entry,
                        and also create the actual Contest
            """

            sport_webhook = WebhookContestScheduler.get_for_sport(self.schedule_model.site_sport.name)

            on_or_off = ' Disabled '
            if self.schedule_model.enable:
                on_or_off = ' *Active* '

            number_of_scheduled_contests = len(self.scheduled_contests)

            print('')
            print('-----------------------------------------------------------------')
            print('%s  --  %s        %s [%s contests]' % (on_or_off,
                       str(self.schedule_model), str(self.now.date()), str(len(self.scheduled_contests))))
            print('-----------------------------------------------------------------')

            if not self.schedule_model.enable:
                sport_webhook.send(str(self.schedule_model), 0, 0, 0)
                return

            existing    = 0
            created     = 0
            for stc in self.scheduled_contests:
                # get all created_contests, and make sure the multiplier
                # matches the count of everything returned by the filter
                created_contests = CreatedContest.objects.filter( day=self.now.date(),
                                                    scheduled_template_contest=stc )
                n = created_contests.count()
                if  n>0 and n == stc.multiplier:
                    print('    existing (%s):'%(str(n)), str(created_contests[0]))
                    existing += 1   # not 'n' because multipliers wont be used often, and will confuse

                else:
                    # create all remaining contests to be created
                    for x in range(stc.multiplier - n):
                        self.create_scheduled_contest(stc)
                        print( '    created:', str(stc))
                        created += 1

            #
            # send webhook
            schedule_text = '%s [%s contests]' % (str(self.schedule_model), str(len(self.scheduled_contests)))
            sport_webhook.send(schedule_text, existing, created, number_of_scheduled_contests)

        @atomic
        def create_scheduled_contest(self, scheduled_template_contest):
            """
            Atomically create the CreatedContest as well as the actual live Contest

            This method does not do any validation to ensure it hasnt already been created,
            so make sure to only use this method internal to update() or any other
            method that knows it wont be duplicating already existing Contests
            """

            day             = self.now.date()                             # the date we are creating it for
            created_contest = CreatedContest()                              # create a record of having created it
            template        = scheduled_template_contest.template_contest   # create the new contest from this template

            # copy all the contest properties
            c = self.create_contest_from_template( scheduled_template_contest )

            # save the created_contest
            created_contest.contest = c
            created_contest.scheduled_template_contest = scheduled_template_contest
            created_contest.day = day
            created_contest.save()

        def create_contest_from_template(self, scheduled_template_contest):
            """
            Using the relevant fields from TemplateContest object, create
            a new contest.models.Contest object !

            Returns the newly created Contest
            """

            template_contest = scheduled_template_contest.template_contest

            c = contest.models.Contest()
            c.site_sport        = template_contest.site_sport
            c.name              = template_contest.name
            c.prize_structure   = template_contest.prize_structure

            # create the start datetime by combining the now().date() with the scheduled datetime's time() object
            utc_dt              = self.now          # get now() just so we have a datetime with tzinfo == <UTC>
            d                   = utc_dt.date()
            t                   = scheduled_template_contest.start_time
            utc_start           = utc_dt.replace( d.year, d.month, d.day, t.hour, t.minute, 0, 0 )
            #print('utc_start:', str(utc_start), 'self.dst_offset_hours():', self.get_dst_offset_hours() )
            utc_start           = utc_start + timedelta(hours=self.get_dst_offset_hours())
            #print('utc_start(after + dst):', str(utc_start))
            c.start             = utc_start
            c.end               = utc_start + timedelta(minutes=scheduled_template_contest.duration_minutes)

            c.max_entries       = template_contest.max_entries
            c.entries           = template_contest.entries

            c.gpp               = template_contest.gpp
            c.respawn           = template_contest.respawn
            c.doubleup          = template_contest.doubleup

            # get or create the draft group
            dgm = DraftGroupManager()
            draft_group = None
            try:
                draft_group = dgm.get_for_site_sport( c.site_sport, c.start, c.end )
            except (NoGamesInRangeException, NotEnoughGamesException):
                # these exceptions basically indicate there was break
                # in schedule... we should try to create games for the following
                # day (or 6) before giving up.
                raise SchedulerNumberOfGamesException()
            except NoGamesAtStartTimeException:
                msg = 'Contest(s) not created -- \n'
                msg += 'there are no games matching the start time [%s]\n' % c.start
                raise ScheduleException(msg)

            except EmptySalaryPoolException:
                msg = 'Contest(s) not created -- you need to generate a salary pool first.'
                raise ScheduleException(msg)

            except:
                msg = 'Contest(s) not created -- are there games for this day?'
                raise ScheduleException(msg)

            c.draft_group = draft_group

            c.save()
            return c

        def get_dst_offset_hours(self):
            # get the local time in 'America/New_York' timezone,
            # as well as local time in UTC, and return the difference in hours
            # it should be 4 or 5 !
            tz = pytz_timezone( settings.TIME_ZONE )    # settings.TIME_ZONE is like 'America/New_York'
            local_datetime = datetime.now(tz=tz)
            utc_datetime = timezone.now()               # get django.utils.timezone.now()
            if utc_datetime.hour <= 6:
                td = timedelta(hours=6)
                utc_datetime = utc_datetime + td
                local_datetime = local_datetime + td
            #
            # the offset should alwasy be 4 or 5
            return utc_datetime.hour - local_datetime.hour

    def __init__(self):
        self.schedules = Schedule.objects.all()

    def now_str(self):
        now = timezone.now()
        return '%s -- %s' % (now.strftime('%A'), now.strftime(self.NOW_FORMAT))

    def print_schedules(self):
        print('=================================================================')
        print('It is currently ', self.now_str() )
        print('=================================================================')
        print('')
        print('-----------------------------------------------------------------')
        print('Schedule Status')
        print('-----------------------------------------------------------------')
        for sched in self.schedules:
            on_or_off = ' Off '
            if sched.enable:
                on_or_off = ' On  '
            print( '     [%s]   ' % on_or_off, sched )

    def run(self, time_delta=None, allow_day_skipping=True):
        """
        Create Contests which need to be scheduled, and have not yet been created.

        This method can be run as often as necessary.

        :param allow_day_skipping: if this argument is True, this method
                                    will keep attempting to schedule contests
                                    on successive until it succeeds
                                    (for a limited number of days into the future)

        :return:
        """
        # if time_delta is passed, ensure its in valid range or raise exception
        if time_delta and (time_delta < timedelta(days=0) or time_delta > timedelta(days=6)):
            raise ScheduleOutOfRangeException()

        #
        # if a time_delta is specified, add it to the current time and
        # create the Schedule object for that datetime. if dt == None,
        # thats ok -- the default Schedule object is created for the
        # current server day !
        dt = None
        if time_delta:
            dt = timezone.now() + time_delta

        for sched in self.schedules:

            try:
                sc = self.Schedule( sched, dt=dt )
                sc.update() # run this schedule

            except SchedulerNumberOfGamesException:
                #
                # if day skipping is disabled, and we fail
                # to create the schedule for the given day,
                # then try no more... continue
                if not allow_day_skipping:
                    continue # ie dont pass on to the next part of code

                msg = '%s >>> warning - we are potentially skipping days' % str(sched)
                sport_webhook = WebhookContestScheduler.get_for_sport(sched.site_sport.name)
                sport_webhook.send( msg, 0, 0, 0, warn=True)

                #
                # allow_day_skipping is True at this point.
                # Try scheduling for the following days
                # until we find a day that works.
                print('allow_day_skipping == ', str(allow_day_skipping))
                for extra_days in range(1,self.MAX_SKIP_DAYS+1):  # ie: [1,2,3,4,5,6]
                    #
                    try:
                        sc = self.Schedule( sched, dt = timezone.now() + timedelta(days=extra_days+1) )
                        sc.update() # run this schedule

                    except (SchedulerNumberOfGamesException, ScheduleException):
                        # essentially for any exception that happens now
                        # just try the next day
                        continue
                    #
                    # at this point, the scheduler successfully made games for a day
                    # so happily continue thru the original/outter loop
                    pass

            except ScheduleException as se:
                # print there was an error, but keep going so
                # we dont prevent subsequent schedules from running
                print( se )

                sport_webhook = WebhookContestScheduler.get_for_sport(sched.site_sport.name)
                sport_webhook.send( str(sched), 0, 0, 0, err_msg=str(se))

class ScheduleDay(object):

    tzinfo_est              = pytz_timezone('America/New_York')
    datetime_format_date    = '%Y-%m-%d'
    datetime_format_time    = '%I:%M %p'

    default_season_types    = ['reg','pst']

    class SportDay(object):

        tzinfo_est              = pytz_timezone('America/New_York')
        datetime_format_date    = '%Y-%m-%d'
        datetime_format_time    = '%I:%M %p'

        weekday     = None
        saturday    = None
        sunday      = None

        weekday_values  = [0,1,2,3,4]
        saturday_values = [5]
        sunday_values   = [6]

        def __init__(self, site_sport, datetime_obj, games):
            self.site_sport = site_sport
            self.the_datetime = datetime_obj
            self.games = games

            #self.get_data()

            self.data = {
                'weekday'       : None,
                'type'          : None,
                'total'         : None,
                'include'       : None,
                'exclude'       : None,
                'include_times' : None,
                'exclude_times' : None,
                'include_pct'   : None,
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

        def get_cutoff_datetime(self):
            return self.data['cutoff_datetime']

        def get_data(self):
            if self.games.count() == 0:
                return None

            weekday = None
            include = []
            exclude = []
            include_times = []
            exclude_times = []
            for game in self.games:

                if weekday is None:
                    weekday = game.start.weekday()

                datetime_start_est = self.get_local_datetime(game.start)
                if weekday in [0,1,2,3,4] and self.include_in_weekday_block(datetime_start_est):
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
                                                include, exclude, include_times, exclude_times )

            return self.data

        def save_internal_data(self, weekday, type, total, include, exclude, include_times, exclude_times):
            self.data = {
                'weekday'       : weekday,
                'type'          : type,
                'total'         : total,
                'include'       : include,
                'exclude'       : exclude,
                'include_times' : include_times,
                'exclude_times' : exclude_times,
                'include_pct'   : float(float(len(include)) / float(total)),
                'cutoff_time'   : self.get_cutoff_time(weekday),
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
                         included, str(self.data['total']), str(self.data['include_times']), str(self.data['exclude_times']))

        def weekday_to_str(self, weekday):
            if weekday in self.weekday_values:
                return 'Weekday'
            elif weekday in self.saturday_values:
                return 'Saturday'
            elif weekday in self.sunday_values:
                return 'Sunday'

        def get_cutoff_time(self, weekday):
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

        weekday     = time(19, 0)   # 7pm +
        saturday    = time(16, 0)   # 4pm +
        sunday      = time(13, 0)   # 1pm +

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

    class NhlDay(SportDay):

        weekday     = time(19, 0)   # 7pm +
        saturday    = time(19, 0)   # 7pm +
        sunday      = time(15, 0)   # 3pm +

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

    class NbaDay(SportDay):

        weekday     = time(19, 0)   # 7pm +
        saturday    = time(19, 0)   # 7pm +
        sunday      = time(18, 0)   # 6pm +

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

    class NflDay(SportDay):

        weekday     = time(19, 0)   # 7pm +  (thursday night games)
        saturday    = time(13, 0)   # 1pm +  (saturday games)
        sunday      = time(13, 0)   # 1pm +  (sunday games)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

    @staticmethod
    def factory(sport):
        if sport == 'nba': return ScheduleDay.NbaDay
        if sport == 'nhl': return ScheduleDay.NhlDay
        if sport == 'mlb': return ScheduleDay.MlbDay
        if sport == 'nfl': return ScheduleDay.NflDay

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
        #self.sport_day = None # TODO set this up like NbaDay, MlbDay, etc...
        self.sport_day_class = ScheduleDay.factory(self.sport) #self.MlbDay #self.NbaDay # TODO TODO TOOD dont hardcode
        self.site_sport_manager = SiteSportManager()
        self.site_sport = self.site_sport_manager.get_site_sport(self.sport)
        self.game_model_class = self.site_sport_manager.get_game_class(self.site_sport)
        self.season = season # season is None, only get games for the season type after 'now'
        self.season_types = season_types
        if self.season_types is None:
            self.season_types = self.default_season_types

        # setup the datetime range with a start and end
        self.start = None
        self.end = None

    def update_range(self, days_ago):
        """
        add timedelta(days=days) to the start and end datetime object

        :param days:
        :return:
        """
        dfs_date_range = DfsDate.get_current_dfs_date_range()
        # set our dfsday range to start on the first day of the games we found
        self.start = dfs_date_range[0] - timedelta(days=days_ago)
        self.end  = dfs_date_range[1] - timedelta(days=days_ago)

    def get_day_range(self):
        return (self.start, self.end)

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
        dfs_date_tomorrow = DfsDate.get_current_dfs_date_range()[0] + timedelta(days=1)

        games = [] # default
        self.data = []
        if self.season is None:
            # we are going to have to find the following dfs day... and check gte its start time
            games = self.game_model_class.objects.filter(
                start__gt=dfs_date_tomorrow,
                season__season_type__in=self.season_types).order_by('start') # oldest first
        else:
            games = self.game_model_class.objects.filter(season__season_year=self.season,
                season__season_type__in=self.season_types).order_by('start') # oldest first

        if games.count() <= 0:
            print('0 games found. exiting...')
            return
        else:
            print('%s games found, as old as %s' % (games.count(), games[0].start))

        #
        days_ago = self.get_days_since(games[0].start)
        self.update_range(days_ago)
        day_range = self.get_day_range()

        print('')
        print('first day (dt range)', str(day_range))

        # Weekdays@7pm or later
        # Saturdays@7pm or later
        # Sundays@6pm or later

        # idx = 0
        while games.filter(start__gt=self.get_day_range()[1]).count() > 0:
            # get all the games for the dfs day
            daily_games = games.filter(start__range=self.get_day_range())


            if daily_games.count() >= 2:
                # there must be more than 2 games for DFS!
                dt = self.get_day_range()[0]
                date_str = self.get_str_local_date(dt)
                self.data.append( (date_str, self.sport_day_class(self.site_sport, dt, daily_games)) )

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
        self.end  = dfs_date_range[1] - timedelta(days=days_ago)

    def increment_day_range(self):
        """
        increment the weekly range by adding 7
        """
        self.start = self.start + timedelta(days=7)
        #self.end = self.end + timedelta(days=7)
        self.end = self.start + timedelta(days=3)

class ContestPoolScheduleManager(object): # TODO
    """
    This class takes over all the duties of ensuring that ContestPools
    are created at the proper times.
    """

    def __init__(self):
        self.upcoming_blocks = None # TODO get the the upcoming blocks

    def should_run(self):
        """
        """
        return True # TODO how are we going to know when NOT to run?

    def run(self):
        """
        """
        pass # TODO

class BlockCreator(object):
    """
    Given a sport, create a Block
    """

    class BlockScheduleExists(Exception): pass

    max_days_scheduled = 10

    def __init__(self, sport_day):
        self.sport_day = sport_day

    def create(self):
        """
        create the block and its block games from the SportDay instance information
        """

        block = Block.objects.create(site_sport=self.sport_day.site_sport,
                                     start=self.sport_day.the_datetime)

        #
        # create the BlockGames which are excluded from the schedule
        for game in self.sport_day.get_excluded_games():
            print('creating this excluded BlockGame...')
            print('    ', str(game))
            block_game = BlockGame()
            block_game.block = block
            block_game.name = game.get_home_at_away_str()
            block_game.srid = game.srid
            block_game.game = game
            block_game.save()

        #
        # create the BlockGames associated with this Block at the current time
        for game in self.sport_day.get_included_games():
            print('creating this included BlockGame...')
            print('    ', str(game))
            block_game = BlockGame()
            block_game.block = block
            block_game.name = game.get_home_at_away_str()
            block_game.srid = game.srid
            block_game.game = game
            block_game.save()

        return block

    # def get_game_data(self):
    #     """
    #     ScheduleDay has the data about the sports upcoming games
    #     """
    #     self.schedule_day.update()
    #     return self.schedule_day.data
    #
    # def create_upcoming_blocks(self):
    #     """
    #     update the next few days of the block schedule.
    #     if necessary, create new blocks.
    #     """
    #     game_data = self.get_game_data()
    #     for date_str, sport_day in game_data[:self.max_days_scheduled]:
    #         #
    #         # date_str is just a date string like: '2016-04-07', starting with tomorrow
    #         # sport_day is a sport specific instance of ScheduleDay.SportDay
    #         #           and has a method get_data() which contains information like this:
    #         #
    #
    #         # TODO if there is already a Block for this sport & day, go no further
    #         # potentially move this logic into the BlockScheduleManager
    #         # and just use this class to always create a block

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
            raise Exception('"block" is not a Block instance')

    def create(self):
        """
        perform the initial creation of all the BlockPrizeStructure(s)
        by giving the block every PrizeStructure from its
        sports DefaultPrizeStructure table
        """

        if BlockPrizeStructure.objects.filter(block=self.block).count() > 0:
            print('exiting... this block already created its default prize structures.')
            return

        for prize_structure in DefaultPrizeStructure.objects.filter(site_sport=self.block.site_sport):
            try:
                bps = BlockPrizeStructure()
                bps.block = self.block
                bps.prize_structure = prize_structure.prize_structure
                bps.save()

            except Exception as e:
                # couldnt create it, but maybe it already existed
                print(e)
                pass

class DefaultPrizeStructureManager(object):
    """
    manages each sports default set of prize structures.
    this is the templates from which all new blocks receive
    their BlockPrizeStructures.
    """

    default_buyin_amounts = [1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0]
    default_contest_sizes = [(2, 1), (10, 5), (10, 3)] # each tuple: (size, payouts)

    @staticmethod
    def create_initial_default_prize_structures():

        site_sport_manager = SiteSportManager()
        for sport in  SiteSportManager.SPORTS:
            created_default_prize_structures = 0
            site_sport = site_sport_manager.get_site_sport(sport)
            for buyin in DefaultPrizeStructureManager.default_buyin_amounts:
                for size, payout_spots in DefaultPrizeStructureManager.default_contest_sizes:
                    # get the prize structure based on the buyin and # of payout spots
                    prize_structures = PrizeStructure.objects.filter(generator__buyin=buyin,
                                                                     generator__payout_spots=payout_spots)
                    prize_structure = None # loop until we find it
                    for ps in prize_structures:
                        if size == ps.get_entries():
                            prize_structure = ps
                            break # we found it
                    if prize_structure is None:
                        err_msg = 'no PrizeStructure for buyin:', str(buyin), 'payout_spots', str(payout_spots)
                        print(err_msg)
                        print('... you can add them manually though!')
                        #raise Exception(err_msg)

                    else:
                        #
                        # create the default prize structures for the SiteSport
                        dps = DefaultPrizeStructure()
                        dps.site_sport = site_sport
                        dps.prize_structure = prize_structure
                        dps.save()
                        created_default_prize_structures += 1

            print(str(created_default_prize_structures), 'for', sport)
