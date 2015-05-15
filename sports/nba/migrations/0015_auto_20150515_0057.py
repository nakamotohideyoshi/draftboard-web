# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0014_auto_20150515_0046'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameboxscore',
            name='away_scoring_json',
            field=models.CharField(max_length=2048, default=''),
        ),
        migrations.AddField(
            model_name='gameboxscore',
            name='home_scoring_json',
            field=models.CharField(max_length=2048, default=''),
        ),
    ]
