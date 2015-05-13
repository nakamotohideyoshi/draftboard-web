# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('mlb', '0007_auto_20150513_0143'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 5, 13, 3, 13, 51, 264377, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='srid',
            field=models.CharField(help_text='the sportsradar global id', unique=True, max_length=64, default=''),
            preserve_default=False,
        ),
    ]
