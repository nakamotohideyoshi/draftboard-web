# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nfl', '0001_squashed_0009_auto_20160119_2126'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='lineup_nickname',
            field=models.CharField(max_length=64, help_text='sets the the automatically generated name for lineups using this player', default=''),
        ),
    ]
