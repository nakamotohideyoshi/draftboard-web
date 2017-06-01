from logging import getLogger

from django.db.transaction import atomic
from django.db.utils import IntegrityError
from raven.contrib.django.raven_compat.models import client

import push.classes
import sports.nba.models
from dataden.classes import DataDen
from sports.game_status import GameStatus
from sports.nba.models import (
    Team,
    Game,
    Player,
    GameBoxscore,
    Pbp,
    PbpDescription,
    GamePortion,
    Season,
)
from sports.sport.base_parser import (
    DataDenGameBoxscores,
    AbstractDataDenParser,
    DataDenPlayerStats,
    DataDenSeasonSchedule,
    DataDenTeamHierarchy,
    DataDenGameSchedule,
    DataDenPlayerRosters,
    DataDenTeamBoxscores,
    DataDenPbpDescription,
    DataDenInjury,
    SridFinder,
)
from sports.sport.base_parser import (
    TsxContentParser,
)
from util.dicts import (
    Reducer,
    Shrinker,
    Manager,
)

logger = getLogger('sports.nba.parser')


class TeamBoxscoreReducer(Reducer):
    remove_fields = [
        '_id',
        'parent_api__id',
    ]


class TeamBoxscoreShrinker(Shrinker):
    fields = {
        'id': 'srid_team',
        'dd_updated__id': 'ts',
        'game__id': 'srid_game',
    }


class TeamBoxscoreManager(Manager):
    reducer_class = TeamBoxscoreReducer
    shrinker_class = TeamBoxscoreShrinker


class TeamBoxscores(DataDenTeamBoxscores):
    gameboxscore_model = GameBoxscore

    # setting manager_class will cause it to
    # reduce and shrink the data before getting sent to client
    manager_class = TeamBoxscoreManager

    # for pusher to know the channel & event
    # 'boxscores', its not sport specific
    channel = push.classes.PUSHER_BOXSCORES
    event = 'team'

    def __init__(self):
        super().__init__()

    def parse(self, obj, target=None):
        super().parse(obj, target)
        # super() does all the work !

    def send(self, *args, **kwargs):
        super().send()

        # build the data (with Manager class instance if its set)
        data = self.get_send_data()
        # pusher it
        push.classes.DataDenPush(self.channel, self.event).send(data)


class GameBoxscoreReducer(Reducer):
    remove_fields = []


class GameBoxscoreShrinker(Shrinker):
    """ in underlying data, rename key to value for all key-value-pairs in 'fields' """
    fields = {
        'id': 'srid_game'
    }


class GameBoxscoreManager(Manager):
    """
    get_data() method calls reduce() and shrink() automatically
    """
    shrinker_class = GameBoxscoreShrinker
    reducer_class = GameBoxscoreReducer


