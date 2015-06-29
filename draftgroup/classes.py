#
# draftgroup/classes.py

from django.db.transaction import atomic    # @atomic decorator for atomic transactions
from django.utils import timezone
from .models import DraftGroup, Player
from sports.models import SiteSport
from salary.models import Pool, Salary
import datetime

class InvalidSiteSportTypeException(Exception):
    """ Exception - raised for an invalid site sport argument """
    pass

class InvalidStartTypeException(Exception):
    """ Exception - raised for an invalid start argument """
    pass

class SalaryPoolException(Exception):
    """ Exception - thrown in __init__ if there is no active salary pool """
    pass

class AbstractDraftGroupManager(object):
    """
    Parent class for all DraftGroup common functionality
    """

    class Salaries(object):
        """
        holds the salary.models.Pool, and a list of the salary.model.Player objects
        """
        def __init__(self, pool, players):
            self.pool       = pool
            self.players    = players

        def get_pool(self):
            return self.pool

        def get_players(self):
            return self.players

    def __init__(self):
        pass

    def get_active_salary_pool(self, site_sport):
        """
        Return a Salaries instance with the Pool and Salary objects.

        There _should_ only be one active per sport at a time, but
        just in case there are multiple, we are doing a filter()
        and using the most recently created active pool.

        If not pool exists for the given site_sport, raise SalaryPoolException
        """

        active_pools = Pool.objects.filter(site_sport=site_sport, active=True)
        if len(active_pools) == 0:
            raise SalaryPoolException('could not find active salary pool for given site_sport')

        pool = active_pools[0]
        salaried_players = Salary.objects.filter( pool=pool )
        return self.Salaries( pool, list(salaried_players) )

    def get_games_gte_start(self, start):
        """
        Get all the game objects for the date contained in start
        which start exactly on, or after the start time.
        """
        pass # TODO

class DraftGroupManager( AbstractDraftGroupManager ):
    """
    This class helps get or create a "draft group".

    A draft group is essentially a pool of players, who may or may not
    play, and accrue stats, in a game scheduled to take place
    on or after (but within the same day of games) a certain time.

    (Note: Contests will load the lists of players for users to draft teams.
     These lists of players will contain all the players from a draft
     group which the Contest was created with.)

    """

    def __init__(self):
        super().__init__()

    def get(self, pk):
        """
        Return the active draft group for the method arguments, or None if does not exist.

        'site_sport' is a sports.models.SiteSport
        'start' is a datetime object

        :param site_sport:
        :param start:
        :return:
        """
        return None # TODO - actually try to get one

    @atomic
    def create(self, site_sport, start):
        """
        create and return a NEW draft group for the SiteSport and start Datetime

        :param site_sport:
        :param start:
        :return:
        """
        if not isinstance(site_sport, SiteSport):
            raise InvalidSiteSportTypeException('site_sport must be an instance of SiteSport')
        if not isinstance(start, datetime.datetime):
            raise InvalidStartTypeException('start must be a datetime object')

        salaries    = self.get_active_salary_pool(site_sport)
        draft_group = DraftGroup.objects.create(salary_pool=salaries.get_pool(), start_dt=start)

        #
        # TODO - we need to add each Salary.player (a GFK to the sports.models.Player)
        #        who will play in the game on a day, on or after 'start' datetime
        #         TODO TODO TODO



        return draft_group

# easy usage:
# >>> from draftgroup.classes import manager
manager = DraftGroupManager()