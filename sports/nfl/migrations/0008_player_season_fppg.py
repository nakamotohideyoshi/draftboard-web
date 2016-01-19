# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nfl', '0007_auto_20160110_2223'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='season_fppg',
            field=models.FloatField(default=0.0),
        ),
    ]
