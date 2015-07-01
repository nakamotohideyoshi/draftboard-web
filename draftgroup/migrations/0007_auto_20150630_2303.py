# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('draftgroup', '0006_player_created'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gameteam',
            old_name='game_start',
            new_name='start',
        ),
    ]
