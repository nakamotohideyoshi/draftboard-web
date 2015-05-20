#
# scoring/tests.py

import itertools
import sports.nba.models
from django.test import TestCase
from test.classes import AbstractTest
from scoring.classes import NbaSalaryScoreSystem
from dataden.util.timestamp import Parse as DataDenDatetime

class NbaScoringTest(AbstractTest):
    """
    Test the scoring system for NBA.  The test method will be:
        - Create a dummy player in the Postgres database with all stats set to 0
        - Increment individual stats and compare the calculated point value against the scoring system projected value
        - Increment groups of stars and compare the calculated point value against the scoring system projected value
    """

    def setUp(self):
        self.create_team()
        self.create_game()
        self.create_player()
        self.player_stats = self.create_player_stats()
        self.nba_Salary_Score_System = NbaSalaryScoreSystem()

    def create_team(self):
        srid            = "583ecea6-fb46-11e1-82cb-f4ce4684ea4c"
        srid_league     = "4353138d-4c22-4396-95d8-5f587d2df25c"
        srid_conference = "3960cfac-7361-4b30-bc25-8d393de6f62f"
        srid_division   = "54dc7348-c1d2-40d8-88b3-c4c0138e085d"
        market          = "Miami"
        name            = "Heat"
        alias           = "MIA"
        srid_venue      = "b67d5f09-28b2-5bc6-9097-af312007d2f4"

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

    def create_player(self):
        srid        = "09d25155-c3be-4246-a986-55921a1b5e61"
        srid_team   = "583ecea6-fb46-11e1-82cb-f4ce4684ea4c"

        first_name  = "James"
        last_name   = "Jones"

        birth_place = "Miami, FL, USA"
        birthdate   = "1980-10-04"
        college     = "Miami"
        experience  = 11
        height      = 80      # inches
        weight      = 215      # lbs.
        jersey_number       = 1

        position            = "F-G"
        primary_position    = "SF"

        status              = "ACT"   # roster status, ie: basically whether they are on it

        draft_pick      = 49
        draft_round     = 2
        draft_year      = 2003
        srid_draft_team = "583ecea6-fb46-11e1-82cb-f4ce4684ea4c"

        t = sports.nba.models.Team.objects.get(srid=srid_team)

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

    def create_game(self):
        srid        = "5fbd3295-32ca-445f-baf5-c7c008351398"
        start_str   = "2015-04-18T16:30:00+00:00"
        start       = DataDenDatetime.from_string( start_str )
        status      = "closed"

        srid_home   = "583ecea6-fb46-11e1-82cb-f4ce4684ea4c"
        srid_away   = "583ecea6-fb46-11e1-82cb-f4ce4684ea4c"
        title       = "Game 1"

        h = sports.nba.models.Team.objects.get(srid=srid_home)
        a = sports.nba.models.Team.objects.get(srid=srid_away)

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

    def create_player_stats(self):
        srid_game   = "5fbd3295-32ca-445f-baf5-c7c008351398"
        srid_player = "09d25155-c3be-4246-a986-55921a1b5e61"

        p = sports.nba.models.Player.objects.get(srid=srid_player)
        g = sports.nba.models.Game.objects.get(srid=srid_game)

        try:
            ps = sports.nba.models.PlayerStats.objects.get( srid_game=srid_game, srid_player=srid_player )
        except sports.nba.models.PlayerStats.DoesNotExist:
            ps = sports.nba.models.PlayerStats()
            ps.srid_game    = srid_game
            ps.srid_player  = srid_player
            ps.player  = p
            ps.game    = g

        #content_type    = models.ForeignKey(ContentType, related_name='nba_playerstats')

        ps.defensive_rebounds =  0.0
        ps.two_points_pct = 0.0
        ps.assists = 0.0
        ps.free_throws_att = 0.0
        ps.flagrant_fouls = 0.0
        ps.offensive_rebounds = 0.0
        ps.personal_fouls = 0.0
        ps.field_goals_att = 0.0
        ps.three_points_att = 0.0
        ps.field_goals_pct = 0.0
        ps.turnovers = 0.0
        ps.points = 0.0
        ps.rebounds = 0.0
        ps.two_points_att = 0.0
        ps.field_goals_made = 0.0
        ps.blocked_att = 0.0
        ps.free_throws_made = 0.0
        ps.blocks = 0.0
        ps.assists_turnover_ratio = 0.0
        ps.tech_fouls = 0.0
        ps.three_points_made = 0.0
        ps.steals = 0.0
        ps.two_points_made = 0.0
        ps.free_throws_pct = 0.0
        ps.three_points_pct = 0.0

        ps.save() # commit changes

        return ps

    def update_player_stats(self, stat_list):
        for stat in stat_list.keys():
            setattr(self.player_stats, stat, stat_list[stat])
        self.player_stats.save()

    def test_stats_all_0(self):
        self.assertAlmostEquals(self.nba_Salary_Score_System.score_player(self.player_stats), 0)

    def test_all_unused_stats(self):
        # Set all unused stats values to 10 and make sure that the total points calculated is still 0
        unused_stats = {
            'defensive_rebounds': 10.0,
            'two_points_pct': 10.0,
            'free_throws_att': 10.0,
            'flagrant_fouls': 10.0,
            'offensive_rebounds': 10.0,
            'personal_fouls': 10.0,
            'field_goals_att': 10.0,
            'three_points_att': 10.0,
            'field_goals_pct': 10.0,
            'two_points_att': 10.0,
            'field_goals_made': 10.0,
            'blocked_att': 10.0,
            'free_throws_made': 10.0,
            'assists_turnover_ratio': 10.0,
            'tech_fouls': 10.0,
            'two_points_made': 10.0,
            'free_throws_pct': 10.0,
            'three_points_pct': 10.0
        }
        self.create_player_stats()
        self.update_player_stats(unused_stats)
        self.assertAlmostEquals(self.nba_Salary_Score_System.score_player(self.player_stats), 0)

    def test_points(self):
        # Test various values of points to make sure the calculations are correct
        self.create_player_stats()
        for points in range(0, 101, 10):
            self.update_player_stats({'points': points})
            multiplier = self.nba_Salary_Score_System.get_value_of('point')
            self.assertAlmostEquals(self.nba_Salary_Score_System.score_player(self.player_stats), points * multiplier)

    def test_three_points_made(self):
        # Test various values of three_points_made to make sure the calculations are correct
        self.create_player_stats()
        for three_points_made in range(0, 101, 10):
            self.update_player_stats({'three_points_made': three_points_made})
            multiplier = self.nba_Salary_Score_System.get_value_of('three_pm')
            self.assertAlmostEquals(self.nba_Salary_Score_System.score_player(self.player_stats), three_points_made * multiplier)

    def test_rebounds(self):
        # Test various values of rebounds to make sure the calculations are correct
        self.create_player_stats()
        for rebounds in range(0, 101, 10):
            self.update_player_stats({'rebounds': rebounds})
            multiplier = self.nba_Salary_Score_System.get_value_of('rebound')
            self.assertAlmostEquals(self.nba_Salary_Score_System.score_player(self.player_stats), rebounds * multiplier)

    def test_assists(self):
        # Test various values of assists to make sure the calculations are correct
        self.create_player_stats()
        for assists in range(0, 101, 10):
            self.update_player_stats({'assists': assists})
            multiplier = self.nba_Salary_Score_System.get_value_of('assist')
            self.assertAlmostEquals(self.nba_Salary_Score_System.score_player(self.player_stats), assists * multiplier)

    def test_steals(self):
        # Test various values of steals to make sure the calculations are correct
        self.create_player_stats()
        for steals in range(0, 101, 10):
            self.update_player_stats({'steals': steals})
            multiplier = self.nba_Salary_Score_System.get_value_of('steal')
            self.assertAlmostEquals(self.nba_Salary_Score_System.score_player(self.player_stats), steals * multiplier)

    def test_blocks(self):
        # Test various values of blocks to make sure the calculations are correct
        self.create_player_stats()
        for blocks in range(0, 101, 10):
            self.update_player_stats({'blocks': blocks})
            multiplier = self.nba_Salary_Score_System.get_value_of('block')
            self.assertAlmostEquals(self.nba_Salary_Score_System.score_player(self.player_stats), blocks * multiplier)

    def test_turnovers(self):
        # Test various values of turnovers to make sure the calculations are correct
        self.create_player_stats()
        for turnovers in range(0, 101, 10):
            self.update_player_stats({'turnovers': turnovers})
            multiplier = self.nba_Salary_Score_System.get_value_of('turnover')
            self.assertAlmostEquals(self.nba_Salary_Score_System.score_player(self.player_stats), turnovers * multiplier)

    def test_double_double_and_triple_double(self):
        """
        Test various values of stats to make sure the calculations are correct for double doubles and triple doubles.
        If exactly two stats are >= 10.0, a double double bonus should be given.
        If three or more stats are >= 10.0, a triple double bonus should be given.
        This test also tests multiple stats values set simultaneously.
        """
        self.create_player_stats()
        for points, rebounds, assists, steals, blocks in itertools.product(range(0, 21, 15), range(5, 15, 8),
                                                                           range(2, 13, 10), range(3, 11, 7),
                                                                           range(4, 14, 9)):
            stats = {
                'points': points,
                'rebounds': rebounds,
                'assists': assists,
                'steals': steals,
                'blocks': blocks
            }
            self.update_player_stats(stats)

            total = (points * self.nba_Salary_Score_System.get_value_of('point') +
                    rebounds * self.nba_Salary_Score_System.get_value_of('rebound') +
                    assists * self.nba_Salary_Score_System.get_value_of('assist') +
                    steals * self.nba_Salary_Score_System.get_value_of('steal') +
                    blocks * self.nba_Salary_Score_System.get_value_of('block'))

            double_digit_stats = 0
            double_digit_stats += 1 if points >= 10.0 else 0
            double_digit_stats += 1 if rebounds >= 10.0 else 0
            double_digit_stats += 1 if assists >= 10.0 else 0
            double_digit_stats += 1 if steals >= 10.0 else 0
            double_digit_stats += 1 if blocks >= 10.0 else 0

            if double_digit_stats == 2:
                total += self.nba_Salary_Score_System.get_value_of('dbl-dbl')
            elif double_digit_stats > 2:
                total += self.nba_Salary_Score_System.get_value_of('triple-dbl')
            print ("p, r, a, s, b = %.1f %.1f %.1f %.1f %.1f" % (points, rebounds, assists, steals, blocks))
            self.assertAlmostEquals(self.nba_Salary_Score_System.score_player(self.player_stats), total)

