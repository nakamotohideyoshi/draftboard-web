# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0006_auto_20160325_2357'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrentContest',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('contest.contest',),
        ),
        migrations.CreateModel(
            name='UpcomingContestPool',
            fields=[
            ],
            options={
                'verbose_name_plural': 'Upcoming',
                'proxy': True,
                'verbose_name': 'Upcoming',
            },
            bases=('contest.contestpool',),
        ),
    ]
