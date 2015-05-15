# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mlb', '0016_playerstatspitcher_r_total'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameBoxscore',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid_game', models.CharField(help_text='the sportsradar global id for the game', max_length=64)),
                ('srid_home', models.CharField(max_length=64)),
                ('srid_away', models.CharField(max_length=64)),
                ('attendance', models.IntegerField(default=0)),
                ('coverage', models.CharField(default='', max_length=16)),
                ('status', models.CharField(default='', max_length=64)),
                ('home_score', models.IntegerField(default=0)),
                ('away_score', models.IntegerField(default=0)),
                ('day_night', models.CharField(default='', max_length=8)),
                ('game_number', models.IntegerField(default=1)),
                ('inning', models.CharField(default='', max_length=16)),
                ('inning_half', models.CharField(default='', max_length=16)),
                ('srid_home_pp', models.CharField(help_text='srid of the HOME probable pitcher set before the game starts', max_length=64)),
                ('srid_home_sp', models.CharField(help_text='srid of the HOME starting pitcher', max_length=64)),
                ('srid_away_pp', models.CharField(help_text='srid of the AWAY probable pitcher set before the game starts', max_length=64)),
                ('srid_away_sp', models.CharField(help_text='srid of the AWAY starting pitcher', max_length=64)),
                ('srid_win', models.CharField(max_length=64)),
                ('srid_loss', models.CharField(max_length=64)),
                ('srid_hold', models.CharField(max_length=64)),
                ('srid_save', models.CharField(max_length=64)),
                ('home_errors', models.IntegerField(default=0)),
                ('home_hits', models.IntegerField(default=0)),
                ('away_errors', models.IntegerField(default=0)),
                ('away_hits', models.IntegerField(default=0)),
                ('home_scoring_json', models.CharField(default='', max_length=2048)),
                ('away_scoring_json', models.CharField(default='', max_length=2048)),
                ('away', models.ForeignKey(related_name='gameboxscore_away', to='mlb.Team')),
                ('home', models.ForeignKey(related_name='gameboxscore_home', to='mlb.Team')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
