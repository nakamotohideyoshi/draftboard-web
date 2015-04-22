# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cash', '0003_withdrawalstatus'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='withdrawalstatus',
            name='cash_transaction_detail',
        ),
        migrations.DeleteModel(
            name='WithdrawalStatus',
        ),
    ]
