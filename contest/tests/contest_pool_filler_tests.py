import datetime
from logging import getLogger

from django.contrib.auth.models import User
from model_mommy import mommy

from contest.buyin.models import Buyin
from contest.classes import (
    ContestPoolFiller
)
from contest.models import (
    ContestPool,
    Entry,
)
from contest.refund.models import Refund
from prize.classes import (Generator, CashPrizeStructureCreator)
from test.classes import (
    AbstractTest
)

logger = getLogger('contest.contest_pool_filler.tests')


class ContestPoolFillerTest(AbstractTest):
    def setUp(self):
        self.removeAllRefunds()

    def tearDown(self):
        self.removeAllRefunds()

    def removeAllRefunds(self):
        Refund.objects.all().delete()
        self.assertEqual(Refund.objects.all().count(), 0)

    @staticmethod
    def createPrizeStructure(buyin=1, first_place=10, round_payouts=10, payout_spots=1,
                             prize_pool=2):
        """
        Create a prize structure. Other than `prize_pool` these numbers really don't matter since
        we aren't awarding any prizes in these tests.
        :param buyin:
        :param first_place:
        :param round_payouts:
        :param payout_spots:
        :param prize_pool: The number of entries allowed in a contest (kinda, in a roundabout way).
        :return:
        """
        gen = Generator(buyin, first_place, round_payouts, payout_spots, prize_pool, verbose=False)
        gen.update_prize_pool()
        cps = CashPrizeStructureCreator(generator=gen, name='test_cps')
        cps.save()
        return cps.prize_structure

    @staticmethod
    def createUserEntries(contest_pool, user_id, quantity=1):
        entries = mommy.make(
            Entry,
            _quantity=quantity,
            contest_pool=contest_pool,
            user__id=user_id,
            make_m2m=True,
        )
        for entry in entries:
            mommy.make(Buyin, entry=entry)

    def test_2_entries_no_refunds(self):
        """
        2 users, 1 entry each should produce 1 contest, 0 refunds.
        """
        prize_struct = self.createPrizeStructure(prize_pool=2)

        # Create a contest pool that ends tomorrow.
        contest_pool = mommy.make(
            ContestPool,
            end=datetime.date.today() + datetime.timedelta(days=1),
            make_m2m=True,
            prize_structure=prize_struct,
        )

        # create 1 entry each for 2 different users.
        self.createUserEntries(contest_pool, 1, 1)
        self.createUserEntries(contest_pool, 2, 1)

        # Fill the contests.
        cpf = ContestPoolFiller(contest_pool)
        new_contests = cpf.fair_match()

        # ensure 1 contest was created with no refunds issued.
        self.assertEqual(len(new_contests), 1)
        self.assertEqual(Refund.objects.count(), 0)

    def test_2_users_5_entries_refunds(self):
        """
        2 users, one has 4 entries. this should produce 1 contest and 2 refunds
        """
        prize_struct = self.createPrizeStructure(prize_pool=2)

        # Create a contest pool that ends tomorrow.
        contest_pool = mommy.make(
            ContestPool,
            end=datetime.date.today() + datetime.timedelta(days=1),
            make_m2m=True,
            prize_structure=prize_struct,
        )
        # Create a couple of users.
        user1 = mommy.make(User)
        user2 = mommy.make(User)

        self.createUserEntries(contest_pool, user1.id, 1)
        self.createUserEntries(contest_pool, user2.id, 4)

        # Fill contests
        cpf = ContestPoolFiller(contest_pool)
        new_contests = cpf.fair_match()

        # ensure 1 contest was created with 3 refunds issued.
        self.assertEqual(len(new_contests), 1)
        self.assertEqual(Refund.objects.count(), 3)

    def test_2_users_10_entries_refunds(self):
        """
        In this instance 1 contest should be matched and then 3 of user2's entries
        should be refunded.
        """
        prize_struct = self.createPrizeStructure(prize_pool=2)

        # Create a contest pool that ends tomorrow.
        contest_pool = mommy.make(
            ContestPool,
            end=datetime.date.today() + datetime.timedelta(days=1),
            make_m2m=True,
            prize_structure=prize_struct,
        )
        # Create a couple of users.
        user1 = mommy.make(User)
        user2 = mommy.make(User)
        self.createUserEntries(contest_pool, user1.id, 1)
        self.createUserEntries(contest_pool, user2.id, 10)

        # Fill contests
        cpf = ContestPoolFiller(contest_pool)
        new_contests = cpf.fair_match()

        # ensure 1 contest was created with 9refunds issued.
        self.assertEqual(len(new_contests), 1)
        self.assertEqual(Refund.objects.count(), 9)

    def test_4_users_with_refunds(self):
        """
        In this instance 1 3-man contest should be matched, one will be forced, and one
        refund issued.
        """
        prize_struct = self.createPrizeStructure(prize_pool=3)

        # Create a contest pool that ends tomorrow.
        contest_pool = mommy.make(
            ContestPool,
            end=datetime.date.today() + datetime.timedelta(days=1),
            make_m2m=True,
            prize_structure=prize_struct,
        )
        # Create users.
        user1 = mommy.make(User)
        user2 = mommy.make(User)
        user3 = mommy.make(User)
        user4 = mommy.make(User)

        self.createUserEntries(contest_pool, user1.id, 1)
        self.createUserEntries(contest_pool, user2.id, 1)
        self.createUserEntries(contest_pool, user3.id, 3)
        self.createUserEntries(contest_pool, user4.id, 3)

        # Fill contests
        cpf = ContestPoolFiller(contest_pool)
        new_contests = cpf.fair_match()

        # ensure 2 contests were created with 2 or 3 refunds issued.
        # it's 2 or 3 due to the randomness in the fairmatch algorithm.
        self.assertEqual(len(new_contests), 2)
        self.assertIn(Refund.objects.count(), [2, 3])

    def test_not_enough_entries(self):
        """
        If there aren't enough entries to fill a contest's first round, no refunds
        should happen. (first round entries should always match, even if it creates superlay)
        """
        prize_struct = self.createPrizeStructure(prize_pool=3)

        # Create a contest pool that ends tomorrow.
        contest_pool = mommy.make(
            ContestPool,
            end=datetime.date.today() + datetime.timedelta(days=1),
            make_m2m=True,
            prize_structure=prize_struct,
        )

        # Create users.
        user1 = mommy.make(User)
        user2 = mommy.make(User)

        self.createUserEntries(contest_pool, user1.id, 1)
        self.createUserEntries(contest_pool, user2.id, 1)

        # Fill contests
        cpf = ContestPoolFiller(contest_pool)
        new_contests = cpf.fair_match()

        # 1 contest, no refunds
        self.assertEqual(len(new_contests), 1)
        self.assertEqual(Refund.objects.count(), 0)