class GameBoxscoreParser(DataDenGameBoxscores):
    gameboxscore_model = GameBoxscore
    # the Game model
    game_model = Game
    team_model = Team
    # an instance of GameStatus helps us determine the "primary" status
    game_status = GameStatus(GameStatus.nba)
    # setting manager_class will cause it to
    # reduce and shrink the data before getting sent to client
    manager_class = GameBoxscoreManager
    # 'boxscores' pusher channel
    channel = push.classes.PUSHER_BOXSCORES
    event = 'game'
    field_srid_game = 'id'
    field_status = 'status'
    status_halftime = 'halftime'
    boxscore = None

    def __init__(self):
        super().__init__()

    def parse(self, obj, target=None):
        """
        Args:
            obj:
            target:

        Returns:
        """

        # parse triggered object will set original_obj
        # to the current object (with wrapper)
        # and set the self.o (to the unwrapped object)
        self.parse_triggered_object(obj)
        o = self.o  # everything uses 'o already
        # summary_list = o.get('summary__list', {})

        srid_game = o.get(self.field_srid_game, None)
        # srid_home = o.get(self.HOME, None)
        # srid_away = o.get(self.AWAY, None)

        srid_home = o.get(self.HOME, None)
        srid_away = o.get(self.AWAY, None)

        try:
            h = self.team_model.objects.get(srid=srid_home)
        except self.team_model.DoesNotExist:
            logger.error(('Home_team does not exist, not creating GameBoxscore for '
                          'srid_game: %s | srid_home: %s') % (srid_game, srid_home))
            client.captureException()
            return

        try:
            a = self.team_model.objects.get(srid=srid_away)
        except self.team_model.DoesNotExist:
            logger.error(('Away_team does not exist, not creating GameBoxscore for '
                          'srid_game: %s | srid_away: %s') % (srid_game, srid_away))
            client.captureException()
            return

        try:
            self.boxscore = self.gameboxscore_model.objects.get(
                srid_game=srid_game)
        except self.gameboxscore_model.DoesNotExist:
            self.boxscore = self.gameboxscore_model()
            self.boxscore.srid_game = srid_game

        self.boxscore.srid_home = srid_home
        self.boxscore.home = h
        self.boxscore.away = a
        self.boxscore.srid_away = srid_away

        self.boxscore.quarter = o.get('quarter', 0)
        self.boxscore.clock = o.get('clock', '')
        # deprecated, but it will default to empty string
        self.boxscore.coverage = o.get('coverage', '')
        self.boxscore.status = o.get(self.field_status, '')
        self.boxscore.title = o.get('title', '')

        self.boxscore.save()
        logger.info('nba.GameBoxscore Parsed: %s' % self.boxscore)

        # use the boxscore status to update the Game object
        # because the boxscore will be updated much more frequently in
        # real-time especially
        self.update_schedule_game_status(srid_game, self.boxscore.status)

    def update_boxscore_data_in_game(self, boxscore_data):
        game = sports.nba.models.Game.objects.get(srid=self.o.get(self.field_srid_game))
        game.boxscore_data = boxscore_data
        logger.info(
            'Updating game.boxscore data. game: %s -- boxscore_data: %s' % (game, boxscore_data))
        game.save()

    def send(self, *args, **kwargs):
        is_halftime = self.o.get(self.field_status) == self.status_halftime
        data = self.get_send_data()

        # halftime hack to ensure quarter is not left at '2' and is at least
        # moved to '3' during halftime
        try:
            if is_halftime and int(data['quarter']) <= 2:
                data['quarter'] = 3
        except Exception:
            # debug this because i want to know about problems with different scenarios
            client.captureException()

        self.update_boxscore_data_in_game(data)

        # pusher it
        push.classes.DataDenPush(self.channel, self.event).send(data)


class PlayerRosters(DataDenPlayerRosters):
    team_model = Team
    player_model = Player

    def __init__(self):
        super().__init__()

    def parse(self, obj, target=None):
        super().parse(obj, target)

        if self.player is None:
            return

        college = self.o.get('college', '')
        draft_pick = self.o.get('draft__list.pick', '')
        draft_round = self.o.get('draft__list.round', '')
        draft_year = self.o.get('draft__list.year', '')
        srid_draft_team = self.o.get('draft__list.team_id', '')

        self.player.college = college
        self.player.draft_pick = draft_pick
        self.player.draft_round = draft_round
        self.player.draft_year = draft_year
        self.player.srid_draft_team = srid_draft_team

        self.player.save()  # commit to db


class SeasonSchedule(DataDenSeasonSchedule):
    """
    """

    season_model = Season

    def __init__(self):
        super().__init__()

    def parse(self, obj, target=None):
        super().parse(obj, target)

        if self.season is None:
            return

        self.season.save()


class TeamHierarchy(DataDenTeamHierarchy):
    """
    Parse an object from which represents a Team for this sport into the db.
    """

    team_model = Team

    def __init__(self):
        super().__init__()

    def parse(self, obj, target=None):
        super().parse(obj, target)

        if self.team is None:
            return

        self.team.save()


