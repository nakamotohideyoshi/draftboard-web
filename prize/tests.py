from django.test import TestCase
from .classes import Generator
from test.classes import AbstractTest

import mysite.exceptions
import ticket.exceptions

from prize.models import PrizeStructure, Rank
from prize.classes import CashPrizeStructureCreator, TicketPrizeStructureCreator
from ticket.models import TicketAmount
from ticket.classes import TicketManager

# quick way to create/use a prize.Generator
def gen(buyin=100, first=1500, round=100, payouts=23, prize_pool=10000, exact=True, verbose=False):

    return Generator(buyin, first, round, payouts, prize_pool, exact, verbose)

class GeneratorTest(AbstractTest):

    def setUp(self):
        pass

    def test_generator_invalid_round_payouts_param_less_than_buyin(self):
        self.assertRaises( mysite.exceptions.InvalidArgumentException,
                           lambda: Generator(100, 1500, 50, 23, 10000) )

    def test_generator_invalid_round_payouts_is_not_multiple_of_buyin(self):
        self.assertRaises( mysite.exceptions.InvalidArgumentException,
                           lambda: Generator(100, 1500, 101, 23, 10000) )

    def test_create_with_generator(self):
        gen = Generator(10, 1000, 10, 150, 10000, verbose=False)
        gen.update_prize_pool()

        name = 'custom_name'
        cps = CashPrizeStructureCreator(generator=gen, name=name)
        cps.save()

        try:
            ps = PrizeStructure.objects.get(name__istartswith=name)
        except PrizeStructure.DoesNotExist:
            ps = None

        self.assertIsNotNone( ps )

    def test_create_cash_prize_structure_with_adds(self):
        name        = 'custom_name'
        total_ranks = 2
        first       = 75.00
        second      = 25.00
        cps         = CashPrizeStructureCreator(name=name)
        cps.add( 1, first )
        cps.add( 2, second )
        cps.set_buyin( 5.00 )
        cps.save()

        try:
            ps = PrizeStructure.objects.get(name__istartswith=name)
        except PrizeStructure.DoesNotExist:
            ps = None

        self.assertIsNotNone( ps )

        ranks = Rank.objects.filter( prize_structure=ps )
        self.assertEquals( total_ranks, len(ranks) )

    def test_create_ticket_prize_structure_raises_invalid_ticket_amount_exception(self):
        self.assertRaises( ticket.exceptions.InvalidTicketAmountException,
                           lambda: TicketPrizeStructureCreator( 1.77, 10, name='no tickets exist actually' ) )

    def test_create_ticket_prize_structure(self):
        # make sure the standard ticket amount "templates" exist!
        TicketManager.create_default_ticket_amounts()

        name = 'custom_name'
        ticket_value = 5.00
        total_prizes = 10
        creator = TicketPrizeStructureCreator( ticket_value, total_prizes, name=name )
        creator.set_buyin( 1 )
        creator.save()
        # print( str(creator) )

        try:
            ps = PrizeStructure.objects.get(name__istartswith=name)
        except PrizeStructure.DoesNotExist:
            ps = None

        self.assertIsNotNone( ps )

        ranks = Rank.objects.filter( prize_structure=ps )
        self.assertEquals( total_prizes, len(ranks) )

        for r in ranks:
            self.assertEquals( ticket_value, r.value )
