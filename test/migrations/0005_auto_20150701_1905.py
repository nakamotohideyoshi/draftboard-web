# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test', '0004_playerchild_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamechild',
            name='away',
            field=models.ForeignKey(null=True, related_name='gamechild_awayteam', to='test.TeamChild'),
        ),
        migrations.AddField(
            model_name='gamechild',
            name='home',
            field=models.ForeignKey(null=True, related_name='gamechild_hometeam', to='test.TeamChild'),
        ),
        migrations.AddField(
            model_name='gamechild',
            name='srid_away',
            field=models.CharField(null=True, max_length=64, help_text='away team sportsradar global id'),
        ),
        migrations.AddField(
            model_name='gamechild',
            name='srid_home',
            field=models.CharField(null=True, max_length=64, help_text='home team sportsradar global id'),
        ),
        migrations.AddField(
            model_name='gamechild',
            name='title',
            field=models.CharField(null=True, max_length=128),
        ),
    ]
