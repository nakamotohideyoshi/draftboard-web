# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mlb', '0018_gameboxscore_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameboxscore',
            name='srid_game',
            field=models.CharField(default=None, unique=True, max_length=64, help_text='the sportsradar global id for the game'),
        ),
    ]
