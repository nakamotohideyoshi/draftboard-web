#
# sports/sport/base_parser.py

from dataden.util.timestamp import Parse as DataDenDatetime
import json

class AbstractDataDenParser(object):
    """
    for parsing each individual sport, which will have some differences
    """
    game_model = None

    def __init__(self):
        self.validate_models()

        self.ns         = None
        self.parent_api = None

    def validate_models(self):
        if self.game_model is None:
            raise Exception('game_model is not set')

    def name(self):
        """
        helper method to get the class name of the instance, mainly for logging
        :return:
        """
        return self.__class__.__name__

    def unimplemented(self, ns, parent_api):
        print('')
        print('UNIMPLEMENTED <<< %s | %s >>> ... generally this means DataDen<Sport> .parse() just needs an addition to the switch statement.' % (ns,parent_api))

    def parse(self, obj):
        self.ns         = obj.get_ns()
        self.parent_api = obj.get_parent_api()
        self.target     = (self.ns, self.parent_api)

        print ('%s.parse() | %s %s %s' % ( self.name(),
               self.ns, self.parent_api, str(obj.get_o()) ) )
        #
        # child parse() will execute here -- they must call super().parse( obj )
        #  then this class will have setup self.ns and self.parent_api for them

class AbstractDataDenParseable(object):
    """
    for parsing a specific object from dataden mongo db,
     specifically an object which has a namespace and a parent_api,
     such as: nba.player stats
    """

    def __init__(self):
        self.name = self.__class__.__name__

    def parse(self, obj, target=None):
        print( self.name, str(obj)[:100], 'target='+str(target) )

class DataDenTeamHierachy(AbstractDataDenParseable):
    """
    from dataden/mongo, parse the <sport>.team namespace for the parent_api: 'hierarchy',
    ie: parse a team from the the sport.

    this class should work as-is for nba and nhl,
    but you may need to override some things for other sports
    """

    team_model = None

    def __init__(self):
        if self.team_model is None:
            raise Exception('"team_model" cant be None')
        super().__init__()

    def parse(self, obj, target=None):
        super().parse( obj, target )

        # db.team.findOne({'parent_api__id':'hierarchy'})
        # {
        #     "_id" : "cGFyZW50X2FwaV9faWRoaWVyYXJjaHlsZWFndWVfX2lkNDM1MzEzOGQtNGMyMi00Mzk2LTk1ZDgtNWY1ODdkMmRmMjVjY29uZmVyZW5jZV9faWQzOTYwY2ZhYy03MzYxLTRiMzAtYmMyNS04ZDM5M2RlNmY2MmZkaXZpc2lvbl9faWQ1NGRjNzM0OC1jMWQyLTQwZDgtODhiMy1jNGMwMTM4ZTA4NWRpZDU4M2VjZWE2LWZiNDYtMTFlMS04MmNiLWY0Y2U0Njg0ZWE0Yw==",
        #     "alias" : "MIA",
        #     "id" : "583ecea6-fb46-11e1-82cb-f4ce4684ea4c",
        #     "market" : "Miami",
        #     "name" : "Heat",
        #     "parent_api__id" : "hierarchy",
        #     "dd_updated__id" : NumberLong("1431472829579"),
        #     "league__id" : "4353138d-4c22-4396-95d8-5f587d2df25c",
        #     "conference__id" : "3960cfac-7361-4b30-bc25-8d393de6f62f",
        #     "division__id" : "54dc7348-c1d2-40d8-88b3-c4c0138e085d",
        #     "venue" : "b67d5f09-28b2-5bc6-9097-af312007d2f4"
        # }

        o = obj.get_o() # strip off the oplog wrapper

        srid            = o.get('id',               None)
        srid_league     = o.get('league__id',       None)
        srid_conference = o.get('conference__id',   None)
        srid_division   = o.get('division__id',     None)
        market          = o.get('market',           None)
        name            = o.get('name',             None)
        alias           = o.get('alias',            None)
        srid_venue      = o.get('venue',            '')

        try:
            t = self.team_model.objects.get( srid=srid )
        except self.team_model.DoesNotExist:
            t = self.team_model()
            t.srid      = srid

        t.srid_league       = srid_league
        t.srid_conference   = srid_conference
        t.srid_division     = srid_division
        t.market            = market
        t.name              = name
        t.alias             = alias
        t.srid_venue        = srid_venue

        t.save()

