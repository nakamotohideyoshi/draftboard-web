# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payout', '0003_auto_20150722_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payout',
            name='entry',
            field=models.OneToOneField(to='contest.Entry'),
        ),
        migrations.AlterField(
            model_name='payout',
            name='transaction',
            field=models.OneToOneField(to='transaction.Transaction'),
        ),
    ]
