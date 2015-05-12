# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0003_player_playerstats'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerstats',
            name='fouls',
            field=models.FloatField(default=0.0),
        ),
    ]