class DataDenGameSchedule(AbstractDataDenParseable):
    """
    Requires: the game_model & team_model to be set by inheriting classes

    Parses a game objects into the database with parse()

    this class should not need much modification for nba & nhl, but it will for other sports.
    """
    team_model = None
    game_model = None

    def __init__(self):
        if self.team_model is None:
            raise Exception('"team_model cant be None!')
        if self.game_model is None:
            raise Exception('"game_model" cant be None!')
        super().__init__()

    def parse(self, obj, target=None):
        super().parse( obj, target )

        # db.game.findOne({'parent_api__id':'schedule'})
        # {
        #     "_id" : "cGFyZW50X2FwaV9faWRzY2hlZHVsZWxlYWd1ZV9faWQ0MzUzMTM4ZC00YzIyLTQzOTYtOTVkOC01ZjU4N2QyZGYyNWNzZWFzb24tc2NoZWR1bGVfX2lkNWJhM2NkNGQtNDk1Yi00NjgzLWJmYmUtNTZiYTJlYjg0Y2YycGFyZW50X2xpc3RfX2lkZ2FtZXNfX2xpc3RpZDVmYmQzMjk1LTMyY2EtNDQ1Zi1iYWY1LWM3YzAwODM1MTM5OA==",
        #     "away_team" : "583ec8d4-fb46-11e1-82cb-f4ce4684ea4c",
                            #     "coverage" : "full",
        #     "home_team" : "583ecda6-fb46-11e1-82cb-f4ce4684ea4c",
        #     "id" : "5fbd3295-32ca-445f-baf5-c7c008351398",
        #     "scheduled" : "2015-04-18T16:30:00+00:00",
        #     "status" : "closed",
        #     "title" : "Game 1",
                            #     "parent_api__id" : "schedule",
                            #     "dd_updated__id" : NumberLong("1431472812731"),
                            #     "league__id" : "4353138d-4c22-4396-95d8-5f587d2df25c",
                            #     "season_schedule__id" : "5ba3cd4d-495b-4683-bfbe-56ba2eb84cf2",
                            #     "parent_list__id" : "games__list",
                            #     "venue" : "62cc9661-7b13-56e7-bf4a-bba7ad7be8da",
        #     "home" : "583ecda6-fb46-11e1-82cb-f4ce4684ea4c",
        #     "away" : "583ec8d4-fb46-11e1-82cb-f4ce4684ea4c",
                            #     "broadcast__list" : {
                            #         "internet" : "WatchESPN",
                            #         "network" : "ESPN",
                            #         "satellite" : 206
                            #     }
        # }

        o = obj.get_o()

        srid        = o.get('id')
        start_str   = o.get('scheduled')
        start       = DataDenDatetime.from_string( start_str )
        status      = o.get('status')

        srid_home   = o.get('home')
        srid_away   = o.get('away')
        title       = o.get('title', True)

        try:
            h = self.team_model.objects.get(srid=srid_home)
        except self.team_model.DoesNotExist:
            print( str(o) )
            print( 'Team (home) for Game DoesNotExist! Have you parsed the "hierarchy" feed recently?')
            return

        try:
            a = self.team_model.objects.get(srid=srid_away)
        except self.team_model.DoesNotExist:
            print( str(o) )
            print( 'Team (away) for Game DoesNotExist! Have you parsed the "hierarchy" feed recently?')
            return

        try:
            g = self.game_model.objects.get(srid=srid)
        except self.game_model.DoesNotExist:
            g = self.game_model()
            g.srid = srid

        g.home      = h
        g.away      = a
        g.start     = start
        g.status    = status
        g.srid_home = srid_home
        g.srid_away = srid_away
        g.title     = title
        g.save()

