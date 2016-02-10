# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0002_auto_20160209_2241'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClosedContest',
            fields=[
            ],
            options={
                'verbose_name_plural': 'Paid Out',
                'proxy': True,
                'verbose_name': 'Paid Out',
            },
            bases=('contest.contest',),
        ),
        migrations.CreateModel(
            name='ClosedEntry',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('contest.entry',),
        ),
    ]
