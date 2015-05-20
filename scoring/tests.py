#
# scoring/tests.py

import itertools
import sports.nba.models
import sports.nhl.models
import sports.mlb.models
from django.test import TestCase
from test.classes import AbstractTest
from scoring.classes import NbaSalaryScoreSystem, NhlSalaryScoreSystem, MlbSalaryScoreSystem
from dataden.util.timestamp import Parse as DataDenDatetime

class NbaScoringTest(AbstractTest):
    """
    Test the scoring system for NBA.  The test method will be:
        - Create a dummy player in the Postgres database with all stats set to 0
        - Increment individual stats and compare the calculated point value against the scoring system projected value
        - Increment groups of stats and compare the calculated point value against the scoring system projected value
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
            self.assertAlmostEquals(self.nba_Salary_Score_System.score_player(self.player_stats), total)


class NhlScoringTest(AbstractTest):
    """
    Test the scoring system for NHL.  The test method will be:
        - Create a dummy player in the Postgres database with all stats set to 0
        - Increment individual stats and compare the calculated point value against the scoring system projected value
        - Increment groups of stats and compare the calculated point value against the scoring system projected value
    """

    def setUp(self):
        self.create_team()
        self.create_game()
        self.create_player()
        self.player_stats = self.create_player_stats()
        self.nhl_Salary_Score_System = NhlSalaryScoreSystem()

    def create_team(self):
        srid            = "4417eede-0f24-11e2-8525-18a905767e44"
        srid_league     = "fd560107-a85b-4388-ab0d-655ad022aff7"
        srid_conference = "7ab1c9c0-4ffa-4f27-bcb6-be54d6ca6127"
        srid_division   = "1fad71d8-5b9e-4159-921b-9b98d0573f51"
        market          = "Tampa Bay"
        name            = "Lightning"
        alias           = "TBL"
        srid_venue      = "05aa49b2-f72d-4d42-ab30-f219d32ed97b"

        try:
            t = sports.nhl.models.Team.objects.get( srid=srid )
        except sports.nhl.models.Team.DoesNotExist:
            t = sports.nhl.models.Team()
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
        srid        = "434f82a5-0f24-11e2-8525-18a905767e44"
        srid_team   = "4417eede-0f24-11e2-8525-18a905767e44"

        first_name  = "John"
        last_name   = "Erskine"

        birth_place = "Miami, FL, USA"
        birthdate   = "1980-10-04"
        college     = "Miami"
        experience  = 11
        height      = 80      # inches
        weight      = 215      # lbs.
        jersey_number       = 1

        position            = "G"
        primary_position    = "G"

        status              = "ACT"   # roster status, ie: basically whether they are on it

        draft_pick      = 49
        draft_round     = 2
        draft_year      = 2003
        srid_draft_team = "4417eede-0f24-11e2-8525-18a905767e44"

        t = sports.nhl.models.Team.objects.get(srid=srid_team)

        try:
            p = sports.nhl.models.Player.objects.get(srid=srid)
        except sports.nhl.models.Player.DoesNotExist:
            p = sports.nhl.models.Player()
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

        srid_home   = "4417eede-0f24-11e2-8525-18a905767e44"
        srid_away   = "4417eede-0f24-11e2-8525-18a905767e44"
        title       = "Game 1"

        h = sports.nhl.models.Team.objects.get(srid=srid_home)
        a = sports.nhl.models.Team.objects.get(srid=srid_away)

        try:
            g = sports.nhl.models.Game.objects.get(srid=srid)
        except sports.nhl.models.Game.DoesNotExist:
            g = sports.nhl.models.Game()
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
        srid_player = "434f82a5-0f24-11e2-8525-18a905767e44"

        p = sports.nhl.models.Player.objects.get(srid=srid_player)
        g = sports.nhl.models.Game.objects.get(srid=srid_game)

        try:
            ps = sports.nhl.models.PlayerStats.objects.get( srid_game=srid_game, srid_player=srid_player )
        except sports.nhl.models.PlayerStats.DoesNotExist:
            ps = sports.nhl.models.PlayerStats()
            ps.srid_game    = srid_game
            ps.srid_player  = srid_player
            ps.player  = p
            ps.game    = g

        #content_type    = models.ForeignKey(ContentType, related_name='nhl_playerstats')

        # skater stats
        ps.goal        = 0
        ps.assist      = 0
        ps.sog         = 0
        ps.blk         = 0
        ps.sh_goal     = 0
        ps.pp_goal     = 0
        ps.so_goal     = 0

        # goalie stats    ... [ "win", "loss", "overtime_loss", "none" ] are the "credit" types for goalies
        ps.w           = bool(0)
        ps.l           = bool(0)
        ps.otl         = bool(0)
        ps.saves       = 0
        ps.ga          = 0
        ps.shutout     = bool(0)

        ps.save() # commit changes

        return ps

    def update_player_stats(self, stat_list):
        for stat in stat_list.keys():
            setattr(self.player_stats, stat, stat_list[stat])
        self.player_stats.save()

    def test_stats_all_0(self):
        self.assertAlmostEquals(self.nhl_Salary_Score_System.score_player(self.player_stats), 0)

    def test_all_unused_stats(self):
        # Set all unused stats values to 10 and make sure that the total points calculated is still 0
        unused_stats = {
            'pp_goal': 10,
            'l': bool(1),
            'otl': bool(1)
        }
        self.create_player_stats()
        self.update_player_stats(unused_stats)
        self.assertAlmostEquals(self.nhl_Salary_Score_System.score_player(self.player_stats), 0)

    def test_goal_and_hat_trick(self):
        # Test various values of goals to make sure the calculations are correct, including hat tricks
        self.create_player_stats()
        for goals in range(0, 10):
            self.update_player_stats({'goal': goals})
            total = goals * self.nhl_Salary_Score_System.get_value_of('goal')
            total += self.nhl_Salary_Score_System.get_value_of('hat') if goals >= 3 else 0
            self.assertAlmostEquals(self.nhl_Salary_Score_System.score_player(self.player_stats), total)

    def test_assist(self):
        # Test various values of assists to make sure the calculations are correct
        self.create_player_stats()
        for assists in range(0, 10):
            self.update_player_stats({'assist': assists})
            multiplier = self.nhl_Salary_Score_System.get_value_of('assist')
            self.assertAlmostEquals(self.nhl_Salary_Score_System.score_player(self.player_stats), assists * multiplier)

    def test_shots_on_goal(self):
        # Test various values of sog to make sure the calculations are correct
        self.create_player_stats()
        for sogs in range(0, 10):
            self.update_player_stats({'sog': sogs})
            multiplier = self.nhl_Salary_Score_System.get_value_of('sog')
            self.assertAlmostEquals(self.nhl_Salary_Score_System.score_player(self.player_stats), sogs * multiplier)

    def test_blocks(self):
        # Test various values of blocks to make sure the calculations are correct
        self.create_player_stats()
        for blocks in range(0, 10):
            self.update_player_stats({'blk': blocks})
            multiplier = self.nhl_Salary_Score_System.get_value_of('blk')
            self.assertAlmostEquals(self.nhl_Salary_Score_System.score_player(self.player_stats), blocks * multiplier)

    def test_short_handed_bonus(self):
        # Test various values of goals and short handed bonuses to make sure the calculations are correct
        self.create_player_stats()
        for goals in range(0, 10):
            for sh_goals in range(0, goals+1):
                self.update_player_stats({'goal': goals, 'sh_goal': sh_goals})
                total = goals * self.nhl_Salary_Score_System.get_value_of('goal')
                total += self.nhl_Salary_Score_System.get_value_of('hat') if goals >= 3 else 0
                total += sh_goals * self.nhl_Salary_Score_System.get_value_of('sh-bonus')
                self.assertAlmostEquals(self.nhl_Salary_Score_System.score_player(self.player_stats), total)

    def test_shootout_goals(self):
        # Test various values of goals and shootout_goals to make sure the calculations are correct
        self.create_player_stats()
        for goals in range(1, 10):
            for so_goals in range(0, 2):
                self.update_player_stats({'goal': goals, 'so_goal': so_goals})
                total = goals * self.nhl_Salary_Score_System.get_value_of('goal')
                total += self.nhl_Salary_Score_System.get_value_of('hat') if goals >= 3 else 0
                total += so_goals * self.nhl_Salary_Score_System.get_value_of('so-goal')
                self.assertAlmostEquals(self.nhl_Salary_Score_System.score_player(self.player_stats), total)

    def test_win(self):
        # Test a win to make sure the calculations are correct
        self.create_player_stats()
        self.update_player_stats({'w': bool(1)})
        multiplier = self.nhl_Salary_Score_System.get_value_of('win')
        self.assertAlmostEquals(self.nhl_Salary_Score_System.score_player(self.player_stats), multiplier)

    def test_saves(self):
        # Test saves to make sure the calculations are correct
        self.create_player_stats()
        for saves in range(0, 10):
            self.update_player_stats({'saves': saves})
            multiplier = self.nhl_Salary_Score_System.get_value_of('save')
            self.assertAlmostEquals(self.nhl_Salary_Score_System.score_player(self.player_stats), saves * multiplier)

    def test_goals_against(self):
        # Test goals against to make sure the calculations are correct
        self.create_player_stats()
        for gas in range(0, 10):
            self.update_player_stats({'ga': gas})
            multiplier = self.nhl_Salary_Score_System.get_value_of('ga')
            self.assertAlmostEquals(self.nhl_Salary_Score_System.score_player(self.player_stats), gas * multiplier)

    def test_shutout(self):
        # Test shutout to make sure the calculations are correct
        self.create_player_stats()
        self.update_player_stats({'shutout': bool(1)})
        total = self.nhl_Salary_Score_System.get_value_of('shutout')
        self.assertAlmostEquals(self.nhl_Salary_Score_System.score_player(self.player_stats), total)
        self.update_player_stats({'w': bool(1)})
        total += self.nhl_Salary_Score_System.get_value_of('win')
        self.assertAlmostEquals(self.nhl_Salary_Score_System.score_player(self.player_stats), total)

    def test_all_values(self):
        """
        Test various values of stats to make sure the calculations are correct for double doubles and triple doubles.
        If exactly two stats are >= 10.0, a double double bonus should be given.
        If three or more stats are >= 10.0, a triple double bonus should be given.
        This test also tests multiple stats values set simultaneously.
        """
        self.create_player_stats()
        for goals, assists, sogs, blks, w, saves, ga in itertools.product(range(2, 5, 2), range(0, 4, 3), range(5, 10, 4),
                                                                          range(0, 2), range(0, 2), range(28, 30),
                                                                          range(0, 2)):
            for sh_goals in range(0, min(goals + 1, 2)):
                for so_goals in range(0, min(goals + 1, 1)):
                    stats = {
                        'goal': goals,
                        'assist': assists,
                        'sog': sogs,
                        'blk': blks,
                        'w': bool(w),
                        'saves': saves,
                        'ga': ga,
                        'sh_goal': sh_goals,
                        'so_goal': so_goals,
                        'shutout': not bool(ga)
                    }
                    self.update_player_stats(stats)
        
                    total = (goals * self.nhl_Salary_Score_System.get_value_of('goal') +
                            assists * self.nhl_Salary_Score_System.get_value_of('assist') +
                            sogs * self.nhl_Salary_Score_System.get_value_of('sog') +
                            blks * self.nhl_Salary_Score_System.get_value_of('blk') +
                            w * self.nhl_Salary_Score_System.get_value_of('win') +
                            saves * self.nhl_Salary_Score_System.get_value_of('save') +
                            ga * self.nhl_Salary_Score_System.get_value_of('ga') +
                            sh_goals * self.nhl_Salary_Score_System.get_value_of('sh-bonus') +
                            so_goals * self.nhl_Salary_Score_System.get_value_of('so-goal') +
                            int(not bool(ga)) * self.nhl_Salary_Score_System.get_value_of('shutout'))
                    total += self.nhl_Salary_Score_System.get_value_of('hat') if goals >= 3 else 0

                    self.assertAlmostEquals(self.nhl_Salary_Score_System.score_player(self.player_stats), total)


class MlbScoringTest(AbstractTest):
    """
    Test the scoring system for MLB.  The test method will be:
        - Create a dummy player in the Postgres database with all stats set to 0
        - Increment individual stats and compare the calculated point value against the scoring system projected value
        - Increment groups of stats and compare the calculated point value against the scoring system projected value
    """

    def setUp(self):
        self.create_team()
        self.create_game()
        self.create_pitcher()
        self.create_hitter()
        self.pitcher_stats = self.create_pitcher_stats()
        self.hitter_stats = self.create_hitter_stats()
        self.mlb_Salary_Score_System = MlbSalaryScoreSystem()

    def create_team(self):
        srid            = "1d678440-b4b1-4954-9b39-70afb3ebbcfa"
        srid_league     = "2fa448bc-fc17-4d3d-be03-e60e080fdc26"
        srid_conference = "2ea6efe7-2e21-4f29-80a2-0a24ad1f5f85"
        srid_division   = "1d74e8e9-7faf-4cdb-b613-3944fa5aa739"
        market          = "Toronto"
        name            = "Blue Jays"
        alias           = "TOR"
        srid_venue      = "84d72338-2173-4a90-9d25-99adc6c86f4b"

        try:
            t = sports.mlb.models.Team.objects.get( srid=srid )
        except sports.mlb.models.Team.DoesNotExist:
            t = sports.mlb.models.Team()
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

    def create_pitcher(self):
        srid        = "f11efc76-62f5-4396-b145-e03839fd4d1c"
        srid_team   = "1d678440-b4b1-4954-9b39-70afb3ebbcfa"

        first_name  = "Andrew"
        last_name   = "Hutchison"

        birth_place = "Miami, FL, USA"
        birthdate   = "1980-10-04"
        college     = "Miami"
        experience  = 4
        height      = 80      # inches
        weight      = 215      # lbs.
        jersey_number       = 1

        position            = "P"
        primary_position    = "SP"

        status              = "ACT"   # roster status, ie: basically whether they are on it

        draft_pick      = 49
        draft_round     = 2
        draft_year      = 2011
        srid_draft_team = "1d678440-b4b1-4954-9b39-70afb3ebbcfa"

        t = sports.mlb.models.Team.objects.get(srid=srid_team)

        try:
            p = sports.mlb.models.Player.objects.get(srid=srid)
        except sports.mlb.models.Player.DoesNotExist:
            p = sports.mlb.models.Player()
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

    def create_hitter(self):
        srid        = "0a3067f1-d632-4d4d-b42e-46cb0f7ca608"
        srid_team   = "1d678440-b4b1-4954-9b39-70afb3ebbcfa"

        first_name  = "Christopher"
        last_name   = "Colabello"

        birth_place = "Miami, FL, USA"
        birthdate   = "1980-10-04"
        college     = "Miami"
        experience  = 4
        height      = 80      # inches
        weight      = 215      # lbs.
        jersey_number       = 1

        position            = "IF"
        primary_position    = "1B"

        status              = "ACT"   # roster status, ie: basically whether they are on it

        draft_pick      = 49
        draft_round     = 2
        draft_year      = 2011
        srid_draft_team = "1d678440-b4b1-4954-9b39-70afb3ebbcfa"

        t = sports.mlb.models.Team.objects.get(srid=srid_team)

        try:
            p = sports.mlb.models.Player.objects.get(srid=srid)
        except sports.mlb.models.Player.DoesNotExist:
            p = sports.mlb.models.Player()
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
        srid        = "8c1c0046-36a0-4672-8465-53ebf690d8bb"
        start_str   = "2015-04-18T16:30:00+00:00"
        start       = DataDenDatetime.from_string( start_str )
        status      = "closed"

        srid_home   = "1d678440-b4b1-4954-9b39-70afb3ebbcfa"
        srid_away   = "1d678440-b4b1-4954-9b39-70afb3ebbcfa"
        title       = "Game 1"

        h = sports.mlb.models.Team.objects.get(srid=srid_home)
        a = sports.mlb.models.Team.objects.get(srid=srid_away)

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
        g.save()

    def create_pitcher_stats(self):
        srid_game   = "8c1c0046-36a0-4672-8465-53ebf690d8bb"
        srid_player = "f11efc76-62f5-4396-b145-e03839fd4d1c"

        p = sports.mlb.models.Player.objects.get(srid=srid_player)
        g = sports.mlb.models.Game.objects.get(srid=srid_game)

        #content_type    = models.ForeignKey(ContentType, related_name='mlb_playerstats')

        #pitcher stats
        try:
            ps = sports.mlb.models.PlayerStatsPitcher.objects.get( srid_game=srid_game, srid_player=srid_player )
        except sports.mlb.models.PlayerStatsPitcher.DoesNotExist:
            ps = sports.mlb.models.PlayerStatsPitcher()
        ps.srid_game    = srid_game
        ps.srid_player  = srid_player
        ps.player  = p
        ps.game    = g

        ps.ip_1    = 0.0 # outs, basically. for 1 inning pitched == 3 (4 possible?)
        ps.ip_2    = 0.0 # 1 == one inning pitched
        ps.win     = bool( 0 )
        ps.loss    = bool( 0 )
        ps.qstart  = bool( 0 )
        ps.ktotal  = 0
        ps.er      = 0  # earned runs allowed
        ps.r_total = 0   # total runs allowed (earned and unearned)
        ps.h       = 0     # hits against
        ps.bb      = 0    # walks against
        ps.hbp     = 0   # hit batsmen
        ps.cg      = bool( 0 ) # complete game
        ps.cgso    = bool( 0 ) and ps.cg # complete game shut out
        ps.nono    = bool( ps.h ) and ps.cg # no hitter if hits == 0, and complete game

        ps.save() # commit changes

        return ps

    def create_hitter_stats(self):
        srid_game   = "8c1c0046-36a0-4672-8465-53ebf690d8bb"
        srid_player = "0a3067f1-d632-4d4d-b42e-46cb0f7ca608"

        p = sports.mlb.models.Player.objects.get(srid=srid_player)
        g = sports.mlb.models.Game.objects.get(srid=srid_game)

        #content_type    = models.ForeignKey(ContentType, related_name='mlb_playerstats')

        # hitter stats
        try:
            ps = sports.mlb.models.PlayerStatsHitter.objects.get( srid_game=srid_game, srid_player=srid_player )
        except sports.mlb.models.PlayerStatsHitter.DoesNotExist:
            ps = sports.mlb.models.PlayerStatsHitter()
        ps.srid_game    = srid_game
        ps.srid_player  = srid_player
        ps.player  = p
        ps.game    = g

        ps.bb  = 0
        ps.s   = 0
        ps.d   = 0
        ps.t   = 0
        ps.hr  = 0
        ps.rbi = 0
        ps.r   = 0
        ps.hbp = 0
        ps.sb  = 0
        ps.cs  = 0

        ps.ktotal  = 0

        ps.ab  = 0
        ps.ap  = 0
        ps.lob = 0
        ps.xbh = 0

        ps.save() # commit changes

        return ps

    def update_pitcher_stats(self, stat_list):
        for stat in stat_list.keys():
            setattr(self.pitcher_stats, stat, stat_list[stat])
        self.pitcher_stats.save()

    def update_hitter_stats(self, stat_list):
        for stat in stat_list.keys():
            setattr(self.hitter_stats, stat, stat_list[stat])
        self.hitter_stats.save()

    # Pitcher tests
    def test_pitcher_stats_all_0(self):
        self.assertAlmostEquals(self.mlb_Salary_Score_System.score_player(self.pitcher_stats), 0)

    def test_all_unused_pitcher_stats(self):
        # Set all unused stats values to 10 and make sure that the total points calculated is still 0
        unused_stats = {
            'ip_2': 10.0,
            'loss': bool( 1 ),
            'qstart': bool( 1 ),
            'r_total': 10,
            'hbp': 10
        }
        self.create_pitcher_stats()
        self.update_pitcher_stats(unused_stats)
        self.assertAlmostEquals(self.mlb_Salary_Score_System.score_player(self.pitcher_stats), 0)

    def test_pitcher_innings_pitched(self):
        # Test various values of ip_1 to make sure the calculations are correct
        # ip_1 is the number of outs recorded by the pitcher.  This is divided by 3 to get the number of innings pitched
        self.create_pitcher_stats()
        for ip in range(34):
            self.update_pitcher_stats({'ip_1': ip})
            multiplier = self.mlb_Salary_Score_System.get_value_of('ip')
            self.assertAlmostEquals(self.mlb_Salary_Score_System.score_player(self.pitcher_stats), float(ip / 3.0) * multiplier)

    def test_pitcher_strikeouts(self):
        # Test various values of k to make sure the calculations are correct
        self.create_pitcher_stats()
        for strikeouts in range(11):
            self.update_pitcher_stats({'ktotal': strikeouts})
            multiplier = self.mlb_Salary_Score_System.get_value_of('k')
            self.assertAlmostEquals(self.mlb_Salary_Score_System.score_player(self.pitcher_stats), strikeouts * multiplier)

    def test_pitcher_win(self):
        # Test the bonus for a pitcher getting a win
        self.create_pitcher_stats()
        self.update_pitcher_stats({'win': bool(1)})
        win_bonus = self.mlb_Salary_Score_System.get_value_of('win')
        self.assertAlmostEquals(self.mlb_Salary_Score_System.score_player(self.pitcher_stats), win_bonus)

    def test_pitcher_earned_runs(self):
        # Test various values of er to make sure the calculations are correct
        self.create_pitcher_stats()
        for ers in range(11):
            self.update_pitcher_stats({'er': ers})
            multiplier = self.mlb_Salary_Score_System.get_value_of('er')
            self.assertAlmostEquals(self.mlb_Salary_Score_System.score_player(self.pitcher_stats), ers * multiplier)

    def test_pitcher_hits_allowed(self):
        # Test various values of hit to make sure the calculations are correct
        self.create_pitcher_stats()
        for hits in range(11):
            self.update_pitcher_stats({'h': hits})
            multiplier = self.mlb_Salary_Score_System.get_value_of('hit')
            self.assertAlmostEquals(self.mlb_Salary_Score_System.score_player(self.pitcher_stats), hits * multiplier)

    def test_pitcher_walks(self):
        # Test various values of walk to make sure the calculations are correct
        self.create_pitcher_stats()
        for walks in range(11):
            self.update_pitcher_stats({'bb': walks})
            multiplier = self.mlb_Salary_Score_System.get_value_of('walk')
            self.assertAlmostEquals(self.mlb_Salary_Score_System.score_player(self.pitcher_stats), walks * multiplier)

    def test_pitcher_complete_game(self):
        # Test the bonus for a pitcher getting a complete game
        self.create_pitcher_stats()
        self.update_pitcher_stats({'cg': bool(1)})
        cg_bonus = self.mlb_Salary_Score_System.get_value_of('cg')
        self.assertAlmostEquals(self.mlb_Salary_Score_System.score_player(self.pitcher_stats), cg_bonus)

    def test_pitcher_complete_game_shutout(self):
        # Test the bonus for a pitcher getting a complete game shutout
        self.create_pitcher_stats()
        self.update_pitcher_stats({'cgso': bool(1)})
        cgso_bonus = self.mlb_Salary_Score_System.get_value_of('cgso')
        self.assertAlmostEquals(self.mlb_Salary_Score_System.score_player(self.pitcher_stats), cgso_bonus)

    def test_pitcher_no_hitter(self):
        # Test the bonus for a pitcher getting a no hitter.  The pitcher must have thrown a complete game
        self.create_pitcher_stats()
        self.update_pitcher_stats({'nono': bool(1), 'cg': bool(1)})
        bonus = self.mlb_Salary_Score_System.get_value_of('no-hitter') + self.mlb_Salary_Score_System.get_value_of('cg')
        self.assertAlmostEquals(self.mlb_Salary_Score_System.score_player(self.pitcher_stats), bonus)

    def test_multiple_pitcher_stats(self):
        # Test combinations of all stats
        self.create_pitcher_stats()
        self.update_pitcher_stats({'nono': bool(1), 'cg': bool(1), 'cgso': bool(1), 'win': bool(1)})
        for ip, k, er, hit, walk in itertools.product(range(0, 41, 10), range(0, 10, 9),
                                                      range(0, 4, 3), range(0, 7, 6),
                                                      range(0, 3, 2)):
            stats = {
                'ip_1': ip,
                'ktotal': k,
                'er': er,
                'h': hit,
                'bb': walk
            }
            self.update_pitcher_stats(stats)

            total = (float(ip / 3.0) * self.mlb_Salary_Score_System.get_value_of('ip') +
                    k * self.mlb_Salary_Score_System.get_value_of('k') +
                    er * self.mlb_Salary_Score_System.get_value_of('er') +
                    hit * self.mlb_Salary_Score_System.get_value_of('hit') +
                    walk * self.mlb_Salary_Score_System.get_value_of('walk') +
                    self.mlb_Salary_Score_System.get_value_of('no-hitter') +
                    self.mlb_Salary_Score_System.get_value_of('cg') +
                    self.mlb_Salary_Score_System.get_value_of('cgso') +
                    self.mlb_Salary_Score_System.get_value_of('win'))

            self.assertAlmostEquals(self.mlb_Salary_Score_System.score_player(self.pitcher_stats), total)

    # Hitter tests
    def test_hitter_stats_all_0(self):
        self.assertAlmostEquals(self.mlb_Salary_Score_System.score_player(self.hitter_stats), 0)

    def test_all_unused_hitter_stats(self):
        # Set all unused stats values to 10 and make sure that the total points calculated is still 0
        unused_stats = {
            'ktotal': 10,
            'ab': 10,
            'ap': 10,
            'lob': 10,
            'xbh': 10
        }
        self.create_hitter_stats()
        self.update_hitter_stats(unused_stats)
        self.assertAlmostEquals(self.mlb_Salary_Score_System.score_player(self.hitter_stats), 0)

    def test_hitter_singles(self):
        # Test various values of single to make sure the calculations are correct
        self.create_hitter_stats()
        for singles in range(5):
            self.update_hitter_stats({'s': singles})
            multiplier = self.mlb_Salary_Score_System.get_value_of('single')
            self.assertAlmostEquals(self.mlb_Salary_Score_System.score_player(self.hitter_stats), singles * multiplier)

    def test_hitter_doubles(self):
        # Test various values of double to make sure the calculations are correct
        self.create_hitter_stats()
        for doubles in range(5):
            self.update_hitter_stats({'d': doubles})
            multiplier = self.mlb_Salary_Score_System.get_value_of('double')
            self.assertAlmostEquals(self.mlb_Salary_Score_System.score_player(self.hitter_stats), doubles * multiplier)

    def test_hitter_triples(self):
        # Test various values of triple to make sure the calculations are correct
        self.create_hitter_stats()
        for triples in range(5):
            self.update_hitter_stats({'t': triples})
            multiplier = self.mlb_Salary_Score_System.get_value_of('triple')
            self.assertAlmostEquals(self.mlb_Salary_Score_System.score_player(self.hitter_stats), triples * multiplier)

    def test_hitter_home_runs(self):
        # Test various values of hr to make sure the calculations are correct
        self.create_hitter_stats()
        for hrs in range(5):
            self.update_hitter_stats({'hr': hrs})
            multiplier = self.mlb_Salary_Score_System.get_value_of('hr')
            self.assertAlmostEquals(self.mlb_Salary_Score_System.score_player(self.hitter_stats), hrs * multiplier)

    def test_hitter_rbis(self):
        # Test various values of rbi to make sure the calculations are correct
        self.create_hitter_stats()
        for rbis in range(5):
            self.update_hitter_stats({'rbi': rbis})
            multiplier = self.mlb_Salary_Score_System.get_value_of('rbi')
            self.assertAlmostEquals(self.mlb_Salary_Score_System.score_player(self.hitter_stats), rbis * multiplier)

    def test_hitter_runs(self):
        # Test various values of run to make sure the calculations are correct
        self.create_hitter_stats()
        for runs in range(5):
            self.update_hitter_stats({'r': runs})
            multiplier = self.mlb_Salary_Score_System.get_value_of('run')
            self.assertAlmostEquals(self.mlb_Salary_Score_System.score_player(self.hitter_stats), runs * multiplier)

    def test_hitter_walks(self):
        # Test various values of bb to make sure the calculations are correct
        self.create_hitter_stats()
        for bbs in range(5):
            self.update_hitter_stats({'bb': bbs})
            multiplier = self.mlb_Salary_Score_System.get_value_of('bb')
            self.assertAlmostEquals(self.mlb_Salary_Score_System.score_player(self.hitter_stats), bbs * multiplier)

    def test_hitter_hit_by_pitch(self):
        # Test various values of hbp to make sure the calculations are correct
        self.create_hitter_stats()
        for hbps in range(5):
            self.update_hitter_stats({'hbp': hbps})
            multiplier = self.mlb_Salary_Score_System.get_value_of('hbp')
            self.assertAlmostEquals(self.mlb_Salary_Score_System.score_player(self.hitter_stats), hbps * multiplier)

    def test_hitter_stolen_bases(self):
        # Test various values of sb to make sure the calculations are correct
        self.create_hitter_stats()
        for sbs in range(5):
            self.update_hitter_stats({'sb': sbs})
            multiplier = self.mlb_Salary_Score_System.get_value_of('sb')
            self.assertAlmostEquals(self.mlb_Salary_Score_System.score_player(self.hitter_stats), sbs * multiplier)

    def test_hitter_caught_stealing(self):
        # Test various values of cs to make sure the calculations are correct
        self.create_hitter_stats()
        for css in range(5):
            self.update_hitter_stats({'cs': css})
            multiplier = self.mlb_Salary_Score_System.get_value_of('cs')
            self.assertAlmostEquals(self.mlb_Salary_Score_System.score_player(self.hitter_stats), css * multiplier)

    def test_multiple_hitter_stats(self):
        # Test combinations of all stats
        self.create_hitter_stats()
        for single, double, triple, hr, rbi, run, bb, hbp, sb, cs in itertools.product(range(3, 5), range(2, 4),
                                                                                       range(2), range(0, 3, 2),
                                                                                       range(3, 7, 3), range(0, 4, 3),
                                                                                       range(2), range(2),
                                                                                       range(2), range(2)):
            stats = {
                's': single,
                'd': double,
                't': triple,
                'hr': hr,
                'rbi': rbi,
                'r': run,
                'bb': bb,
                'hbp': hbp,
                'sb': sb,
                'cs': cs
            }
            self.update_hitter_stats(stats)

            total = (single * self.mlb_Salary_Score_System.get_value_of('single') +
                    double * self.mlb_Salary_Score_System.get_value_of('double') +
                    triple * self.mlb_Salary_Score_System.get_value_of('triple') +
                    hr * self.mlb_Salary_Score_System.get_value_of('hr') +
                    rbi * self.mlb_Salary_Score_System.get_value_of('rbi') +
                    run * self.mlb_Salary_Score_System.get_value_of('run') +
                    bb * self.mlb_Salary_Score_System.get_value_of('bb') +
                    hbp * self.mlb_Salary_Score_System.get_value_of('hbp') +
                    sb * self.mlb_Salary_Score_System.get_value_of('sb') +
                    cs * self.mlb_Salary_Score_System.get_value_of('cs'))

            self.assertAlmostEquals(self.mlb_Salary_Score_System.score_player(self.hitter_stats), total)

