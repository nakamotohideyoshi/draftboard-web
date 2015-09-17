#
# draftgroup/classes.py

from django.dispatch import receiver
import mysite.exceptions
from .exceptions import EmptySalaryPoolException
from django.db.transaction import atomic
from .models import DraftGroup, Player, GameTeam
from sports.models import Game, SiteSport, GameStatusChangedSignal
from salary.models import Pool, Salary
from sports.classes import SiteSportManager
import datetime
from draftgroup.tasks import on_game_closed

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

    def get_draft_group(self, draft_group_id):
        """
        raises DraftGroup.DoesNotExist if the draft_group_id specified is not found
        """
        return DraftGroup.objects.get(pk = draft_group_id )

    def create_gameteam(self, draft_group, game, team, alias, start):
        """
        create and return a new draftgroup.models.GameTeam object
        """
        return GameTeam.objects.create( draft_group=draft_group,
                                            start=start,
                                            game_srid=game,
                                            team_srid=team,
                                            alias=alias )

    def create_player(self, draft_group, salary_player, salary, start, game_team):
        """
        create and return a new draftgroup.models.Player object
        """
        return Player.objects.create( draft_group=draft_group,
                                      salary_player=salary_player,
                                      salary=salary,
                                      start=start,
                                      game_team=game_team)

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
        #print( 'on_game_status_changed' )

        # get the game instance from the signal
        game = kwargs.get('game')

        if game.is_inprogress():
            #
            # this live game status just changed to inprogress
            dgm = DraftGroupManager()
            draft_groups = dgm.get_for_game( game )
            refund_task_results = []

        elif game.is_closed():
            #
            # the live game is all done getting stat updates. it was just closed.
            dgm = DraftGroupManager()
            draft_groups = dgm.get_for_game( game )

            results = []
            for draft_group in draft_groups:
                res = on_game_closed.delay( draft_group )
                # build list of tuples of (DraftGroup, task result) pairs
                results.append( (draft_group, res))
            # check results... ?

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

    def get_players(self, draft_group):
        """
        return a list of sports.<sport>.Player models who are in this DraftGroup

        :param draft_group:
        :return:
        """
        #ssm = SiteSportManager()
        return Player.objects.filter( draft_group=draft_group )

    def get_player_stats(self, draft_group):
        """
        get the sports.<sport>.models.PlayerStats objects for the given draft_group
        returned in a dictionary of:

            {
                <model name> : [ list of objects ],
                <model name> : [ list of objects ],
                ... etc...
            }

        :param draft_group:
        :return:
        """
        ssm = SiteSportManager()
        game_srids = [ x.game_srid for x in self.get_game_teams(draft_group=draft_group) ]
        player_stats_models = ssm.get_player_stats_class( sport=draft_group.salary_pool.site_sport )
        data = {}
        for stats_model in player_stats_models:
            for player_stat_obj in stats_model.objects.filter( srid_game__in=game_srids ):
                # l.append( player_stat_obj.to_json() )
                data[ player_stat_obj.player_id  ] = player_stat_obj.to_score()

        return data

    def get_game_teams(self, draft_group):
        """
        Return a QuerySet of the draftgroup.models.GameTeam objects
        for the draftgroup.

        Each GameTeam object has srids for the game, and for one of the teams.
        (So there will typically be one GameTeam for home, and one for away.)

        :param draftgroup: draftgroup.models.DraftGroup instance
        :return:
        """
        return GameTeam.objects.filter( draft_group=draft_group )

    def get_games(self, draft_group):
        """
        Return the sports.<sport>.Game objects of the DraftGroup instance.

        This method simply gets the distinct('game_srid') rows
        from the QuerySet returned by get_game_teams().

        :param draft_group:
        :return: QuerySet of sports.<sport>.Game objects
        """

        # get the distinct games from the gameteam model
        distinct_gameteam_games = self.get_game_teams( draft_group=draft_group ).distinct('game_srid')
        game_srids = [ x.game_srid for x in distinct_gameteam_games ]

        # get the sports game_model (ie: sports.<sport>.Game)
        ssm = SiteSportManager()
        game_model = ssm.get_game_class( sport=draft_group.salary_pool.site_sport )
        return game_model.objects.filter( srid__in=game_srids )

    def get_game_boxscores(self, draft_group):
        """
        Return the sports.<sport>.GameBoxscore objects related to the DraftGroup instance.

        This method simply gets the distinct('game_srid') rows
        from the QuerySet returned by get_game_teams().

        :param draft_group:
        :return: QuerySet of sports.<sport>.Game objects
        """

        # get the distinct games from the gameteam model
        distinct_gameteam_games = self.get_game_teams( draft_group=draft_group ).distinct('game_srid')
        game_srids = [ x.game_srid for x in distinct_gameteam_games ]

        # get the sports game_model (ie: sports.<sport>.Game)
        ssm = SiteSportManager()
        game_boxscore_model = ssm.get_game_boxscore_class( sport=draft_group.salary_pool.site_sport )
        return game_boxscore_model.objects.filter( srid_game__in=game_srids )

    def get_pbp_descriptions(self, draft_group, max=15):
        """
        get the most recent pbp descriptions for this draft group

        does not return the full list, but a capped (short) trailing history
        :param draft_group:
        :return:
        """

        # get the distinct games from the gameteam model
        distinct_gameteam_games = self.get_game_teams( draft_group=draft_group ).distinct('game_srid')
        game_srids = [ x.game_srid for x in distinct_gameteam_games ]

        # get the sports game_model (ie: sports.<sport>.Game)
        ssm = SiteSportManager()
        pbp_description_model = ssm.get_pbp_description_class( sport=draft_group.salary_pool.site_sport )
        #return pbp_description_model.objects.filter( description__srid_game__in=game_srids )[:15]
        return pbp_description_model.objects.filter( )[:15] # TODO

    def get_for_game(self, game):
        """
        return a list of all the DraftGroups which contain this Game

        :param game:
        :return: list of distinct DraftGroups objects which contain the specified Game
        """

        # get a list of GameTeam objects, with distinct DraftGroups
        distinct_draft_groups = GameTeam.objects.filter(game_srid=game.srid).distinct('draft_group')
        return [ x.draft_group for x in distinct_draft_groups ]

    def get_for_contest(self, contest):
        """
        Wrapper for method get_for_site_sport().
        Uses the contest site_sport, start, end properties to get DraftGroup

        :param contest:
        :return:
        """
        return self.get_for_site_sport( contest.site_sport, contest.start, contest.end )

    def create_for(self, contest):
        """
        wrapper for create( site_sport, start, end ) method
        which uses the contest's site_sport, start, and end
        for the creation of the draft_group

        Warning: this does NOT set the draft_group to the contest,
                    so dont assume that it does.

        :param contest:
        :return: DraftGroup instance
        """
        return self.create( contest.site_sport, contest.start, contest.end )

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
        salary          = self.get_active_salary_pool(site_sport)
        if len(salary.get_players()) <= 0:
            #
            # we dont want to allow a draft group without players!
            raise EmptySalaryPoolException()

        draft_group = DraftGroup.objects.create(salary_pool=salary.get_pool(),
                                                        start=start, end=end )

        #
        # build lists of all the teams, and all the player srids in the draft group
        team_srids      = {}
        game_teams      = {} # newly created game_team objects will need to be associated with draftgroup players
        for g in games:
            gt = self.create_gameteam( draft_group, g.srid, g.away.srid, g.away.alias, g.start )
            game_teams[ g.away.srid ] = gt
            gt = self.create_gameteam( draft_group, g.srid, g.home.srid, g.home.alias, g.start )
            game_teams[ g.home.srid ] = gt

            team_srids[g.away.srid]  = g.start
            team_srids[g.home.srid]  = g.start

        #
        # for each salaried player, create their draftgroup.models.Player
        # instance if their team is in the team srids list we generated above
        for p in salary.get_players():    # these 3 lines work but lets get rid of if statement
            if p.player.team.srid in team_srids:
                self.create_player(draft_group, p, p.amount,
                                   team_srids.get( p.player.team.srid ),
                                   game_teams[ p.player.team.srid ])

        #
        return draft_group
