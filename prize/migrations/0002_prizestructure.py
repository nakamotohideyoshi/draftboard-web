# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prize', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrizeStructure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(blank=True, default='', max_length=128)),
                ('buyin', models.IntegerField(default=0)),
                ('first_place', models.IntegerField(default=0)),
                ('round_payouts', models.IntegerField(default=0)),
                ('payout_spots', models.IntegerField(default=0)),
                ('prize_pool', models.IntegerField(default=0)),
            ],
        ),
    ]
