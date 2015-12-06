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
        try:
            # check if we already made the generator for this amount
            generator_settings = GeneratorSettings.objects.get( buyin=amount )
        except GeneratorSettings.DoesNotExist:
            #
            first_place = (amount*2) - (amount * 0.1)  # take out rake: 10%
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
        cash_amount, created = CashAmount.objects.get_or_create(amount=amount)

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