#
import sports.nba.models
from sports.sport.base_parser import AbstractDataDenParser
from dataden.util.timestamp import Parse as DataDenDatetime

class AbstractParseable(object):
    def __init__(self):
        self.name = self.__class__.__name__
    def parse(self, obj, target=None):
        print( self.name, str(obj)[:200], 'target='+str(target) )

class PlayerRosters(AbstractParseable):
    def __init__(self):
        super().__init__()
    def parse(self, obj, target=None):
        super().parse( obj, target )

        # db.player.findOne({'parent_api__id':'rosters'})
        # {
        #     "_id" : "cGFyZW50X2FwaV9faWRyb3N0ZXJzdGVhbV9faWQ1ODNlYzc3My1mYjQ2LTExZTEtODJjYi1mNGNlNDY4NGVhNGNwYXJlbnRfbGlzdF9faWRwbGF5ZXJzX19saXN0aWQwOWQyNTE1NS1jM2JlLTQyNDYtYTk4Ni01NTkyMWExYjVlNjE=",
        #     "abbr_name" : "J.Jones",
        #     "birth_place" : "Miami, FL, USA",
        #     "birthdate" : "1980-10-04",
        #     "college" : "Miami",
        #     "experience" : 11,
        #     "first_name" : "James",
        #     "full_name" : "James Jones",
        #     "height" : 80,
        #     "id" : "09d25155-c3be-4246-a986-55921a1b5e61",
        #     "jersey_number" : 1,
        #     "last_name" : "Jones",
        #     "position" : "F-G",
        #     "primary_position" : "SF",
        #     "status" : "ACT",
        #     "updated" : "2014-12-08T03:48:40+00:00",
        #     "weight" : 215,
        #     "parent_api__id" : "rosters",
        #     "dd_updated__id" : NumberLong("1431472891718"),
        #     "team__id" : "583ec773-fb46-11e1-82cb-f4ce4684ea4c",
        #     "parent_list__id" : "players__list",
        #     "draft__list" : {
        #         "pick" : 49,
        #         "round" : 2,
        #         "team_id" : "583ec7cd-fb46-11e1-82cb-f4ce4684ea4c",
        #         "year" : 2003
        #     }
        # }

        o = obj.get_o()

        srid        = o.get('id')
        srid_team   = o.get('team__id')

        first_name  = o.get('first_name')
        last_name   = o.get('last_name')

        birth_place = o.get('birth_place', '')
        birthdate   = o.get('birthdate', '')
        college     = o.get('college', '')
        experience  = o.get('experience', 0.0)
        height      = o.get('height', 0.0)      # inches
        weight      = o.get('weight', 0.0)      # lbs.
        jersey_number       = o.get('jersey_number', 0.0)

        position            = o.get('position')
        primary_position    = o.get('primary_position')

        status              = o.get('status')   # roster status, ie: basically whether they are on it

        draft_pick      = o.get('draft__list.pick', '')
        draft_round     = o.get('draft__list.round', '')
        draft_year      = o.get('draft__list.year', '')
        srid_draft_team = o.get('draft__list.team_id', '')

        try:
            t = sports.nba.models.Team.objects.get(srid=srid_team)
        except sports.nba.models.Team.DoesNotExist:
            print( str(o) )
            print( 'Team for Player DoesNotExist!')
            return

        try:
            p = sports.nba.models.Player.objects.get(srid=srid)
        except sports.nba.models.Player.DoesNotExist:
            p = sports.nba.models.Player()
            p.srid = srid

        p.team          = t             # team could easily change of course
        p.first_name    = first_name
        p.last_name     = last_name

        p.birth_place   = birth_place
        p.birthdate     = birthdate
        p.college       = college
        p.experience    = experience
        p.height        = height
        p.weight        = weight
        p.jersey_number = jersey_number
        p.position      = position
        p.primary_position  = primary_position
        p.status        = status
        p.draft_pick    = draft_pick
        p.draft_round   = draft_round
        p.draft_year    = draft_year
        p.srid_draft_team = srid_draft_team

        p.save()

class TeamHierachy(AbstractParseable):
    def __init__(self):
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
            t = sports.nba.models.Team.objects.get( srid=srid )
        except sports.nba.models.Team.DoesNotExist:
            t = sports.nba.models.Team()
            t.srid      = srid
            t.save()

        t.srid_league       = srid_league
        t.srid_conference   = srid_conference
        t.srid_division     = srid_division
        t.market            = market
        t.name              = name
        t.alias             = alias
        t.srid_venue        = srid_venue

        t.save()

class GameSchedule(AbstractParseable):
    def __init__(self):
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
            h = sports.nba.models.Team.objects.get(srid=srid_home)
        except sports.nba.models.Team.DoesNotExist:
            print( str(o) )
            print( 'Team (home) for Game DoesNotExist! Have you parsed the "hierarchy" feed recently?')
            return

        try:
            a = sports.nba.models.Team.objects.get(srid=srid_away)
        except sports.nba.models.Team.DoesNotExist:
            print( str(o) )
            print( 'Team (away) for Game DoesNotExist! Have you parsed the "hierarchy" feed recently?')
            return

        try:
            g = sports.nba.models.Game.objects.get(srid=srid)
        except sports.nba.models.Game.DoesNotExist:
            g = sports.nba.models.Game()
            g.srid = srid

        g.home      = h
        g.away      = a
        g.start     = start
        g.status    = status
        g.srid_home = srid_home
        g.srid_away = srid_away
        g.title     = title
        g.save()

class GameStats(AbstractParseable):
    def __init__(self):
        super().__init__()