class PlayerStatsParser(DataDenPlayerStats):
    game_model = Game
    player_model = Player
    player_stats_model = sports.nba.models.PlayerStats

    def __init__(self):
        super().__init__()

    def parse(self, obj, target=None):
        super().parse(obj, target)

        if self.ps is None:
            return

        o = obj.get_o()
        o = o.get('statistics__list', {})
        # { 'defensive_rebounds': 1.0,
        self.ps.defensive_rebounds = o.get('defensive_rebounds', 0.0)
        # 'two_points_pct': 0.6,
        self.ps.two_points_pct = o.get('two_points_pct', 0.0)
        # 'assists': 0.0,
        self.ps.assists = o.get('assists', 0.0)
        # 'free_throws_att': 2.0,
        self.ps.free_throws_att = o.get('free_throws_att', 0.0)
        # 'flagrant_fouls': 0.0,
        self.ps.flagrant_fouls = o.get('flagrant_fouls', 0.0)
        # 'offensive_rebounds': 1.0,
        self.ps.offensive_rebounds = o.get('offensive_rebounds', 0.0)
        # 'personal_fouls': 0.0,
        self.ps.personal_fouls = o.get('personal_fouls', 0.0)
        # 'field_goals_att': 5.0,
        self.ps.field_goals_att = o.get('field_goals_att', 0.0)
        # 'three_points_att': 0.0,
        self.ps.three_points_att = o.get('three_points_att', 0.0)
        # 'field_goals_pct': 60.0,
        self.ps.field_goals_pct = o.get('field_goals_pct', 0.0)
        # 'turnovers': 0.0,
        self.ps.turnovers = o.get('turnovers', 0.0)
        # 'points': 8.0,
        self.ps.points = o.get('points', 0.0)
        # 'rebounds': 2.0,
        self.ps.rebounds = o.get('rebounds', 0.0)
        # 'two_points_att': 5.0,
        self.ps.two_points_att = o.get('two_points_att', 0.0)
        # 'field_goals_made': 3.0,
        self.ps.field_goals_made = o.get('field_goals_made', 0.0)
        # 'blocked_att': 0.0,
        self.ps.blocked_att = o.get('blocked_att', 0.0)
        # 'free_throws_made': 2.0,
        self.ps.free_throws_made = o.get('free_throws_made', 0.0)
        # 'blocks': 0.0,
        self.ps.blocks = o.get('blocks', 0.0)
        # 'assists_turnover_ratio': 0.0,
        self.ps.assists_turnover_ratio = o.get('assists_turnover_ratio', 0.0)
        # 'tech_fouls': 0.0,
        self.ps.tech_fouls = o.get('tech_fouls', 0.0)
        # 'three_points_made': 0.0,
        self.ps.three_points_made = o.get('three_points_made', 0.0)
        # 'steals': 0.0,
        self.ps.steals = o.get('steals', 0.0)
        # 'two_points_made': 3.0,
        self.ps.two_points_made = o.get('two_points_made', 0.0)
        # 'free_throws_pct': 100.0,
        self.ps.free_throws_pct = o.get('free_throws_pct', 0.0)
        # 'three_points_pct': 0.0
        self.ps.three_points_pct = o.get('three_points_pct', 0.0)

        # minutes will be in the form '20:13'   (20 minutes, 13 seconds)
        minutes_val = o.get('minutes', None)
        if not isinstance(minutes_val, str):
            # its not a string, set default value of 0
            self.ps.minutes = 0.0
        else:
            # parse the string
            parts = minutes_val.split(':')
            if len(parts) == 2:
                self.ps.minutes = float(parts[0])

        self.ps.save()  # commit changes


class GameSchedule(DataDenGameSchedule):
    team_model = Team
    game_model = Game
    season_model = Season

    def __init__(self):
        super().__init__()

    def parse(self, obj, target=None):
        super().parse(obj, target)

        if self.game is None:
            return

        self.game.save()


