# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mlb', '0010_auto_20150513_1929'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='attendance',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='game',
            name='away',
            field=models.ForeignKey(to='mlb.Team', default=None, related_name='game_awayteam'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='day_night',
            field=models.CharField(default='', max_length=8),
        ),
        migrations.AddField(
            model_name='game',
            name='game_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='game',
            name='home',
            field=models.ForeignKey(to='mlb.Team', default=None, related_name='game_hometeam'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='srid_away',
            field=models.CharField(help_text='away team sportsradar global id', default='', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='srid_home',
            field=models.CharField(help_text='home team sportsradar global id', default='', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='title',
            field=models.CharField(null=True, max_length=128),
        ),
    ]
