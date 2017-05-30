import datetime
from logging import getLogger

from django.contrib.contenttypes.models import ContentType
from django.db.transaction import atomic
from django.dispatch import receiver
from django.utils import timezone

import mysite.exceptions
from draftgroup.tasks import on_game_closed
from roster.models import RosterSpotPosition
from salary.models import Pool, Salary
from salary.tasks import clear_salary_locked_flags_for_draftgroup
from sports.classes import SiteSportManager
from sports.models import SiteSport, GameStatusChangedSignal
from .exceptions import (
    EmptySalaryPoolException,
    NotEnoughGamesException,
    NoGamesAtStartTimeException,
    FantasyPointsAlreadyFinalizedException,
)
from .models import (
    DraftGroup,
    UpcomingDraftGroup,  # proxy model which limits DraftGroup models to upcoming only
    Player,
    GameTeam,
    PlayerUpdate,
    GameUpdate,
)

logger = getLogger('draftgroup.classes')


class AbstractDraftGroupManager(object):
    """
    Parent class for all DraftGroup common functionality.
    DraftGroups are used to define pools of players for a range of time,
    and these players have salary amounts which will not be changed
    after the creation of the DraftGroup.
    """

    class DuplicateTeamInRangeException(Exception):
        pass

    class Salaries(object):
        """
        holds the salary.models.Pool, and a list of the salary.model.Player objects
        """

        def __init__(self, pool, players):
            self.pool = pool
            self.players = players

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
        valid_positions = []
        for rsp in RosterSpotPosition.objects.filter(roster_spot__site_sport=site_sport):
            rsp_name = rsp.position.name
            if rsp_name not in valid_positions:
                valid_positions.append(rsp_name)

        active_pools = Pool.objects.filter(site_sport=site_sport, active=True)
        if len(active_pools) == 0:
            raise mysite.exceptions.SalaryPoolException(
                'could not find active salary pool for given site_sport')

        pool = active_pools[0]
        players = []
        salaried_players = Salary.objects.filter(pool=pool)
        # remove players not on active roster
        for sp in salaried_players:
            logger.info('is position.name[%s] in valid_positions[%s]' % (
                sp.player.position.name, valid_positions))
            if sp.player.position.name not in valid_positions:
                continue  # ignore players who cant fit on the roster anyways.
            if sp.player.on_active_roster == True:
                players.append(sp)
                logger.info('player count: %s. Added player: %s' % (len(players), sp))
            else:
                logger.info('didnt add player')
        # return active players
        return self.Salaries(pool, list(players))

    @staticmethod
    def get_draft_group(draft_group_id):
        """
        raises DraftGroup.DoesNotExist if the draft_group_id specified is not found
        """
        return DraftGroup.objects.get(pk=draft_group_id)

    @staticmethod
    def create_gameteam(draft_group, game, team, alias, start):
        """
        create and return a new draftgroup.models.GameTeam object
        """
        return GameTeam.objects.create(draft_group=draft_group,
                                       start=start,
                                       game_srid=game,
                                       team_srid=team,
                                       alias=alias)

    @staticmethod
    def create_player(draft_group, salary_player, salary, start, game_team):
        """
        create and return a new draftgroup.models.Player object
        """
        return Player.objects.create(draft_group=draft_group,
                                     salary_player=salary_player,
                                     salary=salary,
                                     start=start,
                                     game_team=game_team)


