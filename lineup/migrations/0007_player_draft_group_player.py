# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('draftgroup', '0012_player_game_team'),
        ('lineup', '0006_lineup_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='draft_group_player',
            field=models.ForeignKey(to='draftgroup.Player', default=None),
            preserve_default=False,
        ),
    ]
