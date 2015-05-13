# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mlb', '0008_auto_20150513_0314'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 13, 4, 23, 55, 783137, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='venue',
            name='srid',
            field=models.CharField(max_length=64, default='', help_text='the sportsradar global id', unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='team',
            name='srid_venue',
            field=models.CharField(max_length=64, help_text='the sportsradar global id'),
        ),
    ]
