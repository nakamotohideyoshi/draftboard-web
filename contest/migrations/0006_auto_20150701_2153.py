# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0005_contest_site_sport'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoryContest',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('contest.contest',),
        ),
        migrations.CreateModel(
            name='LiveContest',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('contest.contest',),
        ),
        migrations.CreateModel(
            name='UpcomingContest',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('contest.contest',),
        ),
        migrations.RemoveField(
            model_name='contest',
            name='today_only',
        ),
        migrations.AlterField(
            model_name='contest',
            name='status',
            field=models.CharField(default='scheduled', max_length=32, choices=[('Upcoming', (('reservable', 'Reservable'), ('scheduled', 'Scheduled'))), ('Live', (('inprogress', 'In Progress'), ('completed', 'Completed'))), ('History', (('closed', 'Closed'), ('cancelled', 'Cancelled')))]),
        ),
    ]
