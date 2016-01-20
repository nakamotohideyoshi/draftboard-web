# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('mlb', '0008_player_season_fppg'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 19, 2, 26, 16, 176028, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gameboxscore',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 19, 2, 26, 17, 112077, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='playerstatshitter',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 19, 2, 26, 18, 31855, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='playerstatspitcher',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 19, 2, 26, 19, 408245, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
