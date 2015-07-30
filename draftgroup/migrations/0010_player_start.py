# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('draftgroup', '0009_player_salary'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 29, 23, 44, 9, 347606, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