class DraftGroupManager(AbstractDraftGroupManager):
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
        # print( 'on_game_status_changed' )

        # get the game instance from the signal
        game = kwargs.get('game')

        if game.is_inprogress():
            #
            # this live game status just changed to inprogress
            dgm = DraftGroupManager()
            draft_groups = dgm.get_for_game(game)
            refund_task_results = []

        elif game.is_closed():
            #
            # the live game is all done getting stat updates. it was just closed.
            dgm = DraftGroupManager()
            draft_groups = dgm.get_for_game(game)

            results = []
            for draft_group in draft_groups:
                res = on_game_closed.delay(draft_group)
                # build list of tuples of (DraftGroup, task result) pairs
                results.append((draft_group, res))
                # check results... ?

    @atomic
    def update_final_fantasy_points(self, draft_group_id, scorer_class=None):
        """
        updates the final_fantasy_points for all players in the draft group

        :param draft_group_id:
        :param scorer_class: gives the caller ability to override the scoring class used to calc fantasy points
        :return:
        """

        # get the draft group and then get its players
        draft_group = self.get_draft_group(draft_group_id)
        logger.info("Updating final fantasy points for %s" % draft_group)

        # check if the draft_group has already finalized fantasy_points...
        if draft_group.fantasy_points_finalized is not None:
            err_msg = 'draft_group id: %s' % draft_group_id
            raise FantasyPointsAlreadyFinalizedException(err_msg)

        # get the site sport, and the draft group players
        site_sport = draft_group.salary_pool.site_sport
        players = self.get_players(draft_group)

        # get all the PlayerStats objects for this draft group
        ssm = SiteSportManager()
        # print('ssm.get_score_system_class( %s ):' % str(site_sport))

        if scorer_class is None:
            salary_score_system_class = ssm.get_score_system_class(site_sport)
        else:
            salary_score_system_class = scorer_class

        score_system = salary_score_system_class()
        game_srids = [x.game_srid for x in self.get_game_teams(draft_group=draft_group)]
        game_srids = list(
            set(game_srids))  # itll have the same games twice. this removes duplicates

        # get the PlayerStats model(s) for the sport.
        # and get an instance of the sports scoring.classes.<Sport>SalaryScoreSystem
        # to determine which player stats models to use to retrieve the final fantasy_points from!
        for draft_group_player in players:
            # get the sports.<sport>.player  -- we'll need it later
            sport_player = draft_group_player.salary_player.player
            # determine the PlayerStats class to retrieve the fantasy_points from
            player_stats_class = score_system.get_primary_player_stats_class_for_player(
                sport_player)

            try:
                # Find the player's stats for this draft group.
                player_stats = player_stats_class.objects.get(srid_game__in=game_srids,
                                                              srid_player=sport_player.srid)
            # except player_stats_class.MultipleObjectsReturned as e1:
            #     # print('site_sport:', str(site_sport))
            #     # print('game_srids:', str(game_srids))
            #     # print('sport_player.srid:', str(sport_player.srid))
            #     # raise Exception('testing MultipleObjectsReturned issue')
            #
            #     #
            #     # raise an exception that will let us troubleshoot the draft group range...
            #     # because the draft group probably has too wide of a range
            #     # but it never should have let us create it then!
            #     err_msg = 'original exception[%s]' % str(e1)
            #     err_msg += ''
            #     raise self.StartEndRangeException(err_msg)

            except player_stats_class.DoesNotExist:
                logger.warning("PlayerStats can't be found for: %s" % sport_player)
                logger.info('game_srids: %s' % game_srids)
                logger.info('sport_player.srid: %s' % sport_player.srid)
                player_stats = None
                continue

            # move the current fantasy_points from the player_stats into
            # the draft_group_player and save it!
            logger.info('Setting %s to %s' % (draft_group_player, player_stats))
            draft_group_player.final_fantasy_points = player_stats.fantasy_points
            draft_group_player.save()

        #
        # set the datetime for when we finalized the draft_group players fantasy points
        draft_group.fantasy_points_finalized = timezone.now()
        draft_group.save()
        logger.info("Done updating final fantasy points for %s" % draft_group)

    def get_for_site_sport(self, site_sport, start, end):
        """
        get the most recent draftgroup for the given site_sport

        :param site_sport:
        :return:
        """

        # return the most recently created draftgroup for the site_sport
        dgs = DraftGroup.objects.filter(
            salary_pool__site_sport=site_sport,
            start=start, end=end
        ).order_by('-created')

        if len(dgs) == 0:
            #
            # no matching draftgroups? create a new one! PlayerPool must exist
            return self.create(site_sport, start, end)
        else:
            #
            # otherwise, return the most recently created one
            return dgs[0]

    @staticmethod
    def get_players(draft_group):
        """
        return a list of sports.<sport>.Player models who are in this DraftGroup

        :param draft_group:
        :return:
        """
        # ssm = SiteSportManager()
        return Player.objects.filter(draft_group=draft_group).select_related('salary_player')

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
        game_srids = [x.game_srid for x in self.get_game_teams(draft_group=draft_group)]
        player_stats_models = ssm.get_player_stats_class(sport=draft_group.salary_pool.site_sport)
        data = {}

        # fill with 0s for every player in the draft group first
        for stats_model in player_stats_models:
            for draft_group_player in Player.objects.filter(
                    draft_group=draft_group).prefetch_related('salary_player__player__position'):
                data[draft_group_player.player_id] = {
                    stats_model.field_id: draft_group_player.player_id,
                    stats_model.field_fp: 0.0,
                    stats_model.field_pos: draft_group_player.position,
                }

        # then add the stats for the existing player stats objects
        for stats_model in player_stats_models:
            for player_stat_obj in stats_model.objects.filter(srid_game__in=game_srids):
                # l.append( player_stat_obj.to_json() )
                data[player_stat_obj.player_id] = player_stat_obj.to_score()

        return data

    @staticmethod
    def get_game_teams(draft_group):
        """
        Return a QuerySet of the draftgroup.models.GameTeam objects
        for the draftgroup.

        Each GameTeam object has srids for the game, and for one of the teams.
        (So there will typically be one GameTeam for home, and one for away.)

        :param draft_group: draftgroup.models.DraftGroup instance
        :return:
        """
        return GameTeam.objects.filter(draft_group=draft_group)

    def get_games(self, draft_group):
        """
        Return the sports.<sport>.Game objects of the DraftGroup instance.

        This method simply gets the distinct('game_srid') rows
        from the QuerySet returned by get_game_teams().

        :param draft_group:
        :return: QuerySet of sports.<sport>.Game objects
        """

        # get the distinct games from the gameteam model
        distinct_gameteam_games = self.get_game_teams(draft_group=draft_group).distinct('game_srid')
        game_srids = [x.game_srid for x in distinct_gameteam_games]

        # get the sports game_model (ie: sports.<sport>.Game)
        ssm = SiteSportManager()
        game_model = ssm.get_game_class(sport=draft_group.salary_pool.site_sport)
        return game_model.objects.filter(srid__in=game_srids)

    def get_game_boxscores(self, draft_group):
        """
        Return the sports.<sport>.GameBoxscore objects related to the DraftGroup instance.

        This method simply gets the distinct('game_srid') rows
        from the QuerySet returned by get_game_teams().

        :param draft_group:
        :return: QuerySet of sports.<sport>.Game objects
        """

        # get the distinct games from the gameteam model
        distinct_gameteam_games = self.get_game_teams(draft_group=draft_group).distinct('game_srid')
        game_srids = [x.game_srid for x in distinct_gameteam_games]

        # get the sports game_model (ie: sports.<sport>.Game)
        ssm = SiteSportManager()
        game_boxscore_model = ssm.get_game_boxscore_class(sport=draft_group.salary_pool.site_sport)
        return game_boxscore_model.objects.filter(srid_game__in=game_srids)

    def get_pbp_descriptions(self, draft_group, max=15):
        """
        get the most recent pbp descriptions for this draft group

        does not return the full list, but a capped (short) trailing history
        :param draft_group:
        :return:
        """

        # get the distinct games from the gameteam model
        distinct_gameteam_games = self.get_game_teams(draft_group=draft_group).distinct('game_srid')
        game_srids = [x.game_srid for x in distinct_gameteam_games]

        # get the sports game_model (ie: sports.<sport>.Game)
        ssm = SiteSportManager()
        pbp_description_model = ssm.get_pbp_description_class(
            sport=draft_group.salary_pool.site_sport)
        # return pbp_description_model.objects.filter( description__srid_game__in=game_srids )[:15]
        return pbp_description_model.objects.filter()[:15]

    @staticmethod
    def get_for_game(game):
        """
        return a list of all the DraftGroups which contain this Game

        :param game:
        :return: list of distinct DraftGroups objects which contain the specified Game
        """

        # get a list of GameTeam objects, with distinct DraftGroups
        distinct_draft_groups = GameTeam.objects.filter(game_srid=game.srid).distinct('draft_group')
        return [x.draft_group for x in distinct_draft_groups]

    def get_for_contest(self, contest):
        """
        Wrapper for method get_for_site_sport().
        Uses the contest site_sport, start, end properties to get DraftGroup

        :param contest:
        :return:
        """
        return self.get_for_site_sport(contest.site_sport, contest.start, contest.end)

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
        return self.create(contest.site_sport, contest.start, contest.end)

    @staticmethod
    def find_games_within_time_span(site_sport, start, end):
        #
        # we will use the SiteSportManager the model class for player, game
        ssm = SiteSportManager()
        game_model = ssm.get_game_class(site_sport)
        # get all games equal to or greater than start, and less than end.
        games = game_model.objects.filter(
            start__gte=start, start__lte=end
        ).order_by('start')

        if len(games) == 0:
            err_msg = 'there are ZERO games in [%s until %s]' % (start, end)
            raise mysite.exceptions.NoGamesInRangeException(err_msg)
        elif len(games) < 2:
            raise NotEnoughGamesException()

        #
        # throw an exception if the specified start time does not coincide with any games
        if game_model.objects.filter(start=start).count() == 0:
            raise NoGamesAtStartTimeException()

        # Keep track of teams that are playing today.
        team_srids = []
        for game in games:
            # make sure we do not encounter the same team multiple times!
            for check_team in [game.away, game.home]:
                if check_team.srid in team_srids:
                    logger.warning("Excluding doubleheader game: %s" % game)
                    # If we find a game that has a team that is already playing today,
                    # exclude the second game.
                    games = games.exclude(pk=game.pk)

            # Add the teams to our list of srids.
            team_srids.append(game.away.srid)
            team_srids.append(game.home.srid)

        return games

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
            raise mysite.exceptions.InvalidSiteSportTypeException(
                'site_sport param must be an instance of SiteSport')
        if not isinstance(start, datetime.datetime):
            raise mysite.exceptions.InvalidStartTypeException(
                'start param must be a datetime object')
        if not isinstance(end, datetime.datetime):
            raise mysite.exceptions.InvalidEndTypeException('end param must be a datetime object')

        logger.info('Creating DraftGroup for sport: %s | start: %s | end: %s' % (
            site_sport, start, end))

        games = self.find_games_within_time_span(site_sport, start, end)

        # method returns a Salary object from which we can
        #   - get_pool()  - get the salary.models.Pool
        #   - get_salaries() - get a list of salary.model.Salary (players w/ salaries)
        salary = self.get_active_salary_pool(site_sport)
        if len(salary.get_players()) <= 0:
            #
            # we dont want to allow a draft group without players!
            raise EmptySalaryPoolException()

        # Create the draft group.
        draft_group = DraftGroup.objects.create(
            salary_pool=salary.get_pool(),
            start=start,
            end=end,
            num_games=0
        )

        # build lists of all the teams, and all the player srids in the draft group
        game_srids = {}
        team_srids = {}
        # newly created game_team objects will need to be associated with draftgroup players
        game_teams = {}
        for g in games:
            # add each game srid as a key, using the game itself as the value
            game_srids[g.srid] = g

            # make sure we do not encounter the same team multiple times!
            for check_team in [g.away, g.home]:
                if check_team.srid in team_srids:
                    err_msg = '%s, srid: %s' % (str(check_team), str(check_team.srid))
                    err_msg += '  range[ start:%s  end:%s ]' % (str(start), str(end))
                    raise self.DuplicateTeamInRangeException(err_msg)

            # create the GameTeam objects
            gt = self.create_gameteam(draft_group, g.srid, g.away.srid, g.away.alias, g.start)
            game_teams[g.away.srid] = gt
            gt = self.create_gameteam(draft_group, g.srid, g.home.srid, g.home.alias, g.start)
            game_teams[g.home.srid] = gt

            team_srids[g.away.srid] = g.start
            team_srids[g.home.srid] = g.start

        # for each salaried player, create their draftgroup.models.Player
        # instance if their team is in the team srids list we generated above
        for p in salary.get_players():
            if p.player.team.srid in team_srids:
                self.create_player(draft_group, p, p.amount,
                                   team_srids.get(p.player.team.srid),
                                   game_teams[p.player.team.srid])

        draft_group.num_games = len(games)
        draft_group.category = DraftGroup.DEFAULT_CATEGORY
        draft_group.save()
        draft_group.refresh_from_db()

        logger.info('Created DraftGroup: %s' % draft_group)

        # Unlock all player's salaries from this draft group.
        clear_salary_locked_flags_for_draftgroup.delay(draft_group=draft_group)

        # #
        # # as a final step, signal that this DraftGroup
        # # can have any relevant GameUpdates created
        # try:
        #     sport = draft_group.salary_pool.site_sport.name # ie: 'mlb', or 'nfl', etc...
        #     sig = CheckForGameUpdatesSignal(
        #           draft_group.pk, sport, game_srids=list(game_srids.keys()))
        #     sig.send()
        # except Exception as e:
        #     print('unable to send CheckForGameUpdatesSignal, skipping...')

        #
        return draft_group


