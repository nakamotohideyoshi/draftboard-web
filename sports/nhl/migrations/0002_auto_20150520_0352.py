# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('nhl', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid', models.CharField(max_length=64, help_text='the sportsradar global id', unique=True)),
                ('start', models.DateTimeField()),
                ('status', models.CharField(max_length=32)),
                ('srid_home', models.CharField(max_length=64, help_text='home team sportsradar global id')),
                ('srid_away', models.CharField(max_length=64, help_text='away team sportsradar global id')),
                ('title', models.CharField(null=True, max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GameBoxscore',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid_game', models.CharField(max_length=64, help_text='the sportsradar global id for the game', default=None, unique=True)),
                ('srid_home', models.CharField(max_length=64)),
                ('srid_away', models.CharField(max_length=64)),
                ('attendance', models.IntegerField(default=0)),
                ('coverage', models.CharField(max_length=16, default='')),
                ('status', models.CharField(max_length=64, default='')),
                ('home_score', models.IntegerField(default=0)),
                ('away_score', models.IntegerField(default=0)),
                ('title', models.CharField(max_length=256, default='')),
                ('home_scoring_json', models.CharField(max_length=2048, default='')),
                ('away_scoring_json', models.CharField(max_length=2048, default='')),
                ('clock', models.CharField(max_length=16, default='')),
                ('period', models.CharField(max_length=16, default='')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid', models.CharField(max_length=64, help_text='the sportsradar global id', unique=True)),
                ('first_name', models.CharField(max_length=32)),
                ('last_name', models.CharField(max_length=32)),
                ('srid_team', models.CharField(max_length=64, default='')),
                ('birth_place', models.CharField(max_length=64, default='')),
                ('birthdate', models.CharField(max_length=64, default='')),
                ('college', models.CharField(max_length=64, default='')),
                ('experience', models.FloatField(default=0.0)),
                ('height', models.FloatField(help_text='inches', default=0.0)),
                ('weight', models.FloatField(help_text='lbs', default=0.0)),
                ('jersey_number', models.CharField(max_length=64, default='')),
                ('position', models.CharField(max_length=64, default='')),
                ('primary_position', models.CharField(max_length=64, default='')),
                ('status', models.CharField(max_length=64, help_text='roster status - ie: "ACT" means they are ON the roster. Not particularly active as in not-injured!', default='')),
                ('draft_pick', models.CharField(max_length=64, default='')),
                ('draft_round', models.CharField(max_length=64, default='')),
                ('draft_year', models.CharField(max_length=64, default='')),
                ('srid_draft_team', models.CharField(max_length=64, default='')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PlayerStats',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid_game', models.CharField(max_length=64, help_text='the sportsradar global id for the game')),
                ('srid_player', models.CharField(max_length=64, help_text='the sportsradar global id for the player')),
                ('game_id', models.PositiveIntegerField()),
                ('player_id', models.PositiveIntegerField()),
                ('fantasy_points', models.FloatField(default=0.0)),
                ('position', models.CharField(max_length=16, default='')),
                ('primary_position', models.CharField(max_length=16, default='')),
                ('goal', models.IntegerField(default=0)),
                ('assist', models.IntegerField(default=0)),
                ('sog', models.IntegerField(default=0)),
                ('blk', models.IntegerField(default=0)),
                ('sh_goal', models.IntegerField(default=0)),
                ('pp_goal', models.IntegerField(default=0)),
                ('so_goal', models.IntegerField(default=0)),
                ('w', models.BooleanField(default=False)),
                ('l', models.BooleanField(default=False)),
                ('otl', models.BooleanField(default=False)),
                ('saves', models.IntegerField(default=0)),
                ('ga', models.IntegerField(default=0)),
                ('shutout', models.BooleanField(default=False)),
                ('game_type', models.ForeignKey(to='contenttypes.ContentType', related_name='nhl_playerstats_sport_game')),
                ('player_type', models.ForeignKey(to='contenttypes.ContentType', related_name='nhl_playerstats_sport_player')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid', models.CharField(max_length=64, help_text='the sportsradar global id', unique=True)),
                ('srid_venue', models.CharField(max_length=64, help_text='the sportsradar global id')),
                ('name', models.CharField(max_length=64, help_text='the team name, without the market/city. ie: "Lakers", or "Eagles"', default='')),
                ('alias', models.CharField(max_length=64, help_text='the abbreviation for the team, ie: for Boston Celtic alias == "BOS"', default='')),
                ('srid_league', models.CharField(max_length=64, help_text='league sportsradar id')),
                ('srid_conference', models.CharField(max_length=64, help_text='conference sportsradar id')),
                ('srid_division', models.CharField(max_length=64, help_text='division sportsradar id')),
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
            model_name='gameboxscore',
            name='away',
            field=models.ForeignKey(to='nhl.Team', related_name='gameboxscore_away'),
        ),
        migrations.AddField(
            model_name='gameboxscore',
            name='home',
            field=models.ForeignKey(to='nhl.Team', related_name='gameboxscore_home'),
        ),
        migrations.AddField(
            model_name='game',
            name='away',
            field=models.ForeignKey(to='nhl.Team', related_name='game_awayteam'),
        ),
        migrations.AddField(
            model_name='game',
            name='home',
            field=models.ForeignKey(to='nhl.Team', related_name='game_hometeam'),
        ),
    ]
