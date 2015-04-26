# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('withdraw', '0008_pendingwithdrawmax'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashoutWithdrawSetting',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created', models.DateTimeField(null=True, auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('max_withdraw_amount', models.DecimalField(max_digits=9, decimal_places=2)),
                ('min_withdraw_amount', models.DecimalField(max_digits=9, decimal_places=2)),
            ],
        ),
        migrations.AlterField(
            model_name='automaticwithdraw',
            name='auto_payout_below',
            field=models.DecimalField(max_digits=9, decimal_places=2),
        ),
    ]
