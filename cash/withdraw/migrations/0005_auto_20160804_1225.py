# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-04 16:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('withdraw', '0004_payouttransaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkwithdraw',
            name='net_profit',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='paypalwithdraw',
            name='net_profit',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
            preserve_default=False,
        ),
    ]
