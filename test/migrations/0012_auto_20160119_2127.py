# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('test', '0011_auto_20150918_1546'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamechild',
            name='updated',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 1, 19, 2, 26, 39, 240665, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='playerchild',
            name='season_fppg',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='playerstatschild',
            name='updated',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 1, 19, 2, 26, 40, 767100, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
