# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('mlb', '0007_auto_20150522_1936'),
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
            field=models.ForeignKey(to='contenttypes.ContentType', null=True, related_name='mlb_player_players_injury'),
        ),
    ]