class AbstractUpdateManager(object):
    class CategoryException(Exception):
        pass

    class TypeException(Exception):
        pass

    class ValueException(Exception):
        pass

    class PlayerDoesNotExist(Exception):
        pass

    def __init__(self):
        self.players_not_found = None

    def add(self, update_id, category, type, value,
            status, source_origin, url_origin, **kwargs):
        """
        create or update a PlayerUpdate

        *this method DOES NOT CALL .save() on the model, letting the subclasses do that.

        :param update_id:
        :param category:
        :param type:
        :param value:
        :return:
        """

        self.validate_update_id(update_id)
        self.validate_category(category)
        self.validate_type(type)
        self.validate_value(value)

        # parse and return a datetime object representing the publish time
        updated_at = kwargs.get('published_at')
        if updated_at is None:
            updated_at = timezone.now()

        created = False
        try:
            update = self.model.objects.get(update_id=update_id)
        except self.model.DoesNotExist:
            update = self.model()
            update.update_id = update_id
            created = True

        update.category = category
        update.type = type

        fields = ['updated_at', 'status', 'source_origin', 'url_origin', 'value']
        for f in fields:
            old_value = getattr(update, f)
            if old_value is None or old_value != eval(f):
                setattr(update, f, eval(f))

        # for newly created Update models we need to
        # to associated any relevant draft_groups
        if created == True:
            self.update_applicable_draft_groups(update)

        # let the subclasses set the srid & any other fields specific to their type of update

        return update

    def update_applicable_draft_groups(self, update):
        """
        subclasses can override this method to associate the update with one or more draftgroups

        this method is stubbed out for this abstract/parent class
        """
        pass

    def validate_update_id(self, update_id):
        pass  # ?

    def validate_category(self, category):
        if category not in [x[0] for x in self.model.CATEGORIES]:
            raise self.CategoryException()

    def validate_type(self, type):
        pass  # ?

    def validate_value(self, value):
        pass  # ?


