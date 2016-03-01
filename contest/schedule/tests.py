#
# contest/schedule/tests.py

from django.db.utils import IntegrityError
from django.utils import timezone
from datetime import datetime, date, time, timedelta
from test.classes import AbstractTest
from sports.classes import SiteSportManager
from prize.classes import CashPrizeStructureCreator
from salary.dummy import Dummy # only to be used for testing
from contest.models import Contest
from contest.schedule.classes import ScheduleManager
from contest.schedule.exceptions import ScheduleException, ScheduleOutOfRangeException
from contest.schedule.models import (
    Category,
    Schedule,
    TemplateContest,
    ScheduledTemplateContest,
    CreatedContest,
    Interval,
)

class ScheduleManagerTest(AbstractTest):
    """
    test the scheduling system. (primarily the object ScheduleManager)
    """

    def setUp(self):

        #
        #
        self.verbose = True  # set to False to disable print statements

        #
        # The sport we are going to build fake stats for.
        # Lets use nfl, but it doesnt matter what sport we use
        self.sport = 'nfl'

        #
        # Ensure there are Games by using the Dummy to generate fake stats.
        # The ScheduleManager requires that Game objects exist
        # because when it creates scheduled Contest objects
        # it is required to create a draft group.
        self.dummy = Dummy(sport=self.sport)
        self.dummy.generate()

        self.site_sport = self.dummy.site_sport # stash the site_sport for easy use

        self.site_sport_manager  = SiteSportManager()
        self.game_model          = self.site_sport_manager.get_game_class(self.site_sport)  #ie: sports.nfl.models.Game
        self.games               = self.game_model.objects.all() # there should be handful now, for today

        #
        # The only thing the Dummy object doesnt do is create
        # Game objects for tomorrow. It only creates them for today (in the near future).
        # We will need to do generate games for something like 10 days into the future
        # for testing purposes.
        #
        # Note that the ScheduleManager object can not schedule
        # contests which are more than 1 week in the future.
        self.days_with_games = 3
        for days_into_the_future in range(0, self.days_with_games):    # 1 thru 3 inclusive
            list_ids = [ g.pk for g in self.games ]
            db_games = self.game_model.objects.filter( pk__in=list_ids ).order_by('-start')
            self.__clone_games_for_day( db_games, days_into_the_future )

        # debug only -- show some of the cloning of the games we've done for extra games in the future
        if self.verbose:
            print('')
            print('its currently: ', timezone.now())
            print('dummy data generated for [%s]:' % str(self.site_sport))
            print('    (%s) games created today' % self.games.count())
            for game in self.games:
                print('        ', str(game))
            print('--------------------------------------------------------')
            all_games = self.game_model.objects.all()
            print('    (%s) games after we cloned more days worth of games!' % str(all_games.count()) )
            for game in all_games:
                print('        ', str(game))

        # build a list of PrizeStructure objects
        self.prize_structures = self.__build_prize_structures([1.00, 5.00, 10.00]) # heads-ups only

        # get a Category
        self.category = self.__get_or_create_category('heads-up')

        # get a Schedule
        self.schedule = self.__get_or_create_schedule(self.site_sport, self.category)

        # get a TemplateContest
        prize_structure = self.prize_structures[0]      # first prize_structure in the list
        max_entries     = 1                             # user lineup limit
        entries         = 2                             # contest lineup limit
        name            = prize_structure.name
        self.template_contest = self.__create_template_contest(prize_structure,
                                                max_entries, entries, name=name, site_sport=None,
                                                gpp=False,
                                                respawn=True,
                                                doubleup=False)

        # get an Interval
        # self.interval  = self.__get_or_create_interval(mon=False, wed=False) # disable specific days
        self.interval   = self.__get_or_create_interval() # all days enabled by default!

        #
        # At this point we have everything we need to be able to create a ScheduledTemplateContest
        # and then we can run the ScheduleManager!
        # ... go test it

    def __clone_games_for_day(self, games, days_offset):
        """
        Create the same set of games on day that is 'days_offset' in the future.
        We will need to change the games global id to ensure it can be saved in the db.

        :param games: QuerySet of sports.<sport>.models.Game objects
        :param days_offset: integer days offset from now. (ie: days_offset=1  would be tomorrow)
        :return: None
        """

        game_start_on_15 = None
        # its ordered desecending, so the first game
        # on the quarter hour, is the highest time on a :15
        for g in games:
            if g.start.time().minute % 15 == 0:
                print(str(g), str(g.start))
                game_start_on_15 = g
                break
            else:
                print(str(g), 'not on the :15')
        game_id = game_start_on_15.pk
        #
        td_day_offset = timedelta(days=days_offset)
        td = timedelta(minutes=15)
        tmp_start = game_start_on_15.start
        for x in range(1, 25):
            g.pk    = None
            g.start = tmp_start + timedelta(days=days_offset) + timedelta(minutes=15 * x)

            # add a days worth of seconds to the 'srid', which is a unix timestamp
            g.srid  = str(int(g.srid) + (days_offset * 60 * 60 * 24) + (15*60*x))
            g.save()

    def __build_prize_structures(self, values):
        """
        generate 1v1 (headsup) prize structures for each amount in the values list
        :param values: list of floats
        :return:
        """
        prize_structures = []
        for amount in values:
            ps = CashPrizeStructureCreator(name='$%.2f HU'%amount)      # name it
            ps.set_buyin( amount )                                          # buyin is $1.00
            ps.add( 1, (amount*2.0) - (amount*2.0*0.1) )                                           # 1st pays out $1.80
            ps.save()
            prize_structures.append( ps.prize_structure )
        # return the newly created list
        return prize_structures

    def __get_or_create_category(self, name):
        """
        helper to get or create a schedule.models.Category

        :param name:  whatever we want to name this category (ie: "heads-up")
        :return: contest.schedule.models.Category
        """
        category, created = Category.objects.get_or_create(name=name)
        return category

    def __get_or_create_schedule(self, site_sport, category, enable=True):
        """
        helper to get or create a Schedule object

        :param site_sport:  the SiteSport this Schedule is associated with
        :param category:    the Category this Schedule is associated with
        :param enable:      indicates whether this Schedule is active
        :return:  contest.schedule.models.Schedule
        """
        schedule, created = Schedule.objects.get_or_create(site_sport=site_sport,
                                                 category=category, enable=enable)
        return schedule

    def __create_template_contest(self, prize_structure, max_entries, entries,
                                    name='', site_sport=None,
                                    gpp=False, respawn=False, doubleup=False):
        """
        Build a TemplateContest which the scheduler will use to make real ones!

        It uses the internally set self.site_sport by default

        :param prize_structure:
        :param max_entries:         number of lineups from single user limit
        :param entries:             number of lineups in total for contest
        :param name:
        :param site_sport:
        :param gpp:                 boolean - indicates Guaranteed prize pool
        :param respawn:             boolean - indicates if this contest respawns
        :param doubleup:            boolean - indicates if this contest is a double up
        :return:                    contest.schedule.models.TemplateContest
        """
        ss = site_sport
        if ss is None:
            ss = self.site_sport

        template_contest                    = TemplateContest()
        template_contest.site_sport         = ss
        template_contest.name               = name      # this will be the public name once cloned!
        template_contest.prize_structure    = prize_structure
        template_contest.max_entries        = max_entries
        template_contest.entries            = entries
        template_contest.gpp                = gpp
        template_contest.respawn            = respawn
        template_contest.doubleup           = doubleup

        # TemplateContest objects 'start' & 'end' properties are un-used and can be set to anything!
        template_contest.start              = timezone.now()
        template_contest.end                = timezone.now() + timedelta(seconds=1)

        template_contest.save()     # create/commit the new object
        return template_contest

    def __get_or_create_interval(self, mon=True, tue=True, wed=True, thu=True, fri=True, sat=True, sun=True):
        """
        each argument is a boolean which represents whether that day is enabled

        :param mon:
        :param tue:
        :param wed:
        :param thu:
        :param fri:
        :param sat:
        :param sun:
        :return:       contest.schedule.models.Interval object
        """
        interval, created = Interval.objects.get_or_create(monday=mon,
                                                           tuesday=tue,
                                                           wednesday=wed,
                                                           thursday=thu,
                                                           friday=fri,
                                                           saturday=sat,
                                                           sunday=sun)
        return interval

    def __create_scheduled_template_contest(self, schedule, template_contest, start_time,
                                                 duration_minutes, interval, multiplier=1):
        """
        create a ScheduledTemplateContest -- this is an entry in the database
        which (if its Schedule parent is active) indicates to the system
        that a live Contest matching the ScheduledTemplateContest.start_time
        should be created on the days in the TemplateContest.interval

        :param schedule:
        :param template_contest:
        :param start_time: the datetime.time() object for when this contest should start, on days in its interval
        :param duration_minutes: so we can calculate the end time. (its: start_time + duration_minutes)
        :param interval: which days we should create the contest on
        :param multiplier: the # of contests to create for this template
        :return:
        """
        scheduled_template_contest                  = ScheduledTemplateContest()
        scheduled_template_contest.schedule         = schedule
        scheduled_template_contest.template_contest = template_contest
        scheduled_template_contest.start_time       = start_time
        scheduled_template_contest.duration_minutes = duration_minutes
        scheduled_template_contest.interval         = interval
        scheduled_template_contest.multiplier       = multiplier
        scheduled_template_contest.save()
        return scheduled_template_contest

    def test_single_scheduled_template_contest_today(self):
        """
        Get an interval that includes all days, and make sure the ScheduleManager
        create the Contest for the ScheduledTemplateContest

        :return:
        """

        def run_schedule(scheduled_template_contest, expected_created_contests, expected_contests, time_delta=None):
            # get an instance of ScheduleManager and run() should create this
            sm = ScheduleManager()
            sm.run(time_delta=time_delta)

            # ensure the proper number of CreatedContest entries exist
            self.assertEquals( CreatedContest.objects.all().count(), expected_created_contests )
            # ensure the expected number of resulting Contest objects exist
            self.assertEquals( Contest.objects.all().count(), expected_contests )

        # get a ScheduledTemplateContest (hooks up a TemplateContest with an Interval)
        # since the Dummy object will create games for current time,
        # set the start time to 12:00 AM and set the duration for 24*60 minutes (one whole day in minutes)

        # *** update ***
        # the contest start time MUST exactly match a Game's 'start' datetime !
        plus_30_min = timezone.now()+timedelta(minutes=30)
        games = self.game_model.objects.filter(start__gt=plus_30_min).order_by('start') # ascending
        if games.count() <= 0:
            msg = 'ScheduleManagerTest.test_single_scheduled_template_contest_today: '
            msg += 'there were no upcoming games to target'
            #print(msg)
            raise Exception(msg)

        start_time          = games[0].start.time()
        print('game start for scheduled_template_contest:', str(start_time))
        duration_minutes    = 24 * 60
        multiplier          = 1
        scheduled_template_contest = self.__create_scheduled_template_contest(self.schedule,
                                                                              self.template_contest,
                                                                              start_time,
                                                                              duration_minutes,
                                                                              self.interval,
                                                                              multiplier=multiplier)

        st_time_str = str(scheduled_template_contest.start_time)
        print('after creating, scheduled_template_contest.start_time:', str(st_time_str))
        # before we run - none of these models should have any results
        self.assertEquals( CreatedContest.objects.all().count(), 0 )
        self.assertEquals( Contest.objects.all().count(), 0 )

        # after the first run(), 1 CreatedContest and 1 new Contest should exist
        run_schedule(scheduled_template_contest, 1, 1 )

        # calling run() again does not create more, because its already been created for the day
        run_schedule(scheduled_template_contest, 1, 1 )

        #
        # now changing the multiplier, and run() again.
        # there should be more CreatedContests and Contests
        scheduled_template_contest.multiplier = 5
        scheduled_template_contest.save()
        run_schedule(scheduled_template_contest, 5, 5 )

        #
        #########################################################################
        # now run the schedule for tomorrow ...
        #########################################################################

        # first run for the next day should result in more
        run_schedule(scheduled_template_contest, 10, 10, timedelta(days=1) )
        # and the same run again should not have any more created
        run_schedule(scheduled_template_contest, 10, 10, timedelta(days=1) )

        #
        #########################################################################
        # ensure we cant add a duplicate TemplateContest at the same time
        #########################################################################
        # self.assertRaises( IntegrityError,
        #     lambda: self.__create_scheduled_template_contest(self.schedule,
        #          self.template_contest, start_time, duration_minutes, self.interval, multiplier=3) )

        # now make sure we can create it at a different time on the same day
        new_start_time = time( start_time.hour, start_time.minute + 15 )
        stc_same_day_different_time = self.__create_scheduled_template_contest(self.schedule,
                 self.template_contest, new_start_time, duration_minutes, self.interval, multiplier=3)

        # should be a second ScheduledTemplateContest now !
        self.assertEquals( ScheduledTemplateContest.objects.all().count(), 2 )

        # and run the scheduler again on the current day
        run_schedule(scheduled_template_contest, 13, 13 )

        #
        #########################################################################
        # make sure ScheduleManager.run() throws ScheduleException if out of range
        #########################################################################
        too_many_days_in_future = 7   # if today is monday, 7 is the NEXT monday which is invalid
        sm = ScheduleManager()
        self.assertRaises( ScheduleOutOfRangeException,
                lambda: sm.run( time_delta=timedelta(days=too_many_days_in_future) ) )

        #
        #########################################################################
        # ensure ScheduleException raised when 0 games for the scheduled contest
        #########################################################################
        day_without_games = self.days_with_games + 1
        # however, day_without_games must be <= 6 too!
        if day_without_games > 6:
            raise Exception('fix it so day_without_games is <= 6... it was %s' % str(day_without_games))

        #
        # this is a case where our timedelta is in the valid range,
        # but nothing is created because an internal exception is caught
        # when there are no games to create contests for (ie: DraftGroup cant be created)
        #run_schedule(scheduled_template_contest, 13, 13, timedelta(days=day_without_games) )