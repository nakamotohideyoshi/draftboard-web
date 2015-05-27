# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('nfl', '0002_auto_20150523_0214'),
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
            field=models.ForeignKey(to='contenttypes.ContentType', null=True, related_name='nfl_player_players_injury'),
        ),
    ]
