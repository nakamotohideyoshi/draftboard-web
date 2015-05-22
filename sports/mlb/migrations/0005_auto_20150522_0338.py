# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mlb', '0004_pbp_pbpdescription'),
    ]

    operations = [
        migrations.AddField(
            model_name='pbp',
            name='srid_game',
            field=models.CharField(default=None, max_length=64, help_text='the sportsradar global id for the game'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pbpdescription',
            name='idx',
            field=models.IntegerField(default=0),
        ),
    ]
