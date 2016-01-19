# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0009_auto_20160110_2242'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='season_fppg',
            field=models.FloatField(default=0.0),
        ),
    ]
