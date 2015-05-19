# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nhl', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid', models.CharField(help_text='the sportsradar global id', unique=True, max_length=64)),
                ('start', models.DateTimeField()),
                ('status', models.CharField(max_length=32)),
                ('srid_home', models.CharField(help_text='home team sportsradar global id', max_length=64)),
                ('srid_away', models.CharField(help_text='away team sportsradar global id', max_length=64)),
                ('title', models.CharField(null=True, max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid', models.CharField(help_text='the sportsradar global id', unique=True, max_length=64)),
                ('first_name', models.CharField(max_length=32)),
                ('last_name', models.CharField(max_length=32)),
                ('srid_team', models.CharField(default='', max_length=64)),
                ('birth_place', models.CharField(default='', max_length=64)),
                ('birthdate', models.CharField(default='', max_length=64)),
                ('college', models.CharField(default='', max_length=64)),
                ('experience', models.FloatField(default=0.0)),
                ('height', models.FloatField(help_text='inches', default=0.0)),
                ('weight', models.FloatField(help_text='lbs', default=0.0)),
                ('jersey_number', models.CharField(default='', max_length=64)),
                ('position', models.CharField(default='', max_length=64)),
                ('primary_position', models.CharField(default='', max_length=64)),
                ('status', models.CharField(help_text='roster status - ie: "ACT" means they are ON the roster. Not particularly active as in not-injured!', default='', max_length=64)),
                ('draft_pick', models.CharField(default='', max_length=64)),
                ('draft_round', models.CharField(default='', max_length=64)),
                ('draft_year', models.CharField(default='', max_length=64)),
                ('srid_draft_team', models.CharField(default='', max_length=64)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PlayerStats',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid_game', models.CharField(help_text='the sportsradar global id for the game', max_length=64)),
                ('srid_player', models.CharField(help_text='the sportsradar global id for the player', max_length=64)),
                ('game', models.ForeignKey(to='nhl.Game')),
                ('player', models.ForeignKey(to='nhl.Player')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('start_year', models.CharField(max_length=100)),
                ('season_type', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid', models.CharField(help_text='the sportsradar global id', unique=True, max_length=64)),
                ('srid_venue', models.CharField(help_text='the sportsradar global id', max_length=64)),
                ('name', models.CharField(help_text='the team name, without the market/city. ie: "Lakers", or "Eagles"', default='', max_length=64)),
                ('alias', models.CharField(help_text='the abbreviation for the team, ie: for Boston Celtic alias == "BOS"', default='', max_length=64)),
                ('srid_league', models.CharField(help_text='league sportsradar id', max_length=64)),
                ('srid_conference', models.CharField(help_text='conference sportsradar id', max_length=64)),
                ('srid_division', models.CharField(help_text='division sportsradar id', max_length=64)),
                ('market', models.CharField(max_length=64)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(to='nhl.Team'),
        ),
        migrations.AddField(
            model_name='game',
            name='away',
            field=models.ForeignKey(related_name='game_awayteam', to='nhl.Team'),
        ),
        migrations.AddField(
            model_name='game',
            name='home',
            field=models.ForeignKey(related_name='game_hometeam', to='nhl.Team'),
        ),
    ]
