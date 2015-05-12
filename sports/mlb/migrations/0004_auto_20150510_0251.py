# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mlb', '0003_gameboxscore_injury_player_playerstats_playerstatsseason_rosterplayer_team_venue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerstats',
            name='srid_game',
            field=models.CharField(max_length=64, help_text='the sportsradar global id for the game'),
        ),
        migrations.AlterField(
            model_name='playerstats',
            name='srid_player',
            field=models.CharField(max_length=64, help_text='the sportsradar global id for the player'),
        ),
    ]
