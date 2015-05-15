# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0013_gameboxscore'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gameboxscore',
            old_name='away_points',
            new_name='away_score',
        ),
        migrations.RenameField(
            model_name='gameboxscore',
            old_name='home_points',
            new_name='home_score',
        ),
    ]
