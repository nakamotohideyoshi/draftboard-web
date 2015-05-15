#
#
import sports.mlb.models
from sports.sport.base_parser import AbstractDataDenParser
from dataden.util.timestamp import Parse as DataDenDatetime

class AbstractParseable(object):
    def __init__(self):
        self.name = self.__class__.__name__
    def parse(self, obj, target=None):
        print( self.name, str(obj)[:100], 'target='+str(target) )

class HomeAwaySummary(AbstractParseable):
    def __init__(self):
        super().__init__()
    def parse(self, obj, target=None):
        super().parse( obj, target )

        # db.home.findOne({'parent_api__id':'summary', 'game__id':'31781430-ed00-49c7-827f-e03a9a1e80d4'})
        # {
        #     "_id" : "cGFyZW50X2FwaV9faWRzdW1tYXJ5Z2FtZV9faWQzMTc4MTQzMC1lZDAwLTQ5YzctODI3Zi1lMDNhOWExZTgwZDRpZGM4NzRhMDY1LWMxMTUtNGU3ZC1iMGYwLTIzNTU4NGZiMGU2Zg==",
        #     "abbr" : "CIN",
        #     "errors" : 0,
        #     "hits" : 0,
        #     "id" : "c874a065-c115-4e7d-b0f0-235584fb0e6f",
        #     "market" : "Cincinnati",
        #     "name" : "Reds",
        #     "runs" : 0,
        #     "parent_api__id" : "summary",
        #     "dd_updated__id" : NumberLong("1431648742069"),
        #     "game__id" : "31781430-ed00-49c7-827f-e03a9a1e80d4",
        #     "probable_pitcher" : "1a574c70-eb33-4202-ab97-548645a4d15e",
        #     "starting_pitcher" : "1a574c70-eb33-4202-ab97-548645a4d15e",
        #     "roster__list" : [
        #         { "player" : "07af23d5-a3b9-4526-9e89-8c7f9f5facb4" },
        #         { "player" : "090ff436-c1e8-4927-b457-355cf4f9993b" }, ... more players
        #
        #     "lineup__list" : [
        #         { "player" : "07af23d5-a3b9-4526-9e89-8c7f9f5facb4" },
        #         { "player" : "090ff436-c1e8-4927-b457-355cf4f9993b" }, ... more players
        #     ],
        #     "scoring__list" : [
        #         {
        #             "inning" : {
        #                 "number" : 1,
        #                 "runs" : 0,
        #                 "sequence" : 1
        #             }
        #         },
        #         {
        #             "inning" : {
        #                 "number" : 2,
        #                 "runs" : 0,
        #                 "sequence" : 2
        #             }
        #         },
        #         {
        #             "inning" : {
        #                 "number" : 3,
        #                 "runs" : 0,
        #                 "sequence" : 3
        #             }
        #         },
        #         {
        #             "inning" : {
        #                 "number" : 4,
        #                 "runs" : "X",
        #                 "sequence" : 4
        #             }
        #         }
        #     ],
        #     "statistics__list" : {
        #         "hitting__list" : {
        #             "ab" : 8,
        #             "abhr" : 0,
        #             "abk" : 4,
        #             "ap" : 12,
        #             "avg" : 0,
        #             "babip" : 0,
        #             "bbk" : 2,
        #             "bbpa" : 0.333,
        #             "bip" : 6,
        #             "gofo" : 0.5,
        #             "iso" : 0,
        #             "lob" : 4,
        #             "obp" : 0.333,
        #             "ops" : 0.333,
        #             "pitch_count" : 59,
        #             "rbi" : 0,
        #             "seca" : 0.625,
        #             "slg" : 0,
        #             "xbh" : 0,
        #             "onbase__list" : {
        #                 "bb" : 4,
        #                 "d" : 0,
        #                 "fc" : 0,
        #                 "h" : 0,
        #                 "hbp" : 0,
        #                 "hr" : 0,
        #                 "ibb" : 0,
        #                 "roe" : 0,
        #                 "s" : 0,
        #                 "t" : 0,
        #                 "tb" : 0
        #             },
        #             "runs__list" : {
        #                 "earned" : 0,
        #                 "total" : 0,
        #                 "unearned" : 0
        #             },
        #             "outcome__list" : {
        #                 "ball" : 29,
        #                 "dirtball" : 2,
        #                 "foul" : 3,
        #                 "iball" : 0,
        #                 "klook" : 11,
        #                 "kswing" : 8,
        #                 "ktotal" : 19
        #             },
        #             "outs__list" : {
        #                 "fidp" : 0,
        #                 "fo" : 1,
        #                 "gidp" : 0,
        #                 "go" : 2,
        #                 "klook" : 1,
        #                 "kswing" : 1,
        #                 "ktotal" : 2,
        #                 "lidp" : 0,
        #                 "lo" : 3,
        #                 "po" : 0,
        #                 "sacfly" : 0,
        #                 "sachit" : 0
        #             },
        #             "steal__list" : {
        #                 "caught" : 1,
        #                 "pct" : 0.667,
        #                 "stolen" : 2
        #             }
        #         },
        #         "pitching__list" : {
        #             "bf" : 13,
        #             "era" : 6,
        #             "error" : 0,
        #             "gofo" : 0,
        #             "ip_1" : 9,
        #             "ip_2" : 3,
        #             "k9" : 6.003,
        #             "kbb" : 1,
        #             "lob" : 6,
        #             "oba" : 0.273,
        #             "pitch_count" : 50,
        #             "whip" : 1.667,
        #             "onbase__list" : {
        #                 "bb" : 2,
        #                 "d" : 1,
        #                 "fc" : 0,
        #                 "h" : 3,
        #                 "hbp" : 0,
        #                 "hr" : 0,
        #                 "ibb" : 0,
        #                 "roe" : 0,
        #                 "s" : 2,
        #                 "t" : 0,
        #                 "tb" : 4
        #             },
        #             "runs__list" : {
        #                 "earned" : 2,
        #                 "total" : 2,
        #                 "unearned" : 0
        #             },
        #             "outcome__list" : {
        #                 "ball" : 18,
        #                 "dirtball" : 0,
        #                 "foul" : 8,
        #                 "iball" : 0,
        #                 "klook" : 9,
        #                 "kswing" : 6,
        #                 "ktotal" : 15
        #             },
        #             "outs__list" : {
        #                 "fidp" : 0,
        #                 "fo" : 0,
        #                 "gidp" : 0,
        #                 "go" : 6,
        #                 "klook" : 0,
        #                 "kswing" : 2,
        #                 "ktotal" : 2,
        #                 "lidp" : 0,
        #                 "lo" : 0,
        #                 "po" : 0,
        #                 "sacfly" : 0,
        #                 "sachit" : 0
        #             },
        #             "steal__list" : {
        #                 "caught" : 1,
        #                 "stolen" : 0
        #             },
        #             "games__list" : {
        #                 "blown_save" : 0,
        #                 "complete" : 0,
        #                 "hold" : 0,
        #                 "loss" : 0,
        #                 "qstart" : 0,
        #                 "save" : 0,
        #                 "shutout" : 0,
        #                 "svo" : 0,
        #                 "win" : 0
        #             }
        #         },
        #         "fielding__list" : {
        #             "a" : 9,
        #             "dp" : 0,
        #             "error" : 0,
        #             "fpct" : 1,
        #             "po" : 9,
        #             "tc" : 18,
        #             "tp" : 0
        #         }
        #     },
        #     "players__list" : [
        #         { "player" : "07af23d5-a3b9-4526-9e89-8c7f9f5facb4" },
        #         { "player" : "090ff436-c1e8-4927-b457-355cf4f9993b" }, ... more players who played
        #     ]
        # }

        o = obj.get_o()


