# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    replaces = [('nfl', '0001_initial'), ('nfl', '0002_auto_20150528_2321'), ('nfl', '0003_auto_20150625_0016'), ('nfl', '0004_game_prev_status'), ('nfl', '0005_tsxinjury_tsxnews_tsxplayer_tsxteam_tsxtransaction'), ('nfl', '0006_auto_20160110_2114'), ('nfl', '0007_auto_20160110_2223'), ('nfl', '0008_player_season_fppg'), ('nfl', '0009_auto_20160119_2126')]

    dependencies = [
        ('sports', '0001_squashed_0008_auto_20160119_2124'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid', models.CharField(max_length=64, unique=True, help_text='the sportsradar global id')),
                ('start', models.DateTimeField()),
                ('status', models.CharField(max_length=32)),
                ('srid_home', models.CharField(max_length=64, help_text='home team sportsradar global id')),
                ('srid_away', models.CharField(max_length=64, help_text='away team sportsradar global id')),
                ('title', models.CharField(null=True, max_length=128)),
                ('weather_json', models.CharField(max_length=512)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GameBoxscore',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid_game', models.CharField(default=None, max_length=64, unique=True, help_text='the sportsradar global id for the game')),
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
                ('completed', models.CharField(default='', max_length=64)),
                ('quarter', models.CharField(default='', max_length=16)),
                ('away_type', models.ForeignKey(to='contenttypes.ContentType', related_name='nfl_gameboxscore_away_team')),
                ('home_type', models.ForeignKey(to='contenttypes.ContentType', related_name='nfl_gameboxscore_home_team')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GamePortion',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid_game', models.CharField(max_length=64, help_text='the sportsradar global id for the game this is associate with')),
                ('game_id', models.PositiveIntegerField()),
                ('category', models.CharField(default='', max_length=32, help_text='typically one of these: ["inning-half","quarter","period"]')),
                ('sequence', models.IntegerField(default=0, help_text='an ordering of all GamePortions with the same srid_game')),
                ('srid', models.CharField(default='', max_length=64)),
                ('game_type', models.ForeignKey(to='contenttypes.ContentType', related_name='nfl_gameportion_sport_game')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Injury',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('iid', models.CharField(max_length=128, unique=True, help_text='custom injury id')),
                ('player_id', models.PositiveIntegerField()),
                ('status', models.CharField(default='', max_length=32)),
                ('description', models.CharField(default='', max_length=1024)),
                ('srid', models.CharField(default='', max_length=64)),
                ('practice_status', models.CharField(default='', max_length=1024)),
                ('player_type', models.ForeignKey(to='contenttypes.ContentType', related_name='nfl_injury_injured_player')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pbp',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid_game', models.CharField(max_length=64, help_text='the sportsradar global id for the game')),
                ('game_id', models.PositiveIntegerField()),
                ('game_type', models.ForeignKey(to='contenttypes.ContentType', related_name='nfl_pbp_sport_game')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PbpDescription',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('pbp_id', models.PositiveIntegerField()),
                ('portion_id', models.PositiveIntegerField()),
                ('idx', models.IntegerField(default=0)),
                ('description', models.CharField(default='', max_length=1024)),
                ('srid', models.CharField(default='', max_length=64)),
                ('pbp_type', models.ForeignKey(to='contenttypes.ContentType', related_name='nfl_pbpdescription_pbpdesc_pbp')),
                ('portion_type', models.ForeignKey(to='contenttypes.ContentType', related_name='nfl_pbpdescription_pbpdesc_portion')),
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
                ('srid', models.CharField(max_length=64, unique=True, help_text='the sportsradar global id')),
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
                ('injury_type', models.ForeignKey(null=True, related_name='nfl_player_players_injury', to='contenttypes.ContentType')),
                ('position', models.ForeignKey(to='sports.Position', related_name='nfl_player_player_position')),
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
                ('srid_game', models.CharField(max_length=64, help_text='the sportsradar global id for the game')),
                ('srid_player', models.CharField(max_length=64, help_text='the sportsradar global id for the player')),
                ('game_id', models.PositiveIntegerField()),
                ('player_id', models.PositiveIntegerField()),
                ('fantasy_points', models.FloatField(default=0.0)),
                ('pass_td', models.IntegerField(default=0)),
                ('pass_yds', models.IntegerField(default=0)),
                ('pass_int', models.IntegerField(default=0)),
                ('rush_td', models.IntegerField(default=0)),
                ('rush_yds', models.IntegerField(default=0)),
                ('rec_td', models.IntegerField(default=0)),
                ('rec_yds', models.IntegerField(default=0)),
                ('rec_rec', models.IntegerField(default=0)),
                ('off_fum_lost', models.IntegerField(default=0)),
                ('off_fum_rec_td', models.IntegerField(default=0)),
                ('two_pt_conv', models.IntegerField(default=0)),
                ('sack', models.IntegerField(default=0)),
                ('ints', models.IntegerField(default=0)),
                ('fum_rec', models.IntegerField(default=0)),
                ('ret_kick_td', models.IntegerField(default=0)),
                ('ret_punt_td', models.IntegerField(default=0)),
                ('ret_int_td', models.IntegerField(default=0)),
                ('ret_fum_td', models.IntegerField(default=0)),
                ('ret_blk_punt_td', models.IntegerField(default=0)),
                ('ret_fg_td', models.IntegerField(default=0)),
                ('ret_blk_fg_td', models.IntegerField(default=0)),
                ('sfty', models.IntegerField(default=0)),
                ('blk_kick', models.IntegerField(default=0)),
                ('int_td_against', models.IntegerField(default=0)),
                ('fum_td_against', models.IntegerField(default=0)),
                ('off_pass_sfty', models.IntegerField(default=0)),
                ('off_rush_sfty', models.IntegerField(default=0)),
                ('off_punt_sfty', models.IntegerField(default=0)),
                ('game_type', models.ForeignKey(to='contenttypes.ContentType', related_name='nfl_playerstats_sport_game')),
                ('player_type', models.ForeignKey(to='contenttypes.ContentType', related_name='nfl_playerstats_sport_player')),
                ('position', models.ForeignKey(to='sports.Position', related_name='nfl_playerstats_playerstats_position')),
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
                ('srid', models.CharField(max_length=64, unique=True, help_text='the sportsradar global id')),
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
            field=models.ForeignKey(to='nfl.Team'),
        ),
        migrations.AddField(
            model_name='game',
            name='away',
            field=models.ForeignKey(to='nfl.Team', related_name='game_awayteam'),
        ),
        migrations.AddField(
            model_name='game',
            name='home',
            field=models.ForeignKey(to='nfl.Team', related_name='game_hometeam'),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
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
                ('tsxcontent', models.ForeignKey(to='sports.TsxContent', related_name='nfl_tsxinjury_tsxcontent')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TsxNews',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
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
                ('tsxcontent', models.ForeignKey(to='sports.TsxContent', related_name='nfl_tsxnews_tsxcontent')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TsxPlayer',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('sportsdataid', models.CharField(max_length=64)),
                ('sportradarid', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=128)),
                ('tsxitem_id', models.PositiveIntegerField()),
                ('tsxitem_type', models.ForeignKey(to='contenttypes.ContentType', related_name='nfl_tsxplayer_tsxitem_tsxitemref')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TsxTeam',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('sportsdataid', models.CharField(max_length=64)),
                ('sportradarid', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=128)),
                ('tsxitem_id', models.PositiveIntegerField()),
                ('tsxitem_type', models.ForeignKey(to='contenttypes.ContentType', related_name='nfl_tsxteam_tsxitem_tsxitemref')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TsxTransaction',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
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
                ('tsxcontent', models.ForeignKey(to='sports.TsxContent', related_name='nfl_tsxtransaction_tsxcontent')),
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
            field=models.ForeignKey(default=None, to='nfl.Player'),
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
            field=models.ForeignKey(default=None, to='nfl.Team'),
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
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 19, 2, 26, 4, 328274, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gameboxscore',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 19, 2, 26, 5, 335073, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='playerstats',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 19, 2, 26, 6, 408614, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