class QuarterPbp(DataDenPbpDescription):
    """
    Parse the list of quarters.
    """

    game_model = Game
    pbp_model = Pbp
    portion_model = GamePortion
    pbp_description_model = PbpDescription

    def __init__(self):
        super().__init__()
        self.KEY_GAME_ID = 'game__id'

    def parse(self, obj, target=None):
        self.timer_start()

        # super().parse() the GamePortions for the periods so that when the pbp events are parsed
        # the game,pbp,gameportion exists get or create GamePortion for this period
        super().parse(obj, target)

        if self.game is None:
            return

        srid_period = self.o.get('id', None)
        sequence = self.o.get('sequence')
        game_portion = self.get_game_portion('quarter', sequence, save=False)  # defer save
        game_portion.srid = srid_period
        game_portion.save()  # now save that we added the srid_period

        events = self.o.get('events__list', [])

        # print('events__list count: %s' % str(len(events)))

        idx = 0
        for event_json in events:
            #
            # each event is a pbp item with a description
            srid_event = event_json.get('event', None)
            pbp_desc = self.get_pbp_description(
                game_portion, idx, '', save=False)  # defer save
            # previous line should probably be the following line:
            # pbp_desc    = self.get_pbp_description_by_srid( srid_event )
            pbp_desc.srid = srid_event  # the 'event' is the PbpDescription
            try:
                pbp_desc.save()
            #
            # django.db.utils.IntegrityError
            except IntegrityError:
                #
                # its possible the pbp_desc was already created because we
                # deferred saving it in this spot
                pass  # TODO

            idx += 1

            # PbpEventParser will take care of saving the 'description' field
        self.timer_stop()


class PbpEventParser(DataDenPbpDescription):
    game_model = Game
    pbp_model = Pbp
    portion_model = GamePortion
    pbp_description_model = PbpDescription
    player_stats_model = sports.nba.models.PlayerStats
    pusher_sport_pbp = push.classes.PUSHER_NBA_PBP
    pusher_sport_stats = push.classes.PUSHER_NBA_STATS
    gameboxscore_model = GameBoxscore
    gameboxscore_period_field = 'quarter'

    def __init__(self):
        super().__init__()

    def parse(self, obj, target=None):
        """
        Parse the NBA PBP event.

        :param obj: an OpLogObject
        :param target:
        :return:
        """
        super().parse(obj, target)

        # Log object for debugging.
        logger.info("Parsing NBA PBP Object: %s" % self.o)
        srid_pbp_desc = self.o.get('id', None)
        pbp_desc = self.get_pbp_description_by_srid(srid_pbp_desc)

        # TODO: (zach) I'm not sure if any of this description stuff is needed.
        if pbp_desc:
            # DataDenNba.parse() | nba.event pbp {
            # 'updated': '2015-06-17T03:58:49+00:00',
            # 'parent_list__id': 'events__list',
            # 'possession': '583ec825-fb46-11e1-82cb-f4ce4684ea4c',
            # 'dd_updated__id': 1441316758302,
            # 'parent_api__id': 'pbp',
            # 'clock': '00:00',
            # 'description': 'End of 4th Quarter.',
            # 'event_type': 'endperiod',
            # 'quarter__id': '37d8a2b0-eb65-431d-827f-1c25396a3f1f',
            # 'game__id': '63aa3abe-c1c2-4d69-8d0f-5e3e2f263470',
            # 'id': '3688ff8b-f056-412f-9189-7f123073217f',
            # '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDYzYWEzYWJlLWMxYzItNGQ2OS04ZDBmLTVlM2U...'
            # }

            # pbp_description_model: <class 'sports.nba.models.PbpDescription'>

            description = self.o.get('description', None)
            logger.debug('description: %s' % description)

            if pbp_desc.description != description:
                # only save it if its changed
                logger.debug(
                    '..saving it because it doesnt match the description we currently have (must '
                    'have changed)')
                pbp_desc.description = description
                pbp_desc.save()
                logger.debug('before: %s' % pbp_desc.description)
                pbp_desc.refresh_from_db()
                logger.debug('after: %s' % pbp_desc.description)
            else:
                logger.debug('..not saving description because it matches what we currently have.')
                pass
        else:
            logger.debug('pbp_desc not found by srid %s' % srid_pbp_desc)
            pass

    def get_send_data(self):
        """
        Build the linked object from the parts

        This gets called in self.send() just before the payload is Pusher'd
        :return:
        """

        # get the PlayerStats model instances associated with this play
        # which can be found using the game and player srids
        srid_finder = SridFinder(self.o)
        srid_games = srid_finder.get_for_field('game__id')
        srid_players = srid_finder.get_for_field('player')
        player_stats = self.find_player_stats(srid_players)

        logger.debug(
            '%s PlayerStats found for srid_game="%s", srid_player__in=%s' % (
                player_stats.count(),
                srid_games, srid_players)
        )

        # Gather linked player stats.
        player_stats_json = []
        for ps in player_stats:
            stats = ps.to_json()
            # Attach first + last name to the player stats info.
            stats['first_name'] = ps.player.first_name
            stats['last_name'] = ps.player.last_name
            player_stats_json.append(stats)

        # Attach PBP and linked stats, then return.
        data = {
            'pbp': self.o,
            'stats': player_stats_json,
            'game': self.get_game_info(),
        }

        return data


