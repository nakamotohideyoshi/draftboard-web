# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0018_merge'),
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
    ]
