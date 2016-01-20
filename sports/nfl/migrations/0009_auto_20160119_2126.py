# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('nfl', '0008_player_season_fppg'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 19, 2, 26, 4, 328274, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gameboxscore',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 19, 2, 26, 5, 335073, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='playerstats',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 19, 2, 26, 6, 408614, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
