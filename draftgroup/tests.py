#
# draftgroup/tests.py

from dataden.util.timestamp import DfsDateTimeUtil
from django.utils import timezone
from datetime import datetime, timedelta, time
from test.classes import AbstractTest
from test.models import GameChild
from mysite.exceptions import InvalidSiteSportTypeException, \
                                InvalidStartTypeException, InvalidEndTypeException, \
                                SalaryPoolException, NoGamesInRangeException
from draftgroup.classes import DraftGroupManager
from sports.models import SiteSport
from salary.dummy import Dummy as SalaryDummy

class DraftGroupManagerCreateParams(AbstractTest):

    def setUp(self):
        self.site_sport, created = SiteSport.objects.get_or_create(name='nfl')
        self.start              = timezone.now()        # a (timezone aware) datetime object
        self.end                = timezone.now()        # a (timezone aware) datetime object
        self.invalid_site_sport = 'invalidsitesport'
        self.invalid_start      = 1420000000 # int is invalid here
        self.invalid_end        = datetime.now().date() # invalid because just date() wont work!

    def test_draft_group_manager_create_invalid_site_sport(self):
        manager = DraftGroupManager()
        date_time = datetime.now()
        self.assertRaises(InvalidSiteSportTypeException,
                  lambda: manager.create(self.invalid_site_sport, self.start, self.end))

    def test_draft_group_manager_create_invalid_start(self):
        manager = DraftGroupManager()
        self.assertRaises(InvalidStartTypeException,
                  lambda: manager.create(self.site_sport, self.invalid_start, self.end ))

    def test_draft_group_manager_create_invalid_end(self):
        manager = DraftGroupManager()
        self.assertRaises(InvalidEndTypeException,
                  lambda: manager.create(self.site_sport, self.start, self.invalid_end ))

    def test_draft_group_manager_create_no_games_in_range_exception(self):
        manager = DraftGroupManager()
        #
        # create a start & end range that cant possibly have games in it
        start   = timezone.now()
        end     = start - timedelta(days=1) # subtract a day from start
        self.assertRaises(NoGamesInRangeException,
                  lambda: manager.create(self.site_sport, start, end ))

class DraftGroupManagerNoSalaryPool(AbstractTest):

    def setUp(self):
        self.site_sport, created = SiteSport.objects.get_or_create(name='sitesporttest')

    def test_draft_group_manager_create_salary_pool_exception(self):
        manager = DraftGroupManager()
        self.assertRaises(SalaryPoolException, lambda: manager.get_active_salary_pool(self.site_sport))

class DraftGroupCreate(AbstractTest):

    def setUp(self):
        """
        create the underlying objects like SiteSport instance
        and salary pool players to be able to create draft group
        """
        self.sport = 'test'  # doesnt HAVE to be a valid site_sport value though
        self.site_sport, created = SiteSport.objects.get_or_create(name=self.sport)

        # dummy.generate_salaries will use the current time
        # when it creates games, so lets capture the time now, and then after
        # it generates stuff to make sure we have a start & end range
        # that will include the games it created                                                                                             more
        now             = timezone.now()
        self.start      = DfsDateTimeUtil.create( now.date() - timedelta(days=1), time(0,0) )

        #
        # we MUST create games, players, teams, salary pool stuff:
        self.salary_generator = SalaryDummy.generate_salaries(sport=self.sport)
        #self.__print_games_in_db()

        # create end datetime after generate_salaries() is run
        self.end        = DfsDateTimeUtil.create( now.date() + timedelta(days=1), time(0,0) )

    def __print_games_in_db(self):
        print( 'GameChild instances in db...')
        for g in GameChild.objects.all():
            print( '    ', str(g), str(g.start) )

    def test_draftgroupmanager_create(self):
        """
        will fail if create() method returns None ! possible if no games, or no salary pool exists
        """
        dgm = DraftGroupManager()
        draft_group = dgm.create( self.site_sport, self.start, self.end )
        self.assertIsNotNone(draft_group)

