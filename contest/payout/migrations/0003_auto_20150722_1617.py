# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payout', '0002_payout'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payout',
            name='entry',
            field=models.ForeignKey(unique=True, to='contest.Entry'),
        ),
        migrations.AlterField(
            model_name='payout',
            name='transaction',
            field=models.ForeignKey(unique=True, to='transaction.Transaction'),
        ),
    ]