class DataDenPlayerRosters(AbstractDataDenParseable):

    team_model = None
    player_model = None

    def __init__(self):
        if self.team_model is None:
            raise Exception('"team_model" cant be None!')
        if self.player_model is None:
            raise Exception('"player_model" cant be None!')
        super().__init__()

    def parse(self, obj, target=None):
        super().parse( obj, target )

        # {
        #     "_id" : "cGFyZW50X2FwaV9faWRyb3N0ZXJzdGVhbV9faWQ0NDE1NTkwOS0wZjI0LTExZTItODUyNS0xOGE5MDU3NjdlNDRwYXJlbnRfbGlzdF9faWRwbGF5ZXJzX19saXN0aWQyZmRmNTI4OS1lNmQwLTRlZDMtODJmMC1hZDk1ZmI5OGMwNjU=",
        #     "abbr_name" : "M.Karlsson",
        #     "birth_place" : "Lycksele,, SWE",
        #     "birthdate" : "1990-07-18",
        #     "first_name" : "Melker",
        #     "full_name" : "Melker Karlsson",
        #     "handedness" : "R",
        #     "height" : 72,
        #     "id" : "2fdf5289-e6d0-4ed3-82f0-ad95fb98c065",
        #     "jersey_number" : 68,
        #     "last_name" : "Karlsson",
        #     "position" : "F",
        #     "primary_position" : "C",
        #     "status" : "ACT",
        #     "updated" : "2014-12-09T20:19:44+00:00",
        #     "weight" : 180,
        #     "parent_api__id" : "rosters",
        #     "dd_updated__id" : NumberLong("1431977962274"),
        #     "team__id" : "44155909-0f24-11e2-8525-18a905767e44",
        #     "parent_list__id" : "players__list"
        # }

        o = obj.get_o()

        srid        = o.get('id')
        srid_team   = o.get('team__id')

        first_name  = o.get('first_name')
        last_name   = o.get('last_name')

        birth_place = o.get('birth_place', '')
        birthdate   = o.get('birthdate', '')
        experience  = o.get('experience', 0.0)
        height      = o.get('height', 0.0)      # inches
        weight      = o.get('weight', 0.0)      # lbs.
        jersey_number       = o.get('jersey_number', 0.0)

        position            = o.get('position')
        primary_position    = o.get('primary_position')

        status              = o.get('status')   # roster status, ie: basically whether they are on it

        try:
            t = self.team_model.objects.get(srid=srid_team)
        except self.team_model.DoesNotExist:
            print( str(o) )
            print( 'Team for Player DoesNotExist!')
            return

        try:
            p = self.player_model.objects.get(srid=srid)
        except self.player_model.DoesNotExist:
            p = self.player_model()
            p.srid = srid

        p.team          = t             # team could easily change of course
        p.first_name    = first_name
        p.last_name     = last_name

        p.birth_place   = birth_place
        p.birthdate     = birthdate
        p.experience    = experience
        p.height        = height
        p.weight        = weight
        p.jersey_number = jersey_number
        p.position      = position
        p.primary_position  = primary_position
        p.status        = status

        p.save()

class DataDenPlayerStats(AbstractDataDenParseable):

    game_model          = None
    player_model        = None
    player_stats_model  = None

    def __init__(self):
        if self.game_model is None:
            raise Exception('"game_model" cant be None!')
        if self.player_model is None:
            raise Exception('"player_model" cant be None!')
        if self.player_stats_model is None:
            raise Exception('"player_stats_model" cant be None!')

        self.ps = None # this will hold the PlayerStats object

        super().__init__()

    def parse(self, obj, target=None):
        """
        get or create the game player and set it to self.ps

        sub-classes must take care of settings the actual per-sport stats!

        :param obj:
        :param target:
        :return:
        """
        super().parse( obj, target )

        o = obj.get_o()
        srid_game   = o.get('game__id', None)
        srid_player = o.get('id', None)

        try:
            p = self.player_model.objects.get(srid=srid_player)
        except self.player_model.DoesNotExist:
            # first_name  = o.get('first_name', None)
            # last_name   = o.get('last_name', None)
            # full_name   = '%s %s' % (str(first_name), str(last_name))
            print( str(o) )
            print('Player object for PlayerStats DoesNotExist')
            return # dont create the playerstats then

        try:
            g = self.game_model.objects.get(srid=srid_game)
        except self.game_model.DoesNotExist:
            print( str(o) )
            print('Game object for PlayerStats DoesNotExist')
            return # dont create the playerstats then

        try:
            self.ps = self.player_stats_model.objects.get( srid_game=srid_game, srid_player=srid_player )
        except self.player_stats_model.DoesNotExist:
            self.ps = self.player_stats_model()
            self.ps.srid_game    = srid_game
            self.ps.srid_player  = srid_player
            self.ps.player  = p
            self.ps.game    = g

