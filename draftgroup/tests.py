#
# draftgroup/tests.py

from django.utils import timezone   # for timezone.now()
from datetime import datetime
from test.classes import AbstractTest
from draftgroup.classes import InvalidSiteSportTypeException, \
                                InvalidStartTypeException,\
                                SalaryPoolException
from draftgroup.classes import DraftGroupManager
from sports.models import SiteSport
from salary.dummy import Dummy
from salary.models import Pool, Salary

class DraftGroupManagerCreateParams(AbstractTest):

    def setUp(self):
        self.site_sport         = SiteSport.objects.get_or_create(name='validsitesport')
        self.start              = timezone.now()        # a (timezone aware) datetime object
        self.invalid_site_sport = 'invalidsitesport'
        self.invalid_start      = datetime.now().date() # invalid because just date() wont work!

    def test_draft_group_manager_create_invalid_site_sport(self):
        manager = DraftGroupManager()
        date_time = datetime.now()
        self.assertRaises(InvalidSiteSportTypeException,
                  lambda: manager.create(self.invalid_site_sport, self.start))

    def test_draft_group_manager_create_invalid_start(self):
        manager = DraftGroupManager()
        self.assertRaises(InvalidSiteSportTypeException,
                  lambda: manager.create(self.site_sport, 1420000000))

class DraftGroupManagerNoSalaryPool(AbstractTest):

    def setUp(self):
        self.site_sport, created = SiteSport.objects.get_or_create(name='sitesporttest')

    def test_draft_group_manager_create_salary_pool_exception(self):
        manager = DraftGroupManager()
        self.assertRaises(SalaryPoolException, lambda: manager.get_active_salary_pool(self.site_sport))

class GroupCreationTest(AbstractTest):

    def setUp(self):
        #
        # creates dummy site_sport, players, games, playerstats,
        # salary config, pool and players. see: the world
        self.salary_generator = Dummy.generate_salaries(pool_active=True) # ensure we create an active pool
        self.site_sport = self.salary_generator.site_sport
        self.pool       = self.salary_generator.pool
        #print( 'created pool pk[%s]' % self.pool, 'with Dummy.generate_salaries()')

    def test_draft_group_manager_get_active_group_none_found(self):
        """
        a draft group for the current time should not exist in this test
        """
        now         = timezone.now()
        manager     = DraftGroupManager()
        draft_group = manager.get(pk=1)
        #
        self.assertIsNone( draft_group )

    def test_draft_group_manager_create(self):
        """
        create a draft group from the salary pool we created with Dummy.generate_salaries()
        """

        pools = Pool.objects.all()
        for p in pools:
            print( 'pk:', p.pk, 'active:', p.active )
        now         = timezone.now()
        manager     = DraftGroupManager()
        draft_group = manager.create(site_sport=self.site_sport, start=now)

