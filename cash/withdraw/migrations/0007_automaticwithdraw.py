# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('withdraw', '0006_auto_20150425_0735'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutomaticWithdraw',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('auto_payout_below', models.DecimalField(max_digits=7, decimal_places=2)),
            ],
        ),
    ]