class LookupItem(object):
    field_srid = 'srid'
    field_model = 'model'

    def __init__(self, model):
        self.model = model
        self.data = {
            'srid': model.srid,
            'model': model,
        }

    def get_data(self):
        return self.data


class PlayerUpdateManager(AbstractUpdateManager):
    """
    This class should exclusively be used as the interface
    to adding draftgroup.models.PlayerUpdate objects to draftgroups.

    usage ex:

        from django.contrib.contenttypes.models import ContentType
        import sports.nfl.models
        from draftgroup.models import Player, PlayerUpdate
        from draftgroup.classes import PlayerUpdateManager
        sport = 'nfl'
        player_srid = '41c44740-d0f6-44ab-8347-3b5d515e5ecf' # TB12
        update_id = 'abcde'
        category = PlayerUpdate.INJURY # alternatives: NEWS, START, LINEUP
        type = 'rotowire'
        value = 'hes the GOAT ' + update_id
        pum = PlayerUpdateManager(sport, player_srid, now=True)
        update_obj = pum.add(update_id, category, type, value)

    """

    model = PlayerUpdate

    history_model_class = None  # if None, wont be saved
    lookup_model_class = None  # if None, relies solely on name-matching

    def __init__(self, sport):
        """

        :param sport:
        :param player_srid:
        :param draft_groups:
        :param now: used to help determine the 'draft_groups' unless they are specified
        :return:
        """
        super().__init__()

        self.player_name = None
        self.sport = sport
        self.sport_player_model_class = self.get_player_model_class(self.sport)
        self.players = None

    def build_player_lookup_table(self):
        """
        return a dictionary that indexes player fullnames to objects with their draftboard information
        to help us determine a player who is coming from a third party service for which no srid exists.
        """
        players = {}
        for player in self.sport_player_model_class.objects.all():
            player_data = LookupItem(player).get_data()
            player_name = '%s %s' % (player.first_name, player.last_name)
            players[player_name] = player_data
        return players

    def get_player_model_class(self, sport):
        ssm = SiteSportManager()
        site_sport = ssm.get_site_sport(sport)
        sport_player_model_class = ssm.get_player_class(site_sport)
        return sport_player_model_class

    def get_player_srid_for_pid(self, pid):
        """
        retrieve the player's srid by specifying the third party service pid for the player.

        if multiple entries have been added for the 'pid' to the PlayerLookup model use the most recent.

        :param pid:
        """
        if self.lookup_model_class is None:
            return None

        lookups = self.lookup_model_class.objects.filter(pid=pid).order_by('-created')
        if lookups.count() <= 0:
            return None

        # otherwise, return the first model in the queryset
        return lookups[0]

    def get_player_srid_for_name(self, name):
        """
        this is where the name-matching happens.
        eventually we will want to be able to link third-party players to
        their known srids internally.

        for now we simply use string matching on the [full] name the third party service gives us.
        """
        if self.players is None:
            self.players = self.build_player_lookup_table()

        lookup_data = self.players.get(name)
        if lookup_data is None:
            # the caller should handle this for players not found
            # because its expected we should find all the players a
            # high percentage of the time -- or else admin needs
            # to update the PlayerLookup model for each missing player!
            self.add_player_not_found(name)
            part1 = 'for name: %s' % str(name)
            part2 = 'check the internal "players_not_found" list'
            err_msg = '%s | %s' % (part1, part2)
            raise self.PlayerDoesNotExist(err_msg)

        # return the found player
        return lookup_data.get(LookupItem.field_srid)

    def add_player_not_found(self, name):
        """
        adds the player name to the internal list of players not found by name.

        returns True is the player was added to the list, False if they were already in the list.
        """
        if self.players_not_found is None:
            self.players_not_found = []
        if name not in self.players_not_found:
            self.players_not_found.append(name)
            return True
        return False

    # def update_applicable_draft_groups(self, update):
    #     return super().update_applicable_draft_groups(update)

    def get_draft_groups(self):
        """
        return a queryset of draft groups which we think the
        update is for , strictly based on the time param 'dt'
        :param dt:
        :return:
        """
        player_srid = self.get_player_srid_for_name(self.player_name)

        # get all DraftGroup objects which include this Player (by their SRID)
        # we should use UpcomingDraftGroup so we only
        # associate PlayerUpdate objects with relevant draftgroups
        try:
            p = self.sport_player_model_class.objects.get(srid=player_srid)
        except self.sport_player_model_class.DoesNotExist:
            err_msg = 'could not find draftboard player with srid: %s' % str(player_srid)
            raise self.PlayerDoesNotExist(err_msg)
        ctype = ContentType.objects.get_for_model(p)
        Player.objects.filter(salary_player__player_type__pk=ctype.pk,
                              salary_player__player_id=p.pk)
        draft_group_players = Player.objects.filter(
            draft_group__in=UpcomingDraftGroup.objects.all(),
            salary_player__player_type__pk=ctype.pk,
            salary_player__player_id=p.pk).distinct('draft_group')
        return [dgp.draft_group for dgp in draft_group_players]

        # TODO we should determine the player's srid in here, not outside this class!

        # TODO we should choose the 'category' inside this class !

    def add(self, player_srid, *args, **kwargs):
        """
        example super().add() arguments: update_id, category, type, value, published_at=None
        """
        # create the model instance
        update_obj = super().add(*args, **kwargs)
        fields = ['sport', 'notes', 'analysis', 'headline']
        for f in fields:
            old_value = getattr(update_obj, f)
            new_value = kwargs.get(f)
            if old_value is None or old_value != new_value:
                setattr(update_obj, f, new_value)
        update_obj.player_srid = player_srid
        update_obj.save()
        return update_obj

    def get_srid_for(self, pid=None, name=None):
        """
        attempt to get the player's SRID based on the values passed to this method

        this method raises an exception if all arguments are None.

        :param pid: the player id (aka 'pid') to look up in the lookup model class (if set)
        :param name: the players full name
        :return: the player's SRID if found, otherwise returns None
        """
        if pid is None and name is None:
            raise Exception('get_srid_for() error - all arguments are None.')

        player_srid = None  # we dont know it yet

        # 1. first try to find the srid using the PlayerLookup model
        if pid is not None:
            player_srid = self.get_player_srid_for_pid(pid)
        # return it if found.
        if player_srid is not None:
            return player_srid

        # 1b. check if someone set the players name as their pid in draftboards system
        if name is not None:
            player_srid = self.get_player_srid_for_pid(name)
        # return it if found.
        if player_srid is not None:
            return player_srid

        # 2. fall back on using string matching on the name to find the player
        return self.get_player_srid_for_name(name)


