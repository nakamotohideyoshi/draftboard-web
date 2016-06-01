# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nhl', '0008_player_on_active_roster'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerstats',
            name='blk_att',
            field=models.IntegerField(default=0, help_text='this players shots which were subsequently blocked by an opposing skater'),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='ms',
            field=models.IntegerField(default=0, help_text='this players missed shots (shots wide of the goalie/net)'),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='played',
            field=models.IntegerField(default=0, help_text='a value of 1 indicates the player participated in the game. 0 indicates they did not play at all.'),
        ),
    ]