class Injury(DataDenInjury):
    player_model = Player
    injury_model = sports.nba.models.Injury

    key_iid = 'id'  # the name of the field in the obj

    def __init__(self, wrapped=True):
        super().__init__(wrapped)

    def parse(self, obj, target=None):
        super().parse(obj, target)

        if self.player is None or self.injury is None:
            return

        # "comment" : "Wroten had successful surgery on his knee on Tuesday (2/3).",
        # "desc" : "Knee",
        # "id" : "c2c3e64b-3363-411d-b55a-a9878fd79310",
        # "start_date" : "2015-01-14",
        # "status" : "Out For Season",
        # "update_date" : "2015-02-04",
        # "parent_api__id" : "injuries",

        # extract the information from self.o
        self.injury.srid = self.o.get('id', '')  # not set by parent
        self.injury.comment = self.o.get('comment', '')
        self.injury.status = self.o.get('status', '')
        self.injury.description = self.o.get('desc', '')
        self.injury.save()

        #
        # connect the player object to the injury object
        self.player.injury = self.injury
        self.player.save()


class DataDenNba(AbstractDataDenParser):
    # the name of the mongo database
    mongo_db_for_sport = 'nba'

    # currently these are just so the sport_trigger can automatically
    # create them if its started and there are any that do not exist!
    triggers = [
        (mongo_db_for_sport, 'team', 'hierarchy'),
        (mongo_db_for_sport, 'season_schedule', 'schedule'),
        (mongo_db_for_sport, 'game', 'schedule'),
        (mongo_db_for_sport, 'player', 'rosters'),
        (mongo_db_for_sport, 'game', 'boxscores'),
        (mongo_db_for_sport, 'team', 'boxscores'),
        (mongo_db_for_sport, 'player', 'stats'),
        (mongo_db_for_sport, 'quarter', 'pbp'),
        (mongo_db_for_sport, 'event', 'pbp'),
    ]

    def __init__(self):
        self.sport = 'nba'

    def parse(self, obj):
        """
        :param obj:
        :return:
        """
        super().parse(obj)  # setup self.ns, self.parent_api

        # switch statement selects the type of object to parse
        # the Namespace-ParentApi combination

        # nba.game
        if self.target == ('nba.season_schedule', 'schedule'):
            SeasonSchedule().parse(obj)
        elif self.target == ('nba.game', 'schedule'):
            GameSchedule().parse(obj)
        elif self.target == ('nba.game', 'boxscores'):
            game_boxscore_parser = GameBoxscoreParser()
            game_boxscore_parser.parse(obj, self.target)
            game_boxscore_parser.send()

        # nba.team
        elif self.target == ('nba.team', 'hierarchy'):
            TeamHierarchy().parse(obj)
        elif self.target == ('nba.team', 'boxscores'):
            team_boxscore_parser = TeamBoxscores()
            team_boxscore_parser.parse(obj, self.target)
            team_boxscore_parser.send()

            # push.classes.DataDenPush(push.classes.PUSHER_BOXSCORES, 'team').send(
            #     obj, async=settings.DATADEN_ASYNC_UPDATES)

        # nba.period
        elif self.target == ('nba.quarter', 'pbp'):
            # QuarterPbp().parse( obj )
            # use Pusher to send this object after DB entry created
            # PbpDataDenPush( push.classes.PUSHER_NBA_PBP, 'quarter' ).send(
            #   obj, async=settings.DATADEN_ASYNC_UPDATES )
            # self.add_pbp( obj ) # stashes the pbp object for the trailing
            # history
            pass  # i dont think we need to parse this!

        # nba.event
        elif self.target == ('nba.event', 'pbp'):
            #
            # handle a play by play event from dataden.
            event_pbp = PbpEventParser()
            event_pbp.parse(obj)  # takes care of pushering the data too.
            # pushers the pbp + stats data as one piece of data
            event_pbp.send()

            # stashes the pbp object for the trailing history api - DISABLED
            # self.add_pbp(obj)

        # nba.player
        elif self.target == ('nba.player', 'rosters'):
            PlayerRosters().parse(obj)

        elif self.target == ('nba.player', 'stats'):
            #
            # will save() the nba PlayerStats model corresponding to this
            # player.
            PlayerStatsParser().parse(obj)
            # note: the PlayerStats model takes care of pushering its updated data!

        # nba.injury
        elif self.target == ('nba.injury', 'injuries'):
            Injury().parse(obj)

        # nba.content - the master object with list of ids to the content items
        elif self.target == ('nba.content', 'content'):
            # get an instance of TsxContentParser('nba') to parse
            # the Sports Xchange content
            TsxContentParser(self.sport).parse(obj)

        # default case, print this message for now
        else:
            self.unimplemented(self.target[0], self.target[1])

    def cleanup_injuries(self):
        """
        When injury objects are parsed, they connect players with injuries.

        However, there needs to be a method which removes injuries objects
        from players who are no longer injured. This is that process,
        and it should be run rather frequently - or at least about as
        frequently as injury feeds are parsed.
        :return:
        """

        #
        # get an instance of DataDen - ie: a connection to mongo db with all
        # the stats
        dd = DataDen()

        #
        # injury process:
        # 1) get all the updates (ie: get the most recent dd_updated__id, and
        # get all objects with that value)
        injury_objects = list(dd.find_recent('nba', 'injury', 'injuries'))
        print(str(len(injury_objects)), 'recent injury updates')

        # 2) get all the existing players with injuries
        # players = list( Player.objects.filter( injury_type__isnull=False, injury_id__isnull=False ) )
        all_players = list(Player.objects.all())

        # 3) for each updated injury, remove the player from the all-players list
        for inj in injury_objects:
            #
            # wrapped=False just means the obj isnt wrapped by the oplogwrapper
            i = Injury(wrapped=False)
            i.parse(inj)
            try:
                all_players.remove(i.get_player())
            except ValueError:
                pass  # thrown if player not in the list.

        # 5) with the leftover existing players,
        #    remove their injury since theres no current injury for them
        ctr_removed = 0
        for player in all_players:
            if player.remove_injury():
                ctr_removed += 1
        print(str(ctr_removed), 'leftover/stale injuries removed')

    @atomic
    def cleanup_rosters(self):
        """
        give the parent method the Team, Player classes,
        and rosters parent api so it can flag players
        who are no long on the teams roster on_active_roster = False
        """
        super().cleanup_rosters(self.sport,  # datadeb sport db, ie: 'nba'
                                # model class for the Team
                                sports.nba.models.Team,
                                # model class for the Player
                                sports.nba.models.Player,
                                parent_api='rosters')  # parent api where the roster players found
