# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('mlb', '0004_auto_20150510_0251'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 12, 23, 48, 36, 576496, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='team',
            name='srid',
            field=models.CharField(default='', help_text='the sportsradar global id', max_length=64, unique=True),
            preserve_default=False,
        ),
    ]
