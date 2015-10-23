# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0004_game_prev_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pbpdescription',
            name='srid',
            field=models.CharField(default='', unique=True, max_length=64),
        ),
    ]
