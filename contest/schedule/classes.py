#
# contest/schedule/classes.py

from django.conf import settings
from pytz import timezone as pytz_timezone
from datetime import timedelta, datetime
from django.utils import timezone
from django.db.transaction import atomic
from django.db.models import Q
import contest.models
from draftgroup.classes import DraftGroupManager
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
)
from util.midnight import midnight

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

            on_or_off = ' Disabled '
            if self.schedule_model.enable:
                on_or_off = ' *Active* '

            print('')
            print('-----------------------------------------------------------------')
            print('%s  --  %s        %s [%s contests]' % (on_or_off,
                       str(self.schedule_model), str(self.now.date()), str(len(self.scheduled_contests))))
            print('-----------------------------------------------------------------')
            if not self.schedule_model.enable:
                return # dont bother trying or printing anything, get out of here!

            for stc in self.scheduled_contests:
                # get all created_contests, and make sure the multiplier
                # matches the count of everything returned by the filter
                created_contests = CreatedContest.objects.filter( day=self.now.date(),
                                                    scheduled_template_contest=stc )
                n = created_contests.count()
                if  n>0 and n == stc.multiplier:
                    print('    existing (%s):'%(str(n)), str(created_contests[0]))

                else:
                    # create all remaining contests to be created
                    for x in range(stc.multiplier - n):
                        self.create_scheduled_contest(stc)
                        print( '    created:', str(stc))

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
            print('utc_start:', str(utc_start), 'self.dst_offset_hours():', self.get_dst_offset_hours() )
            # utc_start           = utc_start + timedelta(hours=self.get_dst_offset_hours())
            # print('utc_start(after + dst):', str(utc_start))
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
                    continue

                #
                # allow_day_skipping is True at this point.
                # Try scheduling for the following days
                # until we find a day that works.
                print('allow_day_skipping == ', str(allow_day_skipping))
                for extra_days in range(1,self.MAX_SKIP_DAYS+1):  # ie: [1,2,3,4,5,6]
                    #
                    try:
                        sc = self.Schedule( sched, dt = dt + timedelta(days=extra_days) )
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

