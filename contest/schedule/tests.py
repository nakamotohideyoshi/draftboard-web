from django.test import TestCase
from django.utils import timezone
from model_mommy import mommy

from contest.models import ContestPool
from sports.classes import SiteSportManager
from sports.mlb.models import Game
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
        Note: games `start` times are in utc!
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

    """
    We can't `cpsm.create_contest_pools()` because you need a ton of other stuff in order
    to actually create them and buliding all of that is too dang hard. Instead we'll just
    create some games and check that the BlockManager picks up on them - that's what
    dictates if they end up being included in the contest pool draft groups anyway.
    """

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
