# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('withdraw', '0003_auto_20150422_2149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviewpendingwithdraw',
            name='cash_transaction_detail',
        ),
        migrations.RemoveField(
            model_name='reviewpendingwithdraw',
            name='created',
        ),
        migrations.RemoveField(
            model_name='reviewpendingwithdraw',
            name='status',
        ),
        migrations.RemoveField(
            model_name='reviewpendingwithdraw',
            name='status_updated',
        ),
    ]
