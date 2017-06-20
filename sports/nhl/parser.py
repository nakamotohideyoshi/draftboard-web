from django.conf import settings
from django.db.transaction import atomic

import push.classes
import push.classes
import sports.nhl.models
from dataden.classes import DataDen
from scoring.classes import NhlSalaryScoreSystem
from sports.game_status import GameStatus
from sports.nhl.models import (
    Team,
    Game,
    Player,
    PlayerStats,
    GameBoxscore,
    Pbp,
    PbpDescription,
    GamePortion,
    Season,
)
from sports.sport.base_parser import (
    AbstractDataDenParser,
    DataDenTeamHierarchy,
    DataDenGameSchedule,
    DataDenPlayerRosters,
    DataDenPlayerStats,
    DataDenGameBoxscores,
    DataDenTeamBoxscores,
    DataDenPbpDescription,
    DataDenInjury,
    SridFinder,
    DataDenSeasonSchedule,
)
from sports.sport.base_parser import TsxContentParser


class TeamHierarchy(DataDenTeamHierarchy):
    """
    TeamHierarchy simply needs to set the right Team model internally.
    """
    team_model = Team

    def __init__(self):
        super().__init__()

    def parse(self, obj):
        super().parse(obj)
        self.team.save()


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


class GameSchedule(DataDenGameSchedule):
    """
    GameSchedule simply needs to set the right Team & Game model internally
    """
    team_model = Team
    game_model = Game
    season_model = Season

    def __init__(self):
        super().__init__()

    def parse(self, obj):
        super().parse(obj)

        if self.game:
            self.game.save()


class PlayerRosters(DataDenPlayerRosters):
    team_model = Team
    player_model = Player

    def __init__(self):
        super().__init__()

    def parse(self, obj):
        super().parse(obj)
        self.player.save()


class PlayerStats(DataDenPlayerStats):
    game_model = Game
    player_model = Player
    player_stats_model = PlayerStats

    def __init__(self):
        super().__init__()
        self.scorer = NhlSalaryScoreSystem()

    def parse(self, obj):

        super().parse(obj)  # setup PlayerStats instance

        if self.ps is None:
            # the PlayerStats object couldnt be created due to a previous issue,
            #  typically, either the game or player couldnt be found by its 'srid'
            return

        # self.ps is the instance of PlayerStats we need to populate with these stats.
        # skaters do not get Goalie stats. Goalies DO GET skater stats!
        o = obj.get_o()
        statistics_list = o.get('statistics__list', {})
        skater_sh_list = statistics_list.get('shorthanded__list', {})
        skater_pp_list = statistics_list.get('powerplay__list', {})
        skater_so_list = statistics_list.get('shootout__list', {})
        goaltending_list = o.get('goaltending__list', {})

        # skater stats
        self.ps.goal = statistics_list.get('goals', 0)
        self.ps.assist = statistics_list.get('assists', 0)
        self.ps.sog = statistics_list.get('shots', 0)
        self.ps.blk = statistics_list.get('blocked_shots', 0)
        self.ps.blk_att = statistics_list.get('blocked_att', 0)  # new
        self.ps.ms = statistics_list.get('missed_shots', 0)  # new
        self.ps.sh_goal = skater_sh_list.get('goals', 0)
        self.ps.pp_goal = skater_pp_list.get('goals', 0)
        self.ps.so_goal = skater_so_list.get('goals', 0)

        # goalie stats    ... [ "win", "loss", "overtime_loss", "none" ] are the "credit" types for goalies
        self.ps.w = goaltending_list.get('credit', '').lower() == 'win'
        self.ps.l = goaltending_list.get('credit', '').lower() == 'loss'
        self.ps.otl = goaltending_list.get('credit', '').lower() == 'overtime_loss'
        self.ps.saves = goaltending_list.get('saves', 0)
        self.ps.ga = goaltending_list.get('goals_against', 0)
        self.ps.shutout = goaltending_list.get('shutout', '').lower() == "true"

        # determine whether the player played in the game or not
        # requires that we check the 'played' field. if it exists
        # and is "true" (a string) the player played, else false.
        # ie: "played": "true" means they played, else they didnt.
        played = o.get('played', None)
        if played is None:
            played = 0
        elif 't' in str(played).lower():
            played = 1
        else:
            played = 0

        self.ps.played = played  # 1 or 0.  a value of 1 indicates the skater played in the game

        #
        # set the fantasy points
        self.ps.fantasy_points = self.scorer.score_player(self.ps)

        self.ps.save()  # commit changes


