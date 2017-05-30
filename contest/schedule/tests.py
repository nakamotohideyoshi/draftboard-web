from django.test import TestCase
from django.utils import timezone
from model_mommy import mommy

from contest.models import ContestPool
from draftgroup.classes import DraftGroupManager
from sports.classes import SiteSportManager
from sports.mlb.models import (Game, Team)
from test.classes import create_prize_structure
from .classes import (ContestPoolScheduleManager, BlockManager)
from .models import (Block, BlockPrizeStructure)


class SchedulerTest(TestCase):
    # some helplful timestamps
    time_1_hour_ago = timezone.now() - timezone.timedelta(hours=1)
    time_1_hour_ahead = timezone.now() + timezone.timedelta(hours=1)
    time_2_hour_ago = timezone.now() - timezone.timedelta(hours=2)
    time_2_hour_ahead = timezone.now() + timezone.timedelta(hours=2)
    time_3_hour_ago = timezone.now() - timezone.timedelta(hours=3)
    time_3_hour_ahead = timezone.now() + timezone.timedelta(hours=3)
    time_12_hour_ahead = timezone.now() + timezone.timedelta(hours=12)
    time_12_hour_ago = timezone.now() - timezone.timedelta(hours=12)

    def setUp(self):
        self.sport = "mlb"
        self.ssm = SiteSportManager()
        self.dgm = DraftGroupManager()
        self.site_sport = self.ssm.get_site_sport(self.sport)
        self.cpsm = ContestPoolScheduleManager(self.sport)

    def tearDown(self):
        Game.objects.all().delete()
        Block.objects.all().delete()
        BlockPrizeStructure.objects.all().delete()

    def create_active_block(self):
        active_block = mommy.make(
            Block,
            site_sport=self.site_sport,
            cutoff_time=self.time_3_hour_ago,
            dfsday_start=self.time_3_hour_ago,
            dfsday_end=self.time_3_hour_ahead,
        )

        prize_structure = create_prize_structure()
        mommy.make(
            BlockPrizeStructure,
            prize_structure=prize_structure,
            block=active_block,
        )

        return Block.objects.get(id=active_block.id)

    def create_valid_game(self):
        """
        Create a game with in the get_active_block block.
        :return: 
        """
        return mommy.make(
            Game,
            start=self.time_1_hour_ahead
        )

    def create_too_early_game(self):
        return mommy.make(
            Game,
            start=self.time_12_hour_ago
        )

    def create_too_late_game(self):
        return mommy.make(
            Game,
            start=self.time_12_hour_ahead
        )

    """
    We can't `cpsm.create_contest_pools()` because you need a ton of other stuff in order
    to actually create them and buliding all of that is too dang hard. Instead we'll just
    create some games and check that the BlockManager picks up on them - that's what
    dictates if they end up being included in the contest pool draft groups anyway.
    """
    def test_get_active_block(self):
        """
        Create a block for today, then make sure the ContestPoolScheduleManager finds it.
        """
        active_block = self.create_active_block()

        self.assertEqual(active_block, self.cpsm.get_active_block())

    def test_create_contest_pools_no_games(self):
        """
        Be sure that no contest pools are created when no games exist.
        """
        active_block = self.create_active_block()
        self.cpsm.create_contest_pools(active_block)

        created_pools = ContestPool.objects.filter(site_sport=self.site_sport)
        self.assertEqual(created_pools.count(), 0)

    def test_2_included_games(self):
        """
        Create 2 games that should be included in this block
        """
        active_block = self.create_active_block()
        self.create_valid_game()
        self.create_valid_game()
        bm = BlockManager(active_block)
        self.assertEqual(bm.get_included_games().count(), 2)

    def test_1_excluded_game(self):
        """
        Create 2 games that should be included in this block and one that shouldn't
        """
        active_block = self.create_active_block()
        self.create_valid_game()
        self.create_valid_game()
        self.create_too_early_game()
        bm = BlockManager(active_block)
        self.assertEqual(bm.get_included_games().count(), 2)

    def test_2_excluded_game(self):
        """
        Create 1 game that should be included in this block and two that shouldn't
        """
        active_block = self.create_active_block()
        self.create_valid_game()
        self.create_too_late_game()
        self.create_too_early_game()
        bm = BlockManager(active_block)
        self.assertEqual(bm.get_included_games().count(), 1)

    def test_draftgroup_create_with_team_doubleheader(self):
        """
        This is generally just for MLB. If a game was rescheduled, and the team
        now plays twice in one day, we should only be included the first game
        when creating a draft group.
        """

        # old game that should not be caught in the draftgroup.
        mommy.make(
            Game,
            start=self.time_12_hour_ago
        )
        # 1 game that should be caught in the draft group
        game_1 = self.create_valid_game()

        teams = mommy.make(
            Team,
            _quantity=2
        )

        # Create 2 games with the same teams - our draft group createtor should ignore
        # the second game.
        double_header_game_1 = mommy.make(
            Game,
            start=self.time_1_hour_ahead,
            away=teams[0],
            srid_away=teams[0].srid,
            home=teams[1],
            srid_home=teams[1].srid
        )

        double_header_game_2 = mommy.make(
            Game,
            start=self.time_3_hour_ahead,
            away=teams[0],
            srid_away=teams[0].srid,
            home=teams[1],
            srid_home=teams[1].srid
        )

        # This should get game_1 and one of double_header_games
        draft_group_games = self.dgm.find_games_within_time_span(
            site_sport=self.site_sport,
            start=game_1.start,
            end=self.time_12_hour_ahead
        )

        # Make sure we have 2 games, containing the first of the
        # doubleheader and not the second.
        self.assertEqual(len(draft_group_games), 2)
        self.assertIn(double_header_game_1, draft_group_games)
        self.assertNotIn(double_header_game_2, draft_group_games)