class GameBoxscores(AbstractParseable):
    def __init__(self):
        super().__init__()
    def parse(self, obj, target=None):
        super().parse( obj, target )

        # FOR A CLOSED GAME!!!!
        # db.game.findOne({'parent_api__id':'boxscores', 'status':'closed'})  # NOTE: 'status':'closed'
        # {
        #     "_id" : "cGFyZW50X2FwaV9faWRib3hzY29yZXNpZGM4MjQ1NmFjLWE0YjktNGNhZi04MTI0LTBhZmE3NGY5Y2YzNA==",
        #     "attendance" : 37441,
        #     "away_team" : "27a59d3b-ff7c-48ea-b016-4798f560f5e1",
        #     "coverage" : "full",
        #     "day_night" : "N",
        #     "game_number" : 1,
        #     "home_team" : "43a39081-52b4-4f93-ad29-da7f329ea960",
        #     "id" : "c82456ac-a4b9-4caf-8124-0afa74f9cf34",
        #     "scheduled" : "2015-05-10T01:10:00+00:00",
        #     "status" : "closed",
        #     "xmlns" : "http://feed.elasticstats.com/schema/baseball/v5/game.xsd",
        #     "parent_api__id" : "boxscores",
        #     "dd_updated__id" : NumberLong("1431234264301"),
        #     "venue" : "f1c03dac-3c0f-437c-a325-8d5702cd321a",
        #     "broadcast__list" : {
        #         "network" : "ROOT SPORTS"
        #     },
        #     "final__list" : {  ##### when the game is OVER it holds this
        #         "inning" : 9,
        #         "inning_half" : "T"
        #     },
        #     "home" : "43a39081-52b4-4f93-ad29-da7f329ea960",
        #     "away" : "27a59d3b-ff7c-48ea-b016-4798f560f5e1",
        #     "pitching__list" : {
        #         "win__list" : {
        #             "player" : "9760f1d6-9560-45ed-bc73-5ec2205905a2"
        #         },
        #         "loss__list" : {
        #             "player" : "a193c72e-e252-49c4-8ae5-2836039afda7"
        #         },
        #         "hold__list" : {
        #             "player" : "6f61629a-8c64-4469-b67a-48d470b7c990"
        #         }
        #     }
        # }

        #### FOR AN ACTIVE GAME!!! ...
        # db.game.findOne({'parent_api__id':'boxscores', 'status':'inprogress'})
        # {
        #     "_id" : "cGFyZW50X2FwaV9faWRib3hzY29yZXNpZDMxNzgxNDMwLWVkMDAtNDljNy04MjdmLWUwM2E5YTFlODBkNA==",
        #     "away_team" : "a7723160-10b7-4277-a309-d8dd95a8ae65",
        #     "coverage" : "full",
        #     "day_night" : "N",
        #     "game_number" : 1,
        #     "home_team" : "c874a065-c115-4e7d-b0f0-235584fb0e6f",
        #     "id" : "31781430-ed00-49c7-827f-e03a9a1e80d4",
        #     "scheduled" : "2015-05-14T23:10:00+00:00",
        #     "status" : "inprogress",
        #     "xmlns" : "http://feed.elasticstats.com/schema/baseball/v5/game.xsd",
        #     "parent_api__id" : "boxscores",
        #     "dd_updated__id" : NumberLong("1431645673334"),
        #     "venue" : "f102d8fb-de67-4b86-9053-8b55f578d45c",
        #     "broadcast__list" : {
        #         "network" : "FS-O"
        #     },
        #     "outcome__list" : {
        #         "current_inning" : 1,
        #         "current_inning_half" : "T",
        #         "type" : "pitch",
        #         "count__list" : {
        #             "balls" : 1,
        #             "half_over" : "false",
        #             "inning" : 1,
        #             "inning_half" : "T",
        #             "outs" : 1,
        #             "strikes" : 2
        #         },
        #         "hitter" : "36ee970b-0cff-4d50-b8ac-9bd16fae2dd1",
        #         "pitcher" : "1a574c70-eb33-4202-ab97-548645a4d15e",
        #         "runners__list" : [
        #             {
        #                 "runner" : "898c62b6-95bf-4973-a435-c6cb42a52158"
        #             },
        #             {
        #                 "runner" : "e47bf865-f612-47f6-8a21-3110bb455e31"
        #             }
        #         ]
        #     },
        #     "home" : "c874a065-c115-4e7d-b0f0-235584fb0e6f",
        #     "away" : "a7723160-10b7-4277-a309-d8dd95a8ae65"
        # }

        o = obj.get_o()

