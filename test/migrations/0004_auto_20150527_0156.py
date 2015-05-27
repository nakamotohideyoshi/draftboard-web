# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('test', '0003_auto_20150520_2122'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerchild',
            name='injury_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='playerchild',
            name='injury_type',
            field=models.ForeignKey(to='contenttypes.ContentType', null=True, related_name='test_playerchild_players_injury'),
        ),
    ]
