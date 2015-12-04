# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
# import ticket.models   # we just need this for ticket.models.DEFAULT_TICKET_VALUES
#
# def load_initial_data(apps, schema_editor):
#     """
#     installs the very standard prize structures for headsup games
#
#     to do that we need to create the ranks, generators, and prizestrucutre entries
#
#     [
# 	{
# 		"model": "prize.generatorsettings",
# 		"fields": {
# 			"round_payouts": 0,
# 			"payout_spots": 1,
# 			"buyin": 1.0,
# 			"first_place": 1.8,
# 			"prize_pool": 1.8
# 		},
# 		"pk": 1
# 	},
#
# 	{
# 		"model": "prize.prizestructure",
# 		"fields": {
# 			"generator": 1,
# 			"created": "2015-12-04T15:12:46.923Z",
# 			"name": "new prize structure"
# 		},
# 		"pk": 1
# 	},
#
# 	{
# 		"model": "prize.rank",
# 		"fields": {
# 			"amount_type": 20,
# 			"amount_id": 1,
# 			"rank": 1,
# 			"prize_structure": 1
# 		},
# 		"pk": 1
# 	}
# ]
#     """
#
#     #
#     # amounts we want to create Headsup prize structures for
#     #amounts = [ 1.00, 2.00, 5.00, 10.00, 20.00, 50.00, 100.00, 200.00, 500.00 ]
#     amounts = [ x[0] for x in ticket.models.DEFAULT_TICKET_VALUES ]
#
#     #
#     # get the model by name
#     CashAmount          = apps.get_model('cash',  'CashAmount')
#     GeneratorSettings   = apps.get_model('prize', 'GeneratorSettings')
#     PrizeStructure      = apps.get_model('prize', 'PrizeStructure')
#     Rank                = apps.get_model('prize', 'Rank')
#
#     #
#     # create HEADS-UP  (1v1) prize structures for the list of amounts
#     for amount in amounts:
#         try:
#             # check if we already made the generator for this amount
#             generator_settings = GeneratorSettings.objects.get( buyin=amount )
#         except GeneratorSettings.DoesNotExist:
#             #
#             generator_settings = GeneratorSettings()
#             generator_settings.buyin            = amount
#             generator_settings.first_place      = (amount*2) - (amount * 0.1)    # take out rake: 10%
#             generator_settings.round_payouts    = 1
#             generator_settings.payout_spots     = 1
#             generator_settings.prize_pool       = 1.8
#             generator_settings.save()
#
#         try:
#             # check if we already made the prize structure for this amount
#             prize_structure = PrizeStructure.objects.get( generator__buyin=amount )
#         except PrizeStructure.DoesNotExist:
#             #
#             prize_structure = PrizeStructure()
#             prize_structure.generator   = generator_settings
#             prize_structure.name        = '$%.0f Head-to-Head' % amount
#             prize_structure.save()
#
#         cash_amount, created = CashAmount.objects.get_or_create(amount=amount)
#
#         try:
#             #
#             # there is only going to be ONE rank (payout) per headsup prize structure
#             rank = Rank.objects.get( prize_structure=prize_structure )
#         except Rank.DoesNotExist:
#             #
#             rank                    = Rank()
#             rank.prize_structure    = prize_structure
#             rank.rank               = 1
#             rank.amount             = cash_amount
#             rank.save()

class Migration(migrations.Migration):

    dependencies = [
        ('prize', '0004_auto_20150902_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generatorsettings',
            name='buyin',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='generatorsettings',
            name='first_place',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='generatorsettings',
            name='prize_pool',
            field=models.FloatField(default=0),
        ),

        # #
        # # custom method to run with this migration
        # # which will install some initial prize structures
        # migrations.RunPython( load_initial_data )
    ]