class TeamHierarchy(AbstractParseable):
    def __init__(self):
        super().__init__()
    def parse(self, obj, target=None):
        super().parse( obj, target )

        # db.team.findOne({'parent_api__id':'hierarchy'})
        # {
        #     "_id" : "cGFyZW50X2FwaV9faWRoaWVyYXJjaHlsZWFndWVfX2lkMmVhNmVmZTctMmUyMS00ZjI5LTgwYTItMGEyNGFkMWY1Zjg1ZGl2aXNpb25fX2lkMWQ3NGU4ZTktN2ZhZi00Y2RiLWI2MTMtMzk0NGZhNWFhNzM5aWQxZDY3ODQ0MC1iNGIxLTQ5NTQtOWIzOS03MGFmYjNlYmJjZmE=",
        #     "abbr" : "TOR",
        #     "id" : "1d678440-b4b1-4954-9b39-70afb3ebbcfa",
        #     "market" : "Toronto",
        #     "name" : "Blue Jays",
        #     "parent_api__id" : "hierarchy",
        #     "dd_updated__id" : NumberLong("1431469575341"),
        #     "league__id" : "2ea6efe7-2e21-4f29-80a2-0a24ad1f5f85",
        #     "division__id" : "1d74e8e9-7faf-4cdb-b613-3944fa5aa739",
        #     "venue" : "84d72338-2173-4a90-9d25-99adc6c86f4b"
        # }
        o = obj.get_o()
        srid            = o.get('id', None)
        srid_league     = o.get('league__id',   None)
        srid_division   = o.get('division__id', None)
        market          = o.get('market',       None)
        name            = o.get('name',         None)
        alias           = o.get('abbr',         None)  # mlb calls alias "abbr"
        srid_venue      = o.get('venue',        '')

        try:
            t = sports.mlb.models.Team.objects.get( srid=srid )
        except sports.mlb.models.Team.DoesNotExist:
            t = sports.mlb.models.Team()
            t.srid      = srid
            t.save()

        t.srid_league       = srid_league
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
        super().parse(obj, target)

        # {
        #     "_id" : "cGFyZW50X2FwaV9faWRzY2hlZHVsZV9yZWdsZWFndWVfX2lkMmZhNDQ4YmMtZmMxNy00ZDNkLWJlMDMtZTYwZTA4MGZkYzI2c2Vhc29uLXNjaGVkdWxlX19pZDk1MjNmMDM5LTA3MGMtNDlkMS1iMmUzLTVmMThiNTdjNWVlM3BhcmVudF9saXN0X19pZGdhbWVzX19saXN0aWQwMDI1NWYyNC0zNGI1LTQ4MDgtODRkOS04NjNkNDA5Nzc2ODU=",
        #     "attendance" : 41545,
        #     "away_team" : "25507be1-6a68-4267-bd82-e097d94b359b",
        #     "coverage" : "full",
        #     "day_night" : "N",
        #     "game_number" : 1,
        #     "home_team" : "a7723160-10b7-4277-a309-d8dd95a8ae65",
        #     "id" : "00255f24-34b5-4808-84d9-863d40977685",
        #     "scheduled" : "2015-04-17T02:15:00+00:00",
        #     "status" : "closed",
        #     "parent_api__id" : "schedule_reg",
        #     "dd_updated__id" : NumberLong("1431469581209"),
        #     "league__id" : "2fa448bc-fc17-4d3d-be03-e60e080fdc26",
        #     "season_schedule__id" : "9523f039-070c-49d1-b2e3-5f18b57c5ee3",
        #     "parent_list__id" : "games__list",
        #     "venue" : "2d7542f5-7b80-49f7-9b24-c53ffdc75af6",
        #     "home" : "a7723160-10b7-4277-a309-d8dd95a8ae65",
        #     "away" : "25507be1-6a68-4267-bd82-e097d94b359b",
        #     "broadcast__list" : {
        #         "network" : "CSN-BA"
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

        attendance  = o.get('attendance',   0)
        day_night   = o.get('day_night',    None)
        game_number = o.get('game_number',  None)

        srid_venue  = o.get('venue', '')

        try:
            h = sports.mlb.models.Team.objects.get(srid=srid_home)
        except sports.mlb.models.Team.DoesNotExist:
            print( str(o) )
            print( 'Team (home) for Game DoesNotExist! Have you parsed the "hierarchy" feed recently?')
            return

        try:
            a = sports.mlb.models.Team.objects.get(srid=srid_away)
        except sports.mlb.models.Team.DoesNotExist:
            print( str(o) )
            print( 'Team (away) for Game DoesNotExist! Have you parsed the "hierarchy" feed recently?')
            return

        try:
            g = sports.mlb.models.Game.objects.get(srid=srid)
        except sports.mlb.models.Game.DoesNotExist:
            g = sports.mlb.models.Game()
            g.srid = srid

        g.home      = h
        g.away      = a
        g.start     = start
        g.status    = status
        g.srid_home = srid_home
        g.srid_away = srid_away
        g.title     = title

        g.attendance    = attendance
        g.day_night     = day_night
        g.game_number   = game_number

        g.srid_venue    = srid_venue

        g.save()

class GameStats(AbstractParseable):
    def __init__(self):
        super().__init__()
    def parse(self, obj, target=None):
        super().parse( obj, target )

# PlayerTeamProfile
class PlayerTeamProfile(AbstractParseable):
    def __init__(self):
        super().__init__()
    def parse(self, obj, target=None):
        super().parse( obj, target )

        # db.player.findOne({'parent_api__id':'team_profile'})
        # {
        #     "_id" : "cGFyZW50X2FwaV9faWR0ZWFtX3Byb2ZpbGV0ZWFtX19pZDU1NzE0ZGE4LWZjYWYtNDU3NC04NDQzLTU5YmZiNTExYTUyNHBhcmVudF9saXN0X19pZHBsYXllcnNfX2xpc3RpZDRhNDAzNjNmLTMxZjUtNDg3ZS1iNjEzLWU1NDU2ZjBmMDc1Mw==",
        #     "bat_hand" : "R",
        #     "birthcity" : "San Isidro",
        #     "birthcountry" : "Dominican Republic",
        #     "birthdate" : "1987-04-24",
        #     "first_name" : "Welington",
        #     "full_name" : "Welington Castillo",
        #     "height" : 70,
        #     "id" : "4a40363f-31f5-487e-b613-e5456f0f0753",
        #     "jersey_number" : 5,
        #     "last_name" : "Castillo",
        #     "mlbam_id" : 456078,
        #     "position" : "C",
        #     "preferred_name" : "Welington",
        #     "primary_position" : "C",
        #     "pro_debut" : "2010-08-11",
        #     "status" : "A",
        #     "throw_hand" : "R",
        #     "updated" : "2014-06-22T15:29:36+00:00",
        #     "weight" : 210,
        #     "parent_api__id" : "team_profile",
        #     "dd_updated__id" : NumberLong("1431545632159"),
        #     "team__id" : "55714da8-fcaf-4574-8443-59bfb511a524",
        #     "parent_list__id" : "players__list"
        # }

        o = obj.get_o()

        srid        = o.get('id')
        srid_team   = o.get('team__id')

        preferred_name = o.get('preferred_name', None)
        first_name  = o.get('first_name')
        last_name   = o.get('last_name')

        birthcity   = o.get('birthcity', '')
        birthcountry = o.get('birthcountry', '')
        birthdate   = o.get('birthdate', '')

        height      = o.get('height', 0.0)      # inches
        weight      = o.get('weight', 0.0)      # lbs.
        jersey_number       = o.get('jersey_number', 0.0)

        position            = o.get('position')
        primary_position    = o.get('primary_position')

        status              = o.get('status')   # roster status, ie: basically whether they are on it

        pro_debut       = o.get('pro_debut',    '')
        throw_hand      = o.get('throw_hand',   '')
        bat_hand        = o.get('bat_hand',     '')

        try:
            t = sports.mlb.models.Team.objects.get(srid=srid_team)
        except sports.mlb.models.Team.DoesNotExist:
            print( str(o) )
            print( 'Team for Player DoesNotExist!')
            return

        try:
            p = sports.mlb.models.Player.objects.get(srid=srid)
        except sports.mlb.models.Player.DoesNotExist:
            p = sports.mlb.models.Player()
            p.srid = srid

        p.team          = t             # team could easily change of course
        p.first_name    = first_name
        p.preferred_name = preferred_name
        p.last_name     = last_name

        p.birthcity     = birthcity
        p.birthcountry  = birthcountry
        p.birthdate     = birthdate

        p.height        = height
        p.weight        = weight
        p.jersey_number = jersey_number
        p.position      = position
        p.primary_position  = primary_position
        p.status        = status

        p.pro_debut     = pro_debut
        p.throw_hand    = throw_hand
        p.bat_hand      = bat_hand

        p.save()