class DataDenGameBoxscores(AbstractDataDenParseable):

    gameboxscore_model  = None
    team_model          = None

    def __init__(self):
        if self.gameboxscore_model is None:
            raise Exception('"gameboxscore_model" cant be None!')
        if self.team_model is None:
            raise Exception('"team_model" cant be None!')

        self.boxscore = None

        super().__init__()

    def parse(self, obj, target=None):
        super().parse( obj, target )

        # db.game.findOne({'parent_api__id':'boxscores','status':'inprogress'})
        # {
        #     "_id" : "cGFyZW50X2FwaV9faWRib3hzY29yZXNpZGMzNGMwZDRjLWU1ZGQtNDMzOS04YjIyLWZhZWUyOWEzZDFhMQ==",
        #     "away_team" : "4417d3cb-0f24-11e2-8525-18a905767e44",
        #     "clock" : "14:22",
        #     "coverage" : "full",
        #     "home_team" : "441781b9-0f24-11e2-8525-18a905767e44",
        #     "id" : "c34c0d4c-e5dd-4339-8b22-faee29a3d1a1",
        #     "period" : 1,
        #     "scheduled" : "2015-05-19T00:00:00+00:00",
        #     "start_time" : "2015-05-19T00:15:00+00:00",
        #     "status" : "inprogress",
        #     "title" : "Game 2",
        #     "xmlns" : "http://feed.elasticstats.com/schema/hockey/game-v2.0.xsd",
        #     "parent_api__id" : "boxscores",
        #     "dd_updated__id" : NumberLong("1431995308494"),
        #     "teams" : [
        #         {
        #             "team" : "441781b9-0f24-11e2-8525-18a905767e44"
        #         },
        #         {
        #             "team" : "4417d3cb-0f24-11e2-8525-18a905767e44"
        #         }
        #     ]
        # }

        o = obj.get_o()
        srid_game   = o.get('id', None)
        srid_home   = o.get('home_team', None)
        srid_away   = o.get('away_team', None)

        try:
            h = self.team_model.objects.get( srid=srid_home )
        except self.team_model.DoesNotExist:
            print( str(o) )
            print( 'Team (home_team) does not exist for srid so not creating GameBoxscore')
            return

        try:
            a = self.team_model.objects.get( srid=srid_away )
        except self.team_model.DoesNotExist:
            print( str(o) )
            print( 'Team (away_team) does not exist for srid so not creating GameBoxscore')
            return

        try:
            self.boxscore = self.gameboxscore_model.objects.get(srid_game=srid_game)
        except self.gameboxscore_model.DoesNotExist:
            self.boxscore = self.gameboxscore_model()
            self.boxscore.srid_game = srid_game

        self.boxscore.srid_home  = srid_home
        self.boxscore.home       = h
        self.boxscore.away       = a
        self.boxscore.srid_away  = srid_away

        self.boxscore.clock      = o.get('clock', '' )
        self.boxscore.coverage   = o.get('coverage', '')
        self.boxscore.status     = o.get('status', '')
        self.boxscore.title      = o.get('title', '')

class DataDenTeamBoxscores(AbstractDataDenParseable):

    gameboxscore_model  = None

    def __init__(self):
        if self.gameboxscore_model is None:
            raise Exception('"gameboxscore_model" cant be None!')

        self.boxscore = None

        super().__init__()

    def parse(self, obj, target=None):
        # db.team.findOne({'game__id':'c34c0d4c-e5dd-4339-8b22-faee29a3d1a1','parent_api__id':'boxscores'})
        # {
        #     "_id" : "cGFyZW50X2FwaV9faWRib3hzY29yZXNnYW1lX19pZGMzNGMwZDRjLWU1ZGQtNDMzOS04YjIyLWZhZWUyOWEzZDFhMWlkNDQxN2QzY2ItMGYyNC0xMWUyLTg1MjUtMThhOTA1NzY3ZTQ0",
        #     "id" : "4417d3cb-0f24-11e2-8525-18a905767e44",
        #     "market" : "Tampa Bay",
        #     "name" : "Lightning",
        #     "points" : 6,
        #     "parent_api__id" : "boxscores",
        #     "dd_updated__id" : NumberLong("1432004309403"),
        #     "game__id" : "c34c0d4c-e5dd-4339-8b22-faee29a3d1a1",
        #     "scoring__list" : [
        #         {
        #             "period" : {
        #                 "number" : 1,
        #                 "points" : 2,
        #                 "sequence" : 1
        #             }
        #         },
        #         {
        #             "period" : {
        #                 "number" : 2,
        #                 "points" : 1,
        #                 "sequence" : 2
        #             }
        #         },
        #         {
        #             "period" : {
        #                 "number" : 3,
        #                 "points" : 3,
        #                 "sequence" : 3
        #             }
        #         }
        #     ],
        super().parse( obj, target )

        o = obj.get_o()
        srid_game   = o.get('game__id', None)
        srid_team   = o.get('id', None)

        try:
            self.boxscore = self.gameboxscore_model.objects.get(srid_game=srid_game)
        except self.gameboxscore_model.DoesNotExist:
            # it hasnt been created yet, but only create it in GameBoxscores.
            return

        if self.boxscore.srid_home == srid_team:
            self.boxscore.home_score        = o.get('points', 0)
            self.boxscore.home_scoring_json = json.loads( json.dumps(o.get('scoring__list', [])))

        elif self.boxscore.srid_away == srid_team:
            self.boxscore.away_score        = o.get('points', 0)
            self.boxscore.away_scoring_json = json.loads( json.dumps(o.get('scoring__list', [])))

        else:
            # this team differs from the teams on this boxscore !
            self.boxscore = None
            print( str(o) )
            print( 'The team[%s] doesnt match home or away team!')
            return

        self.boxscore.save()
