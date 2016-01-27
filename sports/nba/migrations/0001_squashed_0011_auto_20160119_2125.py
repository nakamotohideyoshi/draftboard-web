# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    replaces = [('nba', '0001_initial'), ('nba', '0002_auto_20150528_2321'), ('nba', '0003_auto_20150625_0016'), ('nba', '0004_game_prev_status'), ('nba', '0005_auto_20151016_1942'), ('nba', '0006_tsxinjury_tsxnews_tsxplayer_tsxteam_tsxtransaction'), ('nba', '0007_injury_ddtimestamp'), ('nba', '0008_auto_20160110_2112'), ('nba', '0009_auto_20160110_2242'), ('nba', '0010_player_season_fppg'), ('nba', '0011_auto_20160119_2125')]

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('sports', '0001_squashed_0008_auto_20160119_2124'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid', models.CharField(help_text='the sportsradar global id', max_length=64, unique=True)),
                ('start', models.DateTimeField()),
                ('status', models.CharField(max_length=32)),
                ('srid_home', models.CharField(help_text='home team sportsradar global id', max_length=64)),
                ('srid_away', models.CharField(help_text='away team sportsradar global id', max_length=64)),
                ('title', models.CharField(max_length=128, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GameBoxscore',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid_game', models.CharField(help_text='the sportsradar global id for the game', max_length=64, default=None, unique=True)),
                ('srid_home', models.CharField(max_length=64)),
                ('srid_away', models.CharField(max_length=64)),
                ('home_id', models.PositiveIntegerField()),
                ('away_id', models.PositiveIntegerField()),
                ('attendance', models.IntegerField(default=0)),
                ('coverage', models.CharField(max_length=16, default='')),
                ('status', models.CharField(max_length=64, default='')),
                ('home_score', models.IntegerField(default=0)),
                ('away_score', models.IntegerField(default=0)),
                ('title', models.CharField(max_length=256, default='')),
                ('home_scoring_json', models.CharField(max_length=2048, default='')),
                ('away_scoring_json', models.CharField(max_length=2048, default='')),
                ('clock', models.CharField(max_length=16, default='')),
                ('duration', models.CharField(max_length=16, default='')),
                ('lead_changes', models.IntegerField(default=0)),
                ('quarter', models.CharField(max_length=16, default='')),
                ('times_tied', models.IntegerField(default=0)),
                ('away_type', models.ForeignKey(to='contenttypes.ContentType', related_name='nba_gameboxscore_away_team')),
                ('home_type', models.ForeignKey(to='contenttypes.ContentType', related_name='nba_gameboxscore_home_team')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GamePortion',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid_game', models.CharField(help_text='the sportsradar global id for the game this is associate with', max_length=64)),
                ('game_id', models.PositiveIntegerField()),
                ('category', models.CharField(help_text='typically one of these: ["inning-half","quarter","period"]', max_length=32, default='')),
                ('sequence', models.IntegerField(help_text='an ordering of all GamePortions with the same srid_game', default=0)),
                ('srid', models.CharField(max_length=64, default='')),
                ('game_type', models.ForeignKey(to='contenttypes.ContentType', related_name='nba_gameportion_sport_game')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Injury',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('iid', models.CharField(help_text='custom injury id', max_length=128, unique=True)),
                ('player_id', models.PositiveIntegerField()),
                ('status', models.CharField(max_length=32, default='')),
                ('description', models.CharField(max_length=1024, default='')),
                ('srid', models.CharField(max_length=64, default='')),
                ('comment', models.CharField(max_length=1024, default='')),
                ('player_type', models.ForeignKey(to='contenttypes.ContentType', related_name='nba_injury_injured_player')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pbp',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid_game', models.CharField(help_text='the sportsradar global id for the game', max_length=64)),
                ('game_id', models.PositiveIntegerField()),
                ('game_type', models.ForeignKey(to='contenttypes.ContentType', related_name='nba_pbp_sport_game')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PbpDescription',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('pbp_id', models.PositiveIntegerField()),
                ('portion_id', models.PositiveIntegerField()),
                ('idx', models.IntegerField(default=0)),
                ('description', models.CharField(max_length=1024, default='')),
                ('srid', models.CharField(max_length=64, default='')),
                ('pbp_type', models.ForeignKey(to='contenttypes.ContentType', related_name='nba_pbpdescription_pbpdesc_pbp')),
                ('portion_type', models.ForeignKey(to='contenttypes.ContentType', related_name='nba_pbpdescription_pbpdesc_portion')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid', models.CharField(help_text='the sportsradar global id', max_length=64, unique=True)),
                ('first_name', models.CharField(max_length=32)),
                ('last_name', models.CharField(max_length=32)),
                ('injury_id', models.PositiveIntegerField(null=True)),
                ('srid_team', models.CharField(max_length=64, default='')),
                ('birth_place', models.CharField(max_length=64, default='')),
                ('birthdate', models.CharField(max_length=64, default='')),
                ('college', models.CharField(max_length=64, default='')),
                ('experience', models.FloatField(default=0.0)),
                ('height', models.FloatField(help_text='inches', default=0.0)),
                ('weight', models.FloatField(help_text='lbs', default=0.0)),
                ('jersey_number', models.CharField(max_length=64, default='')),
                ('status', models.CharField(help_text='roster status - ie: "ACT" means they are ON the roster. Not particularly active as in not-injured!', max_length=64, default='')),
                ('draft_pick', models.CharField(max_length=64, default='')),
                ('draft_round', models.CharField(max_length=64, default='')),
                ('draft_year', models.CharField(max_length=64, default='')),
                ('srid_draft_team', models.CharField(max_length=64, default='')),
                ('injury_type', models.ForeignKey(to='contenttypes.ContentType', related_name='nba_player_players_injury', null=True)),
                ('position', models.ForeignKey(to='sports.Position', related_name='nba_player_player_position')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PlayerStats',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid_game', models.CharField(help_text='the sportsradar global id for the game', max_length=64)),
                ('srid_player', models.CharField(help_text='the sportsradar global id for the player', max_length=64)),
                ('game_id', models.PositiveIntegerField()),
                ('player_id', models.PositiveIntegerField()),
                ('fantasy_points', models.FloatField(default=0.0)),
                ('defensive_rebounds', models.FloatField(default=0.0)),
                ('two_points_pct', models.FloatField(default=0.0)),
                ('assists', models.FloatField(default=0.0)),
                ('free_throws_att', models.FloatField(default=0.0)),
                ('flagrant_fouls', models.FloatField(default=0.0)),
                ('offensive_rebounds', models.FloatField(default=0.0)),
                ('personal_fouls', models.FloatField(default=0.0)),
                ('field_goals_att', models.FloatField(default=0.0)),
                ('three_points_att', models.FloatField(default=0.0)),
                ('field_goals_pct', models.FloatField(default=0.0)),
                ('turnovers', models.FloatField(default=0.0)),
                ('points', models.FloatField(default=0.0)),
                ('rebounds', models.FloatField(default=0.0)),
                ('two_points_att', models.FloatField(default=0.0)),
                ('field_goals_made', models.FloatField(default=0.0)),
                ('blocked_att', models.FloatField(default=0.0)),
                ('free_throws_made', models.FloatField(default=0.0)),
                ('blocks', models.FloatField(default=0.0)),
                ('assists_turnover_ratio', models.FloatField(default=0.0)),
                ('tech_fouls', models.FloatField(default=0.0)),
                ('three_points_made', models.FloatField(default=0.0)),
                ('steals', models.FloatField(default=0.0)),
                ('two_points_made', models.FloatField(default=0.0)),
                ('free_throws_pct', models.FloatField(default=0.0)),
                ('three_points_pct', models.FloatField(default=0.0)),
                ('game_type', models.ForeignKey(to='contenttypes.ContentType', related_name='nba_playerstats_sport_game')),
                ('player_type', models.ForeignKey(to='contenttypes.ContentType', related_name='nba_playerstats_sport_player')),
                ('position', models.ForeignKey(to='sports.Position', related_name='nba_playerstats_playerstats_position')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
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
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid', models.CharField(help_text='the sportsradar global id', max_length=64, unique=True)),
                ('srid_venue', models.CharField(help_text='the sportsradar global id', max_length=64)),
                ('name', models.CharField(help_text='the team name, without the market/city. ie: "Lakers", or "Eagles"', max_length=64, default='')),
                ('alias', models.CharField(help_text='the abbreviation for the team, ie: for Boston Celtic alias == "BOS"', max_length=64, default='')),
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
            field=models.ForeignKey(to='nba.Team'),
        ),
        migrations.AddField(
            model_name='game',
            name='away',
            field=models.ForeignKey(to='nba.Team', related_name='game_awayteam'),
        ),
        migrations.AddField(
            model_name='game',
            name='home',
            field=models.ForeignKey(to='nba.Team', related_name='game_hometeam'),
        ),
        migrations.AlterField(
            model_name='gameboxscore',
            name='coverage',
            field=models.CharField(max_length=64, default=''),
        ),
        migrations.AddField(
            model_name='game',
            name='prev_status',
            field=models.CharField(max_length=32, default=''),
        ),
        migrations.AlterField(
            model_name='pbpdescription',
            name='srid',
            field=models.CharField(max_length=64, default='', unique=True),
        ),
        migrations.CreateModel(
            name='TsxInjury',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('srid', models.CharField(help_text='the sportradar global id for the item', max_length=64)),
                ('pcid', models.CharField(help_text='the providers content id for this item', max_length=64)),
                ('content_created', models.DateTimeField()),
                ('content_modified', models.DateTimeField()),
                ('content_published', models.DateTimeField()),
                ('title', models.CharField(max_length=256)),
                ('byline', models.CharField(max_length=256)),
                ('dateline', models.CharField(max_length=32)),
                ('credit', models.CharField(max_length=128)),
                ('content', models.CharField(max_length=8192)),
                ('tsxcontent', models.ForeignKey(to='sports.TsxContent', related_name='nba_tsxinjury_tsxcontent')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TsxNews',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('srid', models.CharField(help_text='the sportradar global id for the item', max_length=64)),
                ('pcid', models.CharField(help_text='the providers content id for this item', max_length=64)),
                ('content_created', models.DateTimeField()),
                ('content_modified', models.DateTimeField()),
                ('content_published', models.DateTimeField()),
                ('title', models.CharField(max_length=256)),
                ('byline', models.CharField(max_length=256)),
                ('dateline', models.CharField(max_length=32)),
                ('credit', models.CharField(max_length=128)),
                ('content', models.CharField(max_length=8192)),
                ('tsxcontent', models.ForeignKey(to='sports.TsxContent', related_name='nba_tsxnews_tsxcontent')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TsxPlayer',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('sportsdataid', models.CharField(max_length=64)),
                ('sportradarid', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=128)),
                ('tsxitem_id', models.PositiveIntegerField()),
                ('tsxitem_type', models.ForeignKey(to='contenttypes.ContentType', related_name='nba_tsxplayer_tsxitem_tsxitemref')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TsxTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('sportsdataid', models.CharField(max_length=64)),
                ('sportradarid', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=128)),
                ('tsxitem_id', models.PositiveIntegerField()),
                ('tsxitem_type', models.ForeignKey(to='contenttypes.ContentType', related_name='nba_tsxteam_tsxitem_tsxitemref')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TsxTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('srid', models.CharField(help_text='the sportradar global id for the item', max_length=64)),
                ('pcid', models.CharField(help_text='the providers content id for this item', max_length=64)),
                ('content_created', models.DateTimeField()),
                ('content_modified', models.DateTimeField()),
                ('content_published', models.DateTimeField()),
                ('title', models.CharField(max_length=256)),
                ('byline', models.CharField(max_length=256)),
                ('dateline', models.CharField(max_length=32)),
                ('credit', models.CharField(max_length=128)),
                ('content', models.CharField(max_length=8192)),
                ('tsxcontent', models.ForeignKey(to='sports.TsxContent', related_name='nba_tsxtransaction_tsxcontent')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='injury',
            name='ddtimestamp',
            field=models.BigIntegerField(help_text='the time this injury update was parsed by dataden.this will be the same value for all objects that were in the feed on the last parse.', default=0),
        ),
        migrations.AddField(
            model_name='tsxplayer',
            name='content_published',
            field=models.DateTimeField(help_text='the item ref is a GFK so also store the publish date here for ordering purposes.', default=datetime.datetime(1999, 1, 1, 12, 0, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='tsxplayer',
            name='player',
            field=models.ForeignKey(default=None, to='nba.Player'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tsxteam',
            name='content_published',
            field=models.DateTimeField(help_text='the item ref is a GFK so also store the publish date here for ordering purposes.', default=datetime.datetime(1999, 1, 1, 12, 0, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='tsxteam',
            name='team',
            field=models.ForeignKey(default=None, to='nba.Team'),
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
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 1, 19, 2, 25, 3, 615679, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gameboxscore',
            name='updated',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 1, 19, 2, 25, 5, 183133, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='playerstats',
            name='updated',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 1, 19, 2, 25, 6, 311945, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