class GameBoxscores(DataDenGameBoxscores):
    gameboxscore_model = GameBoxscore
    team_model = Team

    # the Game model
    game_model = Game

    # an instance of GameStatus helps us determine the "primary" status
    game_status = GameStatus(GameStatus.nhl)

    def __init__(self):
        super().__init__()

    def parse(self, obj):
        super().parse(obj)  # much of the generic parsing is done here, it sets self.boxscore

        if self.boxscore is None:
            return

        o = obj.get_o()
        self.boxscore.period = o.get('period', 1)
        self.boxscore.save()


class TeamBoxscores(DataDenTeamBoxscores):
    team_model = Team
    gameboxscore_model = GameBoxscore

    def __init__(self):
        super().__init__()

    def parse(self, obj):
        super().parse(obj)  # make sure the team exists and gets the sets self.boxscore

        # self.boxscore may be None here, if you write anymore code make sure to check


class PeriodPbp(DataDenPbpDescription):  # ADD TO PARSER SWITCH
    """
    Parse the list of periods.
    """

    game_model = Game
    pbp_model = Pbp
    portion_model = GamePortion
    pbp_description_model = PbpDescription

    def __init__(self):
        super().__init__()
        self.KEY_GAME_ID = 'game__id'

    def parse(self, obj, target=None):
        super().parse(obj, target)

        if self.game is None:
            return

        #
        # super().parse() the GamePortions for the periods
        #       so that when the pbp events are parsed
        #       the game,pbp,gameportion exists
        # get or create GamePortion for thsi period
        srid_period = self.o.get('id', None)
        sequence = self.o.get('sequence')
        game_portion = self.get_game_portion('period', sequence, save=False)  # defer save
        game_portion.srid = srid_period
        game_portion.save()  # now save that we added the srid_period

        events = self.o.get('events__list', [])

        # print('events__list count: %s' % str(len(events)))

        idx = 0
        for event_json in events:
            #
            # each event is a pbp item with a description
            srid_event = event_json.get('event', None)
            pbp_desc = self.get_pbp_description(game_portion, idx, '', save=False)  # defer save
            pbp_desc.srid = srid_event  # the 'event' is the PbpDescription
            pbp_desc.save()
            idx += 1

            # PbpEventParser will take care of saving the 'description' field


class PbpEventParser(DataDenPbpDescription):  # ADD TO PARSER SWITCH
    game_model = Game
    pbp_model = Pbp
    portion_model = GamePortion
    pbp_description_model = PbpDescription
    #
    player_stats_model = sports.nhl.models.PlayerStats
    pusher_sport_pbp = push.classes.PUSHER_NHL_PBP
    pusher_sport_stats = push.classes.PUSHER_NHL_STATS
    gameboxscore_model = GameBoxscore
    gameboxscore_period_field = 'period'
    score_system_class = NhlSalaryScoreSystem

    def __init__(self):
        super().__init__()

    def parse(self, obj, target=None):
        #
        # dont need to call super for PbpEventParser - just get the event by srid.
        # if it doesnt exist dont do anything, else set the description
        # super().parse( obj, target )

        self.original_obj = obj  # since we dont call super().parse() in this class
        self.srid_finder = SridFinder(obj.get_o())

        # pbp_desc = self.get_pbp_description(game_portion, overall_idx, desc)
        self.o = obj.get_o()  # we didnt call super so we should do this
        srid_pbp_desc = self.o.get('id', None)
        pbp_desc = self.get_pbp_description_by_srid(srid_pbp_desc)
        if pbp_desc:
            description = self.o.get('description', None)
            if pbp_desc.description != description:
                # only save it if its changed
                pbp_desc.description = description
                pbp_desc.save()
                # else:
                #     print( 'pbp_desc not found by srid %s' % srid_pbp_desc)


