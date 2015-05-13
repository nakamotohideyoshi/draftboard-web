# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0009_auto_20150513_0314'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='away',
            field=models.ForeignKey(to='nba.Team', related_name='game_awayteam', default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='home',
            field=models.ForeignKey(to='nba.Team', related_name='game_hometeam', default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='birth_place',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='player',
            name='birthdate',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='player',
            name='college',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='player',
            name='draft_pick',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='player',
            name='draft_round',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='player',
            name='draft_year',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='player',
            name='experience',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='player',
            name='height',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='player',
            name='jersey_number',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='player',
            name='position',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='player',
            name='primary_position',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='player',
            name='srid_draft_team',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='player',
            name='srid_team',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='player',
            name='status',
            field=models.CharField(default='', help_text='roster status - ie: "ACT" means they are ON the roster. Not particularly active as in not-injured!', max_length=64),
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(default=None, to='nba.Team'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='weight',
            field=models.FloatField(default=0.0),
        ),
    ]
