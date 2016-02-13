# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('draftgroup', '0017_player_final_fantasy_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='draftgroup',
            name='fantasy_points_finalized',
            field=models.DateTimeField(blank=True, help_text='if set, this is the time the "final_fantasy_points" for each draftgroup player was updated', null=True),
        ),
    ]
