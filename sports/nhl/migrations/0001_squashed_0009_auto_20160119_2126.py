# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    replaces = [('nhl', '0001_initial'), ('nhl', '0002_auto_20150528_2321'), ('nhl', '0003_auto_20150625_0016'), ('nhl', '0004_game_prev_status'), ('nhl', '0005_tsxinjury_tsxnews_tsxplayer_tsxteam_tsxtransaction'), ('nhl', '0006_auto_20160110_2115'), ('nhl', '0007_auto_20160110_2243'), ('nhl', '0008_player_season_fppg'), ('nhl', '0009_auto_20160119_2126')]

    dependencies = [
        ('sports', '0001_squashed_0008_auto_20160119_2124'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid', models.CharField(unique=True, max_length=64, help_text='the sportsradar global id')),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid_game', models.CharField(default=None, unique=True, max_length=64, help_text='the sportsradar global id for the game')),
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
                ('away_type', models.ForeignKey(to='contenttypes.ContentType', related_name='nhl_gameboxscore_away_team')),
                ('home_type', models.ForeignKey(to='contenttypes.ContentType', related_name='nhl_gameboxscore_home_team')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GamePortion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid_game', models.CharField(max_length=64, help_text='the sportsradar global id for the game this is associate with')),
                ('game_id', models.PositiveIntegerField()),
                ('category', models.CharField(default='', max_length=32, help_text='typically one of these: ["inning-half","quarter","period"]')),
                ('sequence', models.IntegerField(default=0, help_text='an ordering of all GamePortions with the same srid_game')),
                ('srid', models.CharField(default='', max_length=64)),
                ('game_type', models.ForeignKey(to='contenttypes.ContentType', related_name='nhl_gameportion_sport_game')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Injury',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('iid', models.CharField(unique=True, max_length=128, help_text='custom injury id')),
                ('player_id', models.PositiveIntegerField()),
                ('status', models.CharField(default='', max_length=32)),
                ('description', models.CharField(default='', max_length=1024)),
                ('srid', models.CharField(default='', max_length=64)),
                ('comment', models.CharField(default='', max_length=1024)),
                ('player_type', models.ForeignKey(to='contenttypes.ContentType', related_name='nhl_injury_injured_player')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pbp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid_game', models.CharField(max_length=64, help_text='the sportsradar global id for the game')),
                ('game_id', models.PositiveIntegerField()),
                ('game_type', models.ForeignKey(to='contenttypes.ContentType', related_name='nhl_pbp_sport_game')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PbpDescription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('pbp_id', models.PositiveIntegerField()),
                ('portion_id', models.PositiveIntegerField()),
                ('idx', models.IntegerField(default=0)),
                ('description', models.CharField(default='', max_length=1024)),
                ('srid', models.CharField(default='', max_length=64)),
                ('pbp_type', models.ForeignKey(to='contenttypes.ContentType', related_name='nhl_pbpdescription_pbpdesc_pbp')),
                ('portion_type', models.ForeignKey(to='contenttypes.ContentType', related_name='nhl_pbpdescription_pbpdesc_portion')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid', models.CharField(unique=True, max_length=64, help_text='the sportsradar global id')),
                ('first_name', models.CharField(max_length=32)),
                ('last_name', models.CharField(max_length=32)),
                ('injury_id', models.PositiveIntegerField(null=True)),
                ('srid_team', models.CharField(default='', max_length=64)),
                ('birth_place', models.CharField(default='', max_length=64)),
                ('birthdate', models.CharField(default='', max_length=64)),
                ('college', models.CharField(default='', max_length=64)),
                ('experience', models.FloatField(default=0.0)),
                ('height', models.FloatField(default=0.0, help_text='inches')),
                ('weight', models.FloatField(default=0.0, help_text='lbs')),
                ('jersey_number', models.CharField(default='', max_length=64)),
                ('status', models.CharField(default='', max_length=64, help_text='roster status - ie: "ACT" means they are ON the roster. Not particularly active as in not-injured!')),
                ('draft_pick', models.CharField(default='', max_length=64)),
                ('draft_round', models.CharField(default='', max_length=64)),
                ('draft_year', models.CharField(default='', max_length=64)),
                ('srid_draft_team', models.CharField(default='', max_length=64)),
                ('injury_type', models.ForeignKey(null=True, to='contenttypes.ContentType', related_name='nhl_player_players_injury')),
                ('position', models.ForeignKey(to='sports.Position', related_name='nhl_player_player_position')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PlayerStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid_game', models.CharField(max_length=64, help_text='the sportsradar global id for the game')),
                ('srid_player', models.CharField(max_length=64, help_text='the sportsradar global id for the player')),
                ('game_id', models.PositiveIntegerField()),
                ('player_id', models.PositiveIntegerField()),
                ('fantasy_points', models.FloatField(default=0.0)),
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
                ('position', models.ForeignKey(to='sports.Position', related_name='nhl_playerstats_playerstats_position')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid', models.CharField(unique=True, max_length=64, help_text='the sportsradar global id')),
                ('srid_venue', models.CharField(max_length=64, help_text='the sportsradar global id')),
                ('name', models.CharField(default='', max_length=64, help_text='the team name, without the market/city. ie: "Lakers", or "Eagles"')),
                ('alias', models.CharField(default='', max_length=64, help_text='the abbreviation for the team, ie: for Boston Celtic alias == "BOS"')),
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
            model_name='game',
            name='away',
            field=models.ForeignKey(to='nhl.Team', related_name='game_awayteam'),
        ),
        migrations.AddField(
            model_name='game',
            name='home',
            field=models.ForeignKey(to='nhl.Team', related_name='game_hometeam'),
        ),
        migrations.AlterField(
            model_name='gameboxscore',
            name='coverage',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='game',
            name='prev_status',
            field=models.CharField(default='', max_length=32),
        ),
        migrations.CreateModel(
            name='TsxInjury',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('srid', models.CharField(max_length=64, help_text='the sportradar global id for the item')),
                ('pcid', models.CharField(max_length=64, help_text='the providers content id for this item')),
                ('content_created', models.DateTimeField()),
                ('content_modified', models.DateTimeField()),
                ('content_published', models.DateTimeField()),
                ('title', models.CharField(max_length=256)),
                ('byline', models.CharField(max_length=256)),
                ('dateline', models.CharField(max_length=32)),
                ('credit', models.CharField(max_length=128)),
                ('content', models.CharField(max_length=8192)),
                ('tsxcontent', models.ForeignKey(to='sports.TsxContent', related_name='nhl_tsxinjury_tsxcontent')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TsxNews',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('srid', models.CharField(max_length=64, help_text='the sportradar global id for the item')),
                ('pcid', models.CharField(max_length=64, help_text='the providers content id for this item')),
                ('content_created', models.DateTimeField()),
                ('content_modified', models.DateTimeField()),
                ('content_published', models.DateTimeField()),
                ('title', models.CharField(max_length=256)),
                ('byline', models.CharField(max_length=256)),
                ('dateline', models.CharField(max_length=32)),
                ('credit', models.CharField(max_length=128)),
                ('content', models.CharField(max_length=8192)),
                ('tsxcontent', models.ForeignKey(to='sports.TsxContent', related_name='nhl_tsxnews_tsxcontent')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TsxPlayer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sportsdataid', models.CharField(max_length=64)),
                ('sportradarid', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=128)),
                ('tsxitem_id', models.PositiveIntegerField()),
                ('tsxitem_type', models.ForeignKey(to='contenttypes.ContentType', related_name='nhl_tsxplayer_tsxitem_tsxitemref')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TsxTeam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sportsdataid', models.CharField(max_length=64)),
                ('sportradarid', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=128)),
                ('tsxitem_id', models.PositiveIntegerField()),
                ('tsxitem_type', models.ForeignKey(to='contenttypes.ContentType', related_name='nhl_tsxteam_tsxitem_tsxitemref')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TsxTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('srid', models.CharField(max_length=64, help_text='the sportradar global id for the item')),
                ('pcid', models.CharField(max_length=64, help_text='the providers content id for this item')),
                ('content_created', models.DateTimeField()),
                ('content_modified', models.DateTimeField()),
                ('content_published', models.DateTimeField()),
                ('title', models.CharField(max_length=256)),
                ('byline', models.CharField(max_length=256)),
                ('dateline', models.CharField(max_length=32)),
                ('credit', models.CharField(max_length=128)),
                ('content', models.CharField(max_length=8192)),
                ('tsxcontent', models.ForeignKey(to='sports.TsxContent', related_name='nhl_tsxtransaction_tsxcontent')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='injury',
            name='ddtimestamp',
            field=models.BigIntegerField(default=0, help_text='the time this injury update was parsed by dataden.this will be the same value for all objects that were in the feed on the last parse.'),
        ),
        migrations.AddField(
            model_name='tsxplayer',
            name='content_published',
            field=models.DateTimeField(default=datetime.datetime(1999, 1, 1, 12, 0, tzinfo=utc), help_text='the item ref is a GFK so also store the publish date here for ordering purposes.'),
        ),
        migrations.AddField(
            model_name='tsxplayer',
            name='player',
            field=models.ForeignKey(to='nhl.Player', default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tsxteam',
            name='content_published',
            field=models.DateTimeField(default=datetime.datetime(1999, 1, 1, 12, 0, tzinfo=utc), help_text='the item ref is a GFK so also store the publish date here for ordering purposes.'),
        ),
        migrations.AddField(
            model_name='tsxteam',
            name='team',
            field=models.ForeignKey(to='nhl.Team', default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tsxinjury',
            name='content',
            field=models.CharField(max_length=16384),
        ),
        migrations.AlterField(
            model_name='tsxnews',
            name='content',
            field=models.CharField(max_length=16384),
        ),
        migrations.AlterField(
            model_name='tsxtransaction',
            name='content',
            field=models.CharField(max_length=16384),
        ),
        migrations.AddField(
            model_name='player',
            name='season_fppg',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='game',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 19, 2, 25, 48, 263284, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gameboxscore',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 19, 2, 25, 49, 607857, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='playerstats',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 19, 2, 25, 50, 775082, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
