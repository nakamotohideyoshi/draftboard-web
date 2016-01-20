# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('nhl', '0008_player_season_fppg'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='updated',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 1, 19, 2, 25, 48, 263284, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gameboxscore',
            name='updated',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 1, 19, 2, 25, 49, 607857, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='playerstats',
            name='updated',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 1, 19, 2, 25, 50, 775082, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