class Injury(DataDenInjury):
    player_model = Player
    injury_model = sports.nhl.models.Injury

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
        #

        #
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


class DataDenNhl(AbstractDataDenParser):
    # the name of the mongo database
    mongo_db_for_sport = 'nhlo'

    # currently these are just so the sport_trigger can automatically
    # create them if its started and there are any that do not exist!
    triggers = [

        # TODO - we will need to figure this out when we integrate NHL Official data
        (mongo_db_for_sport, '???', '???'),

    ]

    def __init__(self):
        self.game_model = Game  # current unused
        self.sport = 'nhl'

    def parse(self, obj):
        """
        :param obj:
        :return:
        """
        super().parse(obj)  # setup self.ns, self.parent_api

        #
        # switch statement selects the type of object to parse
        # the Namespace-ParentApi combination

        #
        # nhl.game
        if self.target == ('nhl.season_schedule', 'schedule'):
            SeasonSchedule().parse(obj)
        elif self.target == ('nhl.game', 'schedule'):
            GameSchedule().parse(obj)
        elif self.target == ('nhl.game', 'boxscores'):
            GameBoxscores().parse(obj)
            push.classes.DataDenPush(push.classes.PUSHER_BOXSCORES, 'game').send(obj,
                                                                                 async=settings.DATADEN_ASYNC_UPDATES)
        #
        # nhl.period
        elif self.target == ('nhl.period', 'pbp'):
            # PeriodPbp().parse( obj )
            # push.classes.PbpDataDenPush( push.classes.PUSHER_NHL_PBP, 'period' ).send( obj, async=settings.DATADEN_ASYNC_UPDATES )
            pass  # i dont think we need to parse this
        #
        # nhl.event
        elif self.target == ('nhl.event', 'pbp'):
            event_pbp = PbpEventParser()
            # push.classes.PbpDataDenPush( push.classes.PUSHER_NHL_PBP, 'event' ).send( obj, async=settings.DATADEN_ASYNC_UPDATES )
            event_pbp.parse(obj)
            event_pbp.send()  # pusher the data, links playerstats
        #
        # nhl.team
        elif self.target == ('nhl.team', 'hierarchy'):
            TeamHierarchy().parse(obj)
        elif self.target == ('nhl.team', 'boxscores'):
            TeamBoxscores().parse(obj)
            push.classes.DataDenPush(push.classes.PUSHER_BOXSCORES, 'team').send(obj,
                                                                                 async=settings.DATADEN_ASYNC_UPDATES)
        #
        # nhl.player
        elif self.target == ('nhl.player', 'rosters'):
            PlayerRosters().parse(obj)
        elif self.target == ('nhl.player', 'stats'):
            PlayerStats().parse(obj)
        #
        # elif self.target == ('nhl.event','pbp'): PbpEventParser().parse( obj )
        #
        #
        elif self.target == ('nhl.injury', 'injuries'):
            Injury().parse(obj)

        #
        # nhl.content - the master object with list of ids to the content items
        elif self.target == ('nhl.content', 'content'):
            #
            # get an instance of TsxContentParser( sport ) to parse
            # the Sports Xchange content
            TsxContentParser(self.sport).parse(obj)

        #
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
        # get an instance of DataDen - ie: a connection to mongo db with all the stats
        dd = DataDen()

        #
        # injury process:
        # 1) get all the updates (ie: get the most recent dd_updated__id, and get all objects with that value)
        injury_objects = list(dd.find_recent('nhl', 'injury', 'injuries'))
        print(str(len(injury_objects)), 'recent injury updates')

        # 2) get all the existing players with injuries
        # players = list( Player.objects.filter( injury_type__isnull=False,
        #                                        injury_id__isnull=False ) )
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
                                sports.nhl.models.Team,  # model class for the Team
                                sports.nhl.models.Player,  # model class for the Player
                                parent_api='rosters')  # parent api where the roster players found
