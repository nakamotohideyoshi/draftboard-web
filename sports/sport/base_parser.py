#
# sports/sport/base_parser.py

from dataden.util.timestamp import Parse as DataDenDatetime

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
    Requires: the game_model to be set by inheriting classes

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