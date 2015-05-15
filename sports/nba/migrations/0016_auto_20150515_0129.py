# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0015_auto_20150515_0057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameboxscore',
            name='srid_game',
            field=models.CharField(default=None, unique=True, max_length=64, help_text='the sportsradar global id for the game'),
        ),
    ]
