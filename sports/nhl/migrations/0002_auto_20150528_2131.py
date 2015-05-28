# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('sports', '0003_auto_20150528_2131'),
        ('nhl', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
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
            name='GameBoxscore',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid_game', models.CharField(help_text='the sportsradar global id for the game', default=None, unique=True, max_length=64)),
                ('srid_home', models.CharField(max_length=64)),
                ('srid_away', models.CharField(max_length=64)),
                ('home_id', models.PositiveIntegerField()),
                ('away_id', models.PositiveIntegerField()),
                ('attendance', models.IntegerField(default=0)),
                ('coverage', models.CharField(default='', max_length=16)),
                ('status', models.CharField(default='', max_length=64)),
                ('home_score', models.IntegerField(default=0)),
                ('away_score', models.IntegerField(default=0)),
                ('title', models.CharField(default='', max_length=256)),
                ('home_scoring_json', models.CharField(default='', max_length=2048)),
                ('away_scoring_json', models.CharField(default='', max_length=2048)),
                ('clock', models.CharField(default='', max_length=16)),
                ('period', models.CharField(default='', max_length=16)),
                ('away_type', models.ForeignKey(related_name='nhl_gameboxscore_away_team', to='contenttypes.ContentType')),
                ('home_type', models.ForeignKey(related_name='nhl_gameboxscore_home_team', to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GamePortion',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid_game', models.CharField(help_text='the sportsradar global id for the game this is associate with', max_length=64)),
                ('game_id', models.PositiveIntegerField()),
                ('category', models.CharField(help_text='typically one of these: ["inning-half","quarter","period"]', default='', max_length=32)),
                ('sequence', models.IntegerField(help_text='an ordering of all GamePortions with the same srid_game', default=0)),
                ('srid', models.CharField(default='', max_length=64)),
                ('game_type', models.ForeignKey(related_name='nhl_gameportion_sport_game', to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Injury',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('iid', models.CharField(help_text='custom injury id', unique=True, max_length=64)),
                ('player_id', models.PositiveIntegerField()),
                ('status', models.CharField(default='', max_length=32)),
                ('description', models.CharField(default='', max_length=1024)),
                ('srid', models.CharField(default='', max_length=64)),
                ('comment', models.CharField(default='', max_length=1024)),
                ('player_type', models.ForeignKey(related_name='nhl_injury_injured_player', to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pbp',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid_game', models.CharField(help_text='the sportsradar global id for the game', max_length=64)),
                ('game_id', models.PositiveIntegerField()),
                ('game_type', models.ForeignKey(related_name='nhl_pbp_sport_game', to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PbpDescription',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('pbp_id', models.PositiveIntegerField()),
                ('portion_id', models.PositiveIntegerField()),
                ('idx', models.IntegerField(default=0)),
                ('description', models.CharField(default='', max_length=1024)),
                ('srid', models.CharField(default='', max_length=64)),
                ('pbp_type', models.ForeignKey(related_name='nhl_pbpdescription_pbpdesc_pbp', to='contenttypes.ContentType')),
                ('portion_type', models.ForeignKey(related_name='nhl_pbpdescription_pbpdesc_portion', to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid', models.CharField(help_text='the sportsradar global id', unique=True, max_length=64)),
                ('first_name', models.CharField(max_length=32)),
                ('last_name', models.CharField(max_length=32)),
                ('injury_id', models.PositiveIntegerField(null=True)),
                ('srid_team', models.CharField(default='', max_length=64)),
                ('birth_place', models.CharField(default='', max_length=64)),
                ('birthdate', models.CharField(default='', max_length=64)),
                ('college', models.CharField(default='', max_length=64)),
                ('experience', models.FloatField(default=0.0)),
                ('height', models.FloatField(help_text='inches', default=0.0)),
                ('weight', models.FloatField(help_text='lbs', default=0.0)),
                ('jersey_number', models.CharField(default='', max_length=64)),
                ('primary_position', models.CharField(default='', max_length=64)),
                ('status', models.CharField(help_text='roster status - ie: "ACT" means they are ON the roster. Not particularly active as in not-injured!', default='', max_length=64)),
                ('draft_pick', models.CharField(default='', max_length=64)),
                ('draft_round', models.CharField(default='', max_length=64)),
                ('draft_year', models.CharField(default='', max_length=64)),
                ('srid_draft_team', models.CharField(default='', max_length=64)),
                ('injury_type', models.ForeignKey(null=True, to='contenttypes.ContentType', related_name='nhl_player_players_injury')),
                ('position', models.ForeignKey(related_name='nhl_player_player_position', to='sports.Position')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PlayerStats',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid_game', models.CharField(help_text='the sportsradar global id for the game', max_length=64)),
                ('srid_player', models.CharField(help_text='the sportsradar global id for the player', max_length=64)),
                ('game_id', models.PositiveIntegerField()),
                ('player_id', models.PositiveIntegerField()),
                ('fantasy_points', models.FloatField(default=0.0)),
                ('position', models.CharField(default='', max_length=16)),
                ('primary_position', models.CharField(default='', max_length=16)),
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
                ('game_type', models.ForeignKey(related_name='nhl_playerstats_sport_game', to='contenttypes.ContentType')),
                ('player_type', models.ForeignKey(related_name='nhl_playerstats_sport_player', to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
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
