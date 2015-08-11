#
# draftgroup/classes.py

from django.dispatch import receiver
import mysite.exceptions
from django.db.transaction import atomic
from .models import DraftGroup, Player, GameTeam
from sports.models import Game, SiteSport, GameStatusChangedSignal
from salary.models import Pool, Salary
from sports.classes import SiteSportManager
import datetime

# @receiver(signal=GameStatusChangedSignal.signal)
# def on_game_status_changed(sender, **kwargs):
#     print( 'on_game_status_changed' )


class AbstractDraftGroupManager(object):
    """
    Parent class for all DraftGroup common functionality.
    DraftGroups are used to define pools of players for a range of time,
    and these players have salary amounts which will not be changed
    after the creation of the DraftGroup.
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
            raise mysite.exceptions.SalaryPoolException('could not find active salary pool for given site_sport')

        pool = active_pools[0]
        salaried_players = Salary.objects.filter( pool=pool )
        return self.Salaries( pool, list(salaried_players) )

    def create_gameteam(self, draft_group, game, team, alias, start):
        """
        create and return a new draftgroup.models.GameTeam object
        """
        return GameTeam.objects.create( draft_group=draft_group,
                                            start=start,
                                            game_srid=game,
                                            team_srid=team,
                                            alias=alias )

    def create_player(self, draft_group, salary_player, salary, start):
        """
        create and return a new draftgroup.models.Player object
        """
        return Player.objects.create( draft_group=draft_group,
                                      salary_player=salary_player,
                                      salary=salary,
                                      start=start)

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

    @receiver(signal=GameStatusChangedSignal.signal)
    def on_game_status_changed(sender, **kwargs):
        print( 'on_game_status_changed' )
        # TODO
        #       1) get the draftgroups the kwargs.get('game') is contained in
        #       2) call the task that does stuff to those draftgroups.
        #
        # example:
        #
        #       mysite.tasks.live_game_status_changed( game=kwargs.get('game') )

    def get_for_site_sport(self, site_sport, start, end):
        """
        get the most recent draftgroup for the given site_sport

        :param site_sport:
        :return:
        """

        # return the most recently created draftgroup for the site_sport
        dgs = DraftGroup.objects.filter( salary_pool__site_sport=site_sport,
                                         start=start, end=end ).order_by('-created')
        if len(dgs) == 0:
            #
            # no matching draftgroups? create a new one! PlayerPool must exist
            return self.create(site_sport, start, end)
        else:
            #
            # otherwise, return the most recently created one
            return dgs[0]

    @atomic
    def create(self, site_sport, start, end):
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
            raise mysite.exceptions.InvalidSiteSportTypeException('site_sport param must be an instance of SiteSport')
        if not isinstance(start, datetime.datetime):
            raise mysite.exceptions.InvalidStartTypeException('start param must be a datetime object')
        if not isinstance(end, datetime.datetime):
            raise mysite.exceptions.InvalidEndTypeException('end param must be a datetime object')

        #
        # we will use the SiteSportManager the model class for player, game
        ssm             = SiteSportManager()
        game_model      = ssm.get_game_class(site_sport)

        # get all games equal to or greater than start, and less than end.
        games = game_model.objects.filter( start__gte=start, start__lt=end )
        if len(games) == 0:
            raise mysite.exceptions.NoGamesInRangeException('there are ZERO games in [%s until %s' % (start, end))

        # method returns a Salary object from which we can
        #   - get_pool()  - get the salary.models.Pool
        #   - get_salaries() - get a list of salary.model.Salary (players w/ salaries)
        salary    = self.get_active_salary_pool(site_sport)

        draft_group = DraftGroup.objects.create(salary_pool=salary.get_pool(),
                                                        start=start, end=end )

        #
        # build lists of all the teams, and all the player srids in the draft group
        team_srids      = {}
        for g in games:
            self.create_gameteam( draft_group, g.srid, g.away.srid, g.away.alias, g.start )
            self.create_gameteam( draft_group, g.srid, g.home.srid, g.home.alias, g.start )

            team_srids[g.away.srid]  = g.start
            team_srids[g.home.srid]  = g.start

        #
        # for each salaried player, create their draftgroup.models.Player
        # instance if their team is in the team srids list we generated above
        for p in salary.get_players():    # these 3 lines work but lets get rid of if statement
            if p.player.team.srid in team_srids:
                self.create_player(draft_group, p, p.amount, team_srids.get(p.player.team.srid))

        #
        return draft_group

# easy usage:
# >>> from draftgroup.classes import manager
manager = DraftGroupManager()