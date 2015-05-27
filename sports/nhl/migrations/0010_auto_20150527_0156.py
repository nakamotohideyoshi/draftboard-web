# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('nhl', '0009_pbpdescription_srid'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='injury_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='injury_type',
            field=models.ForeignKey(to='contenttypes.ContentType', null=True, related_name='nhl_player_players_injury'),
        ),
    ]
