# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ticket.models

def load_initial_data(apps, schema_editor):
    """
    create the CashAmount objects for the initial Ticket amounts

    :param apps:
    :param schema_editor:
    :return:
    """

    CashAmount          = apps.get_model('cash',  'CashAmount')

    amounts = [ x[0] for x in ticket.models.DEFAULT_TICKET_VALUES ]
    for amount in amounts:
        try:
            cash_amount = CashAmount.objects.get( amount=amount )
        except CashAmount.DoesNotExist:
            cash_amount = CashAmount()
            cash_amount.amount = amount
            cash_amount.save()

class Migration(migrations.Migration):

    dependencies = [
        ('cash', '0008_optimalpaymentstransaction'),
    ]

    operations = [

        #
        # make the initial CashAmounts
        migrations.RunPython( load_initial_data ),
    ]
