# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0007_currentcontest_upcomingcontestpool'),
    ]

    operations = [
        migrations.CreateModel(
            name='LiveContestPool',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('contest.contestpool',),
        ),
    ]