class PlayerStats(AbstractParseable):
    def __init__(self):
        super().__init__()
    def parse(self, obj, target=None):
        super().parse( obj, target )

        #     {
        #     "_id" : "cGFyZW50X2FwaV9faWRzdW1tYXJ5Z2FtZV9faWRjODI0NTZhYy1hNGI5LTRjYWYtODEyNC0wYWZhNzRmOWNmMzRob21lX19pZDQzYTM5MDgxLTUyYjQtNGY5My1hZDI5LWRhN2YzMjllYTk2MHBhcmVudF9saXN0X19pZHBsYXllcnNfX2xpc3RpZDAxZWFmZjU5LTliMzQtNDdmZC1hZjY0LTU0YjJlNmYyMjYyOA==",
        #     "first_name" : "Nelson",
        #     "id" : "01eaff59-9b34-47fd-af64-54b2e6f22628",
        #     "jersey_number" : 23,
        #     "last_name" : "Cruz",
        #     "position" : "OF",
        #     "preferred_name" : "Nelson",
        #     "primary_position" : "LF",
        #     "status" : "A",
        #     "parent_api__id" : "summary",
        #     "dd_updated__id" : NumberLong("1431231070789"),
        #     "game__id" : "c82456ac-a4b9-4caf-8124-0afa74f9cf34",
        #     "home__id" : "43a39081-52b4-4f93-ad29-da7f329ea960",
        #     "parent_list__id" : "players__list",
        #     "statistics__list" : {
        #         "hitting__list" : {
        #             "ab" : 3,
        #             "abhr" : 0,
        #             "abk" : 0,
        #             "ap" : 4,
        #             "avg" : 0.667,
        #             "babip" : 0.667,
        #             "bbk" : 0,
        #             "bbpa" : 0.25,
        #             "bip" : 3,
        #             "gofo" : 0,
        #             "iso" : 0.333,
        #             "lob" : 0,
        #             "obp" : 0.75,
        #             "ops" : 1.75,
        #             "pitch_count" : 14,
        #             "rbi" : 1,
        #             "seca" : 0.667,
        #             "slg" : 1,
        #             "xbh" : 1,
        #             "onbase__list" : {
        #                 "bb" : 1,
        #                 "d" : 1,
        #                 "fc" : 0,
        #                 "h" : 2,
        #                 "hbp" : 0,
        #                 "hr" : 0,
        #                 "ibb" : 0,
        #                 "roe" : 0,
        #                 "s" : 1,
        #                 "t" : 0,
        #                 "tb" : 3
        #             },
        #             "runs__list" : {
        #                 "earned" : 1,
        #                 "total" : 1,
        #                 "unearned" : 0
        #             },
        #             "outcome__list" : {
        #                 "ball" : 6,
        #                 "dirtball" : 1,
        #                 "foul" : 0,
        #                 "iball" : 0,
        #                 "klook" : 2,
        #                 "kswing" : 2,
        #                 "ktotal" : 4
        #             },
        #             "outs__list" : {
        #                 "fidp" : 0,
        #                 "fo" : 0,
        #                 "gidp" : 0,
        #                 "go" : 1,
        #                 "klook" : 0,
        #                 "kswing" : 0,
        #                 "ktotal" : 0,
        #                 "lidp" : 0,
        #                 "lo" : 0,
        #                 "po" : 0,
        #                 "sacfly" : 0,
        #                 "sachit" : 0
        #             },
        #             "steal__list" : {
        #                 "caught" : 0,
        #                 "pct" : 0,
        #                 "stolen" : 0
        #             },
        #             "games__list" : {
        #                 "complete" : 0,
        #                 "finish" : 0,
        #                 "play" : 0,
        #                 "start" : 0
        #             }
        #         },
        #         "fielding__list" : {
        #             "a" : 0,
        #             "dp" : 0,
        #             "error" : 0,
        #             "fpct" : 1,
        #             "po" : 4,
        #             "rf" : 0,
        #             "tc" : 4,
        #             "tp" : 0,
        #             "games__list" : {
        #                 "complete" : 0,
        #                 "finish" : 0,
        #                 "play" : 0,
        #                 "start" : 0
        #             }
        #         }
        #     }
        # }


        # "pitching__list" : {
		# 	"bf" : 3,
		# 	"era" : 0,
		# 	"error" : 0,
		# 	"gofo" : 0,
		# 	"ip_1" : 3,
		# 	"ip_2" : 1,
		# 	"k9" : 18,
		# 	"kbb" : 0,
		# 	"lob" : 0,
		# 	"oba" : 0,
		# 	"pitch_count" : 15,
		# 	"whip" : 0,
		# 	"onbase__list" : {
		# 		"bb" : 0,
		# 		"d" : 0,
		# 		"fc" : 0,
		# 		"h" : 0,
		# 		"hbp" : 0,
		# 		"hr" : 0,
		# 		"ibb" : 0,
		# 		"roe" : 0,
		# 		"s" : 0,
		# 		"t" : 0,
		# 		"tb" : 0
		# 	},
		# 	"runs__list" : {
		# 		"earned" : 0,
		# 		"total" : 0,
		# 		"unearned" : 0
		# 	},
		# 	"outcome__list" : {
		# 		"ball" : 5,
		# 		"dirtball" : 0,
		# 		"foul" : 4,
		# 		"iball" : 0,
		# 		"klook" : 4,
		# 		"kswing" : 1,
		# 		"ktotal" : 5
		# 	},
		# 	"outs__list" : {
		# 		"fidp" : 0,
		# 		"fo" : 1,
		# 		"gidp" : 0,
		# 		"go" : 0,
		# 		"klook" : 2,
		# 		"kswing" : 0,
		# 		"ktotal" : 2,
		# 		"lidp" : 0,
		# 		"lo" : 0,
		# 		"po" : 0,
		# 		"sacfly" : 0,
		# 		"sachit" : 0
		# 	},
		# 	"steal__list" : {
		# 		"caught" : 0,
		# 		"stolen" : 0
		# 	},
		# 	"games__list" : {
		# 		"blown_save" : 0,
		# 		"complete" : 0,
		# 		"finish" : 0,
		# 		"hold" : 0,
		# 		"loss" : 0,
		# 		"play" : 1,
		# 		"qstart" : 0,
		# 		"save" : 0,
		# 		"shutout" : 0,
		# 		"start" : 0,
		# 		"svo" : 0,
		# 		"win" : 0
		# 	}
		# },

        # db.player.distinct('primary_position')
        # >>> [ "1B", "LF", "3B", "CF", "RF", "C", "2B", "SP", "RP", "SS", "DH" ]
        o = obj.get_o()
        srid_game   = o.get('game__id', None)
        srid_player = o.get('id', None)

        fielding = o.get('fielding__list', {}) # info about whether they played/started the game
        game_info = fielding.get('games__list', {})

        try:
            p = sports.mlb.models.Player.objects.get(srid=srid_player)
        except sports.mlb.models.Player.DoesNotExist:
            print( str(o) )
            print('Player object for PlayerStats DoesNotExist')
            return # dont create the playerstats then

        try:
            g = sports.mlb.models.Game.objects.get(srid=srid_game)
        except sports.mlb.models.Game.DoesNotExist:
            print( str(o) )
            print('Game object for PlayerStats DoesNotExist')
            return # dont create the playerstats then

        #
        # decide whether this is a hitter or pitcher here, based on 'position'
        position = o.get('position')  # ['IF','OF','C','P','DH']
        if position == 'P':
            # its a pitcher
            try:
                ps = sports.mlb.models.PlayerStatsPitcher.objects.get( srid_game=srid_game, srid_player=srid_player )
            except sports.mlb.models.PlayerStatsPitcher.DoesNotExist:
                ps = sports.mlb.models.PlayerStatsPitcher()
                ps.srid_game    = srid_game
                ps.srid_player  = srid_player
                ps.player  = p
                ps.game    = g

            # collect pitching stats
            statistics = o.get('statistics__list', {}) # default will useful if it doenst exist
            print('')
            print( statistics )
            pitching = statistics.get('pitching__list', {})
            print('')
            print( pitching )
            games   = pitching.get('games__list', {})
            onbase  = pitching.get('onbase__list', {})
            runs    = pitching.get('runs__list', {})
            steals  = pitching.get('steal__list', {})
            outs    = pitching.get('outs__list', {})

            ps.ip_1    = pitching.get('ip_1', 0.0) # outs, basically. for 1 inning pitched == 3 (4 possible?)
            ps.ip_2    = pitching.get('ip_2', 0.0) # 1 == one inning pitched
            ps.win     = bool( games.get('win', 0) )
            ps.loss    = bool( games.get('loss', 0) )
            ps.qstart  = bool( games.get('qstart', 0) )
            ps.ktotal  = outs.get('ktotal', 0)
            ps.er      = runs.get('earned', 0)  # earned runs allowed
            ps.r_total = runs.get('total', 0)   # total runs allowed (earned and unearned)
            ps.h       = onbase.get('h', 0)     # hits against
            ps.bb      = onbase.get('bb', 0)    # walks against
            ps.hbp     = onbase.get('hbp', 0)   # hit batsmen
            ps.cg      = bool( games.get('complete', 0) ) # complete game
            ps.cgso    = bool( games.get('shutout', 0) ) and ps.cg # complete game shut out
            ps.nono    = bool( ps.h ) and ps.cg # no hitter if hits == 0, and complete game

            ps.save() # commit changes

        else:
            # its a hitter
            try:
                ps = sports.mlb.models.PlayerStatsHitter.objects.get( srid_game=srid_game, srid_player=srid_player )
            except sports.mlb.models.PlayerStatsHitter.DoesNotExist:
                ps = sports.mlb.models.PlayerStatsHitter()
                ps.srid_game    = srid_game
                ps.srid_player  = srid_player
                ps.player  = p
                ps.game    = g

            statistics = o.get('statistics__list', {})
            print('')
            print( statistics )
            hitting = statistics.get('hitting__list', {}) # default will useful if it doenst exist
            print('')
            print( hitting )
            onbase  = hitting.get('onbase__list', {})
            runs    = hitting.get('runs__list', {})
            steals  = hitting.get('steal__list', {})
            outs    = hitting.get('outs__list', {})

            ps.bb  = onbase.get('bb', 0)
            ps.s   = onbase.get('s', 0)
            ps.d   = onbase.get('d', 0)
            ps.t   = onbase.get('t', 0)
            ps.hr  = onbase.get('hr', 0)
            ps.rbi = hitting.get('rbi', 0)
            ps.r   = runs.get('total', 0)
            ps.hbp = onbase.get('hbp', 0)
            ps.sb  = steals.get('stolen', 0)
            ps.cs  = steals.get('caught', 0)

            ps.ktotal  = outs.get('ktotal', 0)

            ps.ab  = hitting.get('ab', 0)
            ps.ap  = hitting.get('ap', 0)
            ps.lob = hitting.get('lob', 0)
            ps.xbh = hitting.get('xhb', 0)

            ps.save() # commit changes

        ps.play = bool( game_info.get('play', 0) )
        ps.start = bool( game_info.get('start', 0) )

        return ps

