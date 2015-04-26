# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('withdraw', '0009_auto_20150426_0630'),
    ]

    operations = [
        migrations.AddField(
            model_name='paypalwithdraw',
            name='paypal_errors',
            field=models.CharField(default='', max_length=2048),
        ),
        migrations.AddField(
            model_name='paypalwithdraw',
            name='started_processing',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='cashoutwithdrawsetting',
            name='max_withdraw_amount',
            field=models.DecimalField(default=10000.0, max_digits=9, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='cashoutwithdrawsetting',
            name='min_withdraw_amount',
            field=models.DecimalField(default=5.0, max_digits=9, decimal_places=2),
        ),
    ]
