# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test', '0013_playerchild_lineup_nickname'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamechild',
            name='season_type',
            field=models.CharField(max_length=32, choices=[('pre', 'Preseason'), ('reg', 'Regular Season'), ('pst', 'Postseason')], default='reg'),
        ),
        migrations.AddField(
            model_name='gamechild',
            name='season_year',
            field=models.IntegerField(default=0, help_text='the year the season started'),
        ),
        migrations.AlterField(
            model_name='playerchild',
            name='lineup_nickname',
            field=models.CharField(max_length=64, blank=True, default='', help_text='sets the the automatically generated name for lineups using this player'),
        ),
    ]
