# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lineup', '0007_player_draft_group_player'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='lineup',
            field=models.ForeignKey(to='lineup.Lineup', related_name='players'),
        ),
    ]