class GameUpdateManager(AbstractUpdateManager):
    """
    # TODO need to fix this to be more like PlayerUpdateManager
    This class should exclusively be used as the interface
    to adding draftgroup.models.GameUpdate objects to draftgroups.

    """

    model = GameUpdate

    def __init__(self, sport, game_srid, now=None):
        """

        :param sport:
        :param player_srid:
        :return:
        """
        super().__init__()

        self.sport = sport
        self.game_srid = game_srid
        self.now = now
        if self.now is None:
            self.now = timezone.now()

        self.draft_groups = self.get_draft_groups(self.game_srid)
        logger.info('found %s draft_groups: %s' % (len(self.draft_groups), self.draft_groups))

    def add_probable_pitcher(self, team_srid, player_srid):
        """
        helper method that calls add() with the GameUpdate.LINEUP category
        """
        update_id = '%s%s' % (self.game_srid, team_srid)
        self.add(update_id, GameUpdate.LINEUP, 'pp', player_srid)

    def add(self, update_id, category, type, value):
        """
        create or update a GameUpdate

        :param update_id:
        :param category:
        :param type:
        :param value:
        :return:
        """

        self.validate_update_id(update_id)
        self.validate_category(category)
        self.validate_type(type)
        self.validate_value(value)

        created = False
        try:
            gu = self.model.objects.get(update_id=update_id)
        except self.model.DoesNotExist:
            gu = self.model()
            gu.game_srid = self.game_srid
            gu.category = category
            gu.type = type
            gu.updated_at = timezone.now()
            created = True

        if gu.value is None or gu.value != value:
            gu.value = value
            gu.save()

        if created:
            # add it if we are in the process of creating it
            for draft_group in self.draft_groups:
                gu.draft_groups.add(draft_group)  # ManyToMany relationship!

    def get_draft_groups(self, game_srid):
        """
        get all DraftGroup objects which include this game (by its srid)
        """
        game_teams = GameTeam.objects.filter(game_srid=game_srid).distinct('draft_group')
        return [gt.draft_group for gt in game_teams]
