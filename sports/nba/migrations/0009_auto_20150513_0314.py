# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0008_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 5, 13, 3, 14, 2, 79774, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='srid',
            field=models.CharField(help_text='the sportsradar global id', unique=True, max_length=64, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='srid_away',
            field=models.CharField(help_text='away team sportsradar global id', max_length=64, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='srid_home',
            field=models.CharField(help_text='home team sportsradar global id', max_length=64, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='title',
            field=models.CharField(null=True, max_length=128),
        ),
    ]
