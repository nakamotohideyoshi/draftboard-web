#
# draftgroup/classes.py

from django.db.transaction import atomic    # @atomic decorator for atomic transactions
from django.utils import timezone
from .models import DraftGroup, Player, GameTeam
from sports.models import SiteSport
from salary.models import Pool, Salary
from sports.classes import SiteSportManager
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

    def save_gameteam(self, draft_group, game, team, alias, start):
        """
        create and return a new draftgroup.models.GameTeam object
        """
        return GameTeam.objects.create( draft_group=draft_group,
                                            start=start,
                                            game_srid=game,
                                            team_srid=team,
                                            alias=alias )

    def save_player(self, draft_group, player, salary):
        """
        create and return a new draftgroup.models.Player object
        """
        return Player.objects.create( draft_group=draft_group,
                                      salary_player=player,
                                      salary=salary )

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
    def create(self, site_sport, start, end=None):
        """
        create and return a NEW draft group for the SiteSport
        which contains players included in games starting
        on or after the start time, and before the end time.

        :param site_sport:
        :param start:
        :param end:
        :return:
        """
        if not isinstance(site_sport, SiteSport):
            raise InvalidSiteSportTypeException('site_sport must be an instance of SiteSport')
        if not isinstance(start, datetime.datetime):
            raise InvalidStartTypeException('start must be a datetime object')

        # we will use the SiteSportManager to get the game_model and player_model below
        ssm = SiteSportManager()

        # method returns a Salary object from which we can
        #   - get_pool()  - get the salary.models.Pool
        #   - get_salaries() - get a list of salary.model.Salary (players w/ salaries)
        salary    = self.get_active_salary_pool(site_sport)

        draft_group = DraftGroup.objects.get_or_create(salary_pool=salary.get_pool(),
                                                        start=start, end=end )
        # get the game model for the site sport
        game_model = ssm.get_game_class(site_sport)

        # get all games equal to or greater than start, and less than end.
        games = game_model.objects.filter( start__gte=start, start__lt=end )

        # build lists of all the teams, and all the player srids in the draft group
        team_srids      = []
        for g in games:
            self.save_gameteam( draft_group, g.away.srid, g.away.alias, g.start )
            self.save_gameteam( draft_group, g.home.srid, g.home.alias, g.start )

            if g.away.srid not in team_srids: team_srids.append( g.away.srid )
            if g.home.srid not in team_srids: team_srids.append( g.home.srid )

        # get all the players in those games,
        # and create the draftgroup.models.Player objects
        player_model = ssm.get_player_class(site_sport)

        #
        # TODO - i need to add the Team to the sports.models.Player,
        #        or start parsing TeamRoster or something.... wow
        players = player_model.objects.filter()

        return draft_group

# easy usage:
# >>> from draftgroup.classes import manager
manager = DraftGroupManager()