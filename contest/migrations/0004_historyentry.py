# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0003_completedcontest'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoryEntry',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('contest.entry',),
        ),
    ]