class PlayerPbp(AbstractParseable):
    def __init__(self):
        super().__init__()

class EventPbp(AbstractParseable):
    def __init__(self):
        super().__init__()

class DataDenMlb(AbstractDataDenParser):

    def __init__(self):
        self.game_model = sports.mlb.models.Game

    def parse(self, obj):
        super().parse( obj ) # setup self.ns, self.parent_api

        #
        # game
        if self.target == ('mlb.game','schedule_reg'): GameSchedule().parse( obj )
        elif self.target == ('mlb.game','schedule_pre'): GameSchedule().parse( obj )
        elif self.target == ('mlb.game','schedule_pst'): GameSchedule().parse( obj )

        elif self.target == ('mlb.game','boxscores'): GameBoxscores().parse( obj )  # top level boxscore info
        elif self.target == ('mlb.home','summary'): HomeAwaySummary().parse( obj )  # home team of boxscore
        elif self.target == ('mlb.away','summary'): HomeAwaySummary().parse( obj )  # away team of boxscore

        #
        # team
        elif self.target == ('mlb.team','hierarchy'): TeamHierarchy().parse( obj ) # parse each team
        #
        # player
        elif self.target == ('mlb.player','team_profile'): PlayerTeamProfile().parse( obj ) # ie: rosters
        elif self.target == ('mlb.player','summary'): PlayerStats().parse( obj ) # stats from games
        #
        # default case, print this message for now
        else: self.unimplemented( self.target[0], self.target[1] )
