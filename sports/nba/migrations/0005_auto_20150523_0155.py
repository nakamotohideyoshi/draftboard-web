# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0004_gameportion_pbp_pbpdescription'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameportion',
            name='srid',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='pbpdescription',
            name='srid',
            field=models.CharField(default='', max_length=64),
        ),
    ]
