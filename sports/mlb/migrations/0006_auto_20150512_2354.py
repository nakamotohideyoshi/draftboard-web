# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('mlb', '0005_auto_20150512_2352'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameboxscore',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 5, 12, 23, 54, 16, 485794, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gameboxscore',
            name='srid_game',
            field=models.CharField(help_text='the sportsradar global id for the game', max_length=64, default=''),
            preserve_default=False,
        ),
    ]