class PlayerStats(AbstractParseable):
    def __init__(self):
        super().__init__()
    def parse(self, obj, target=None):
        super().parse( obj, target )

        o = obj.get_o()
        srid_game   = o.get('game__id', None)
        srid_team   = o.get('team__id', None)
        srid_player = o.get('id', None)

        try:
            p = sports.nba.models.Player.objects.get(srid=srid_player)
        except sports.nba.models.Player.DoesNotExist:
            # first_name  = o.get('first_name', None)
            # last_name   = o.get('last_name', None)
            # full_name   = '%s %s' % (str(first_name), str(last_name))
            print( str(o) )
            print('Player object for PlayerStats DoesNotExist')
            return # dont create the playerstats then

        try:
            g = sports.nba.models.Game.objects.get(srid=srid_game)
        except sports.nba.models.Game.DoesNotExist:
            print( str(o) )
            print('Game object for PlayerStats DoesNotExist')
            return # dont create the playerstats then

        try:
            ps = sports.nba.models.PlayerStats.objects.get( srid_game=srid_game, srid_player=srid_player )

            ###### TODO
            # its possible we could save our hash value, and save this player
            # only if his stats have actually changed ! - maybe not the best idea

        except sports.nba.models.PlayerStats.DoesNotExist:
            ps = sports.nba.models.PlayerStats()
            ps.srid_game    = srid_game
            ps.srid_player  = srid_player
            ps.player  = p
            ps.game    = g

        #content_type    = models.ForeignKey(ContentType, related_name='nba_playerstats')

        #   { 'defensive_rebounds': 1.0,
        ps.defensive_rebounds = o.get('defensive_rebounds', 0.0)
        #         'two_points_pct': 0.6,
        ps.two_points_pct = o.get('two_points_pct', 0.0)
        #         'assists': 0.0,
        ps.assists = o.get('assists', 0.0)
        #         'free_throws_att': 2.0,
        ps.free_throws_att = o.get('free_throws_att', 0.0)
        #         'flagrant_fouls': 0.0,
        ps.flagrant_fouls = o.get('flagrant_fouls', 0.0)
        #         'offensive_rebounds': 1.0,
        ps.offensive_rebounds = o.get('offensive_rebounds', 0.0)
        #         'personal_fouls': 0.0,
        ps.personal_fouls = o.get('personal_fouls', 0.0)
        #         'field_goals_att': 5.0,
        ps.field_goals_att = o.get('field_goals_att', 0.0)
        #         'three_points_att': 0.0,
        ps.three_points_att = o.get('three_points_att', 0.0)
        #         'field_goals_pct': 60.0,
        ps.field_goals_pct = o.get('field_goals_pct', 0.0)
        #         'turnovers': 0.0,
        ps.turnovers = o.get('turnovers', 0.0)
        #         'points': 8.0,
        ps.points = o.get('points', 0.0)
        #         'rebounds': 2.0,
        ps.rebounds = o.get('rebounds', 0.0)
        #         'two_points_att': 5.0,
        ps.two_points_att = o.get('two_points_att', 0.0)
        #         'field_goals_made': 3.0,
        ps.field_goals_made = o.get('field_goals_made', 0.0)
        #         'blocked_att': 0.0,
        ps.blocked_att = o.get('blocked_att', 0.0)
        #         'free_throws_made': 2.0,
        ps.free_throws_made = o.get('free_throws_made', 0.0)
        #         'blocks': 0.0,
        ps.blocks = o.get('blocks', 0.0)
        #         'assists_turnover_ratio': 0.0,
        ps.assists_turnover_ratio = o.get('assists_turnover_ratio', 0.0)
        #         'tech_fouls': 0.0,
        ps.tech_fouls = o.get('tech_fouls', 0.0)
        #         'three_points_made': 0.0,
        ps.three_points_made = o.get('three_points_made', 0.0)
        #         'steals': 0.0,
        ps.steals = o.get('steals', 0.0)
        #         'two_points_made': 3.0,
        ps.two_points_made = o.get('two_points_made', 0.0)
        #         'free_throws_pct': 100.0,
        ps.free_throws_pct = o.get('free_throws_pct', 0.0)
        #         'three_points_pct': 0.0
        ps.three_points_pct = o.get('three_points_pct', 0.0)

        ps.save() # commit changes

        return ps

class PlayerPbp(AbstractParseable):
    def __init__(self):
        super().__init__()

class EventPbp(AbstractParseable):
    def __init__(self):
        super().__init__()

class DataDenNba(AbstractDataDenParser):

    def __init__(self):
        self.game_model = sports.nba.models.Game

    def parse(self, obj):
        """
        :param obj:
        :return:
        """
        super().parse( obj ) # setup self.ns, self.parent_api

        #
        # switch statement selects the type of object to parse
        # the Namespace-ParentApi combination

        #
        # nba.game
        if self.target == ('nba.game','schedule'): GameSchedule().parse( obj )
        #elif self.target == ('nba.game','stats'): GameStats().parse( obj )
        #
        # nba.team
        elif self.target == ('nba.team','hierarchy'): TeamHierachy().parse( obj )
        #
        # nba.player
        elif self.target == ('nba.player','rosters'): PlayerRosters().parse( obj )
        elif self.target == ('nba.player','stats'): PlayerStats().parse( obj )
        #elif self.target == ('nba.player','pbp'): PlayerPbp().parse( obj )
        #
        # nba.event
        #elif self.target == ('nba.event','pbp'): EventPbp().parse( obj )
        #
        # default case, print this message for now
        else: self.unimplemented( self.target[0], self.target[1] )
