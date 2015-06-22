from django.test import TestCase
from test.classes import AbstractTest
from contest.models import Contest, Entry
from prize.models import PrizeStructure, Rank

class PayoutTest(AbstractTest):
    def setUp(self):
        #
        # create a simple Rank and Prize Structure

        pass

    def test_simple_payout(self):
        pass