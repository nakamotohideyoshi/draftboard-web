#
# prize/helpers.py

from cash.models import CashAmount
import ticket.models
from .models import GeneratorSettings, PrizeStructure, Rank

#
############################################################
# below is cocde to write a script to install the
# basic  HEADSUP, CASH PrizeStructures... TODO
############################################################
# from django.db import models, migrations
# from django.contrib.contenttypes.models import ContentType
# import ticket.models   # we just need this for ticket.models.DEFAULT_TICKET_VALUES
# from django.apps import apps
# from django.contrib.contenttypes.management import update_contenttypes

ten_entry_template          = [ 10,  [ (1,4),(1,3),(1,2) ]]
twenty_entry_template       = [ 20,  [ (1,7),(1,4.5),(1,3),(1,2),(1,1.5) ]]
onehundred_entry_template   = [ 100, [ (1,12),(1,10),(1,8),(1,6),(2,5),(2,4),(2,3),(5,2.5),(5,2),(5,1.5) ]]
twohundred_entry_template   = [ 200, [ (1,16),(1,12),(1,10),(2,8),(3,6),(4,5),(4,4),(4,3),(10,2.5),(10,2),(10,1.5) ]]

templates = [
    ten_entry_template,
    twenty_entry_template,
    onehundred_entry_template,
    twohundred_entry_template,
]

def create(buyin, entries, payouts):
    total_multiple = 0
    total_payout_spots = 0
    for number_paid, buyin_multiple in payouts:
        total_multiple += (number_paid * buyin_multiple)
        total_payout_spots += number_paid
    if total_multiple*buyin != (buyin * entries * 0.9):
        params = '%s buyin, %s entries, %s payouts' % (str(buyin), str(entries), str(payouts))
        raise Exception('the rake is not 10 percent -- invalid params: %s' % params)
    #
    # create generator settings based on this information
    first_place = payouts[0][1] * buyin
    try:
        # check if we already made the generator for this amount
        print('buyin', str(buyin), 'payout_spots', str(total_payout_spots), 'first_place actual value', str(first_place))
        generator_settings = GeneratorSettings.objects.get( buyin=buyin,
                                                            payout_spots=total_payout_spots,
                                                            first_place=first_place,
                                                            round_payouts=1,
                                                            prize_pool=total_multiple*buyin)
    except GeneratorSettings.DoesNotExist:
        #
        generator_settings = GeneratorSettings()
        generator_settings.buyin            = buyin
        generator_settings.first_place      = payouts[0][1] * buyin      # second part of the first tuple
        generator_settings.round_payouts    = 1
        generator_settings.payout_spots     = total_payout_spots
        generator_settings.prize_pool       = total_multiple * buyin
        generator_settings.save()

    try:
        # check if we already made the prize structure for this amount
        prize_structure = PrizeStructure.objects.get( generator=generator_settings )
    except PrizeStructure.DoesNotExist:
        #
        prize_structure = PrizeStructure()
        prize_structure.generator   = generator_settings
        prize_structure.name = ''
        prize_structure.save()
    prize_structure.name        = '$%.0f %s-Entry (%s paid)' % (buyin, entries, str(int(total_payout_spots)))
    prize_structure.save()

    #
    # create each payout spot with the CashAmount
    rank_idx = 1
    for number_at_spot, multiples_of_buyin in payouts:
        #
        # pay the same value to the number of spots specified by 'number_at_spot'
        for x in range(number_at_spot):

            # the CashAmounts should exist, as they are a dependency of this migration
            cash_amount, created = CashAmount.objects.get_or_create(amount=multiples_of_buyin * buyin)

            try:
                #
                # there is only going to be ONE rank (payout) per headsup prize structure
                rank = Rank.objects.get( prize_structure=prize_structure, rank=rank_idx )
            except Rank.DoesNotExist:
                #
                rank                    = Rank()
                rank.prize_structure    = prize_structure
                rank.rank               = rank_idx
                rank.amount             = cash_amount
                rank.save()

            rank_idx += 1

def create_templates():
    amounts = [ x[0] for x in ticket.models.DEFAULT_TICKET_VALUES ]
    for amount in amounts:
        for template in templates:
            print('amount', str(amount), 'entries', str(template[0]), 'structure', str(template[1]))
            create(amount, template[0], template[1])

def create_initial_data():
    """
    installs the very standard prize structures for headsup games

    to do that we need to create the ranks, generators, and prizestrucutre entries

    [
	{
		"model": "prize.generatorsettings",
		"fields": {
			"round_payouts": 0,
			"payout_spots": 1,
			"buyin": 1.0,
			"first_place": 1.8,
			"prize_pool": 1.8
		},
		"pk": 1
	},

	{
		"model": "prize.prizestructure",
		"fields": {
			"generator": 1,
			"created": "2015-12-04T15:12:46.923Z",
			"name": "new prize structure"
		},
		"pk": 1
	},

	{
		"model": "prize.rank",
		"fields": {
			"amount_type": 20,
			"amount_id": 1,
			"rank": 1,
			"prize_structure": 1
		},
		"pk": 1
	}
]
    """

    #
    # amounts we want to create Headsup prize structures for
    #amounts = [ 1.00, 2.00, 5.00, 10.00, 20.00, 50.00, 100.00, 200.00, 500.00 ]
    amounts = [ x[0] for x in ticket.models.DEFAULT_TICKET_VALUES ]

    #
    # create HEADS-UP  (1v1) prize structures for the list of amounts
    for amount in amounts:
        first_place = (amount*2) - (amount*2 * 0.1)  # take out rake: 10%

        try:
            # check if we already made the generator for this amount
            generator_settings = GeneratorSettings.objects.get( buyin=amount )

        except GeneratorSettings.MultipleObjectsReturned:
            print('create_initial_data() - a prize structure for buyin [%s] exists... skipping!'%str(amount))
            continue

        except GeneratorSettings.DoesNotExist:
            #
            generator_settings = GeneratorSettings()
            generator_settings.buyin            = amount
            generator_settings.first_place      = first_place
            generator_settings.round_payouts    = 1
            generator_settings.payout_spots     = 1
            generator_settings.prize_pool       = first_place
            generator_settings.save()

        try:
            # check if we already made the prize structure for this amount
            prize_structure = PrizeStructure.objects.get( generator__buyin=amount )
        except PrizeStructure.DoesNotExist:
            #
            prize_structure = PrizeStructure()
            prize_structure.generator   = generator_settings
            prize_structure.name        = '$%.0f Head-to-Head' % amount
            prize_structure.save()

        # the CashAmounts should exist, as they are a dependency of this migration
        cash_amount, created = CashAmount.objects.get_or_create(amount=first_place)

        try:
            #
            # there is only going to be ONE rank (payout) per headsup prize structure
            rank = Rank.objects.get( prize_structure__pk=prize_structure.pk )
        except Rank.DoesNotExist:
            #
            rank                    = Rank()
            rank.prize_structure_id = prize_structure.pk
            rank.rank               = 1
            rank.amount             = cash_amount
            rank.save()

    # #
    # # also create the "dan" structures
    # create_templates()