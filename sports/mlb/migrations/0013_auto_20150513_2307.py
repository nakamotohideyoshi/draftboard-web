# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mlb', '0012_auto_20150513_2011'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerStatsHitter',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid_game', models.CharField(max_length=64, help_text='the sportsradar global id for the game')),
                ('srid_player', models.CharField(max_length=64, help_text='the sportsradar global id for the player')),
                ('bb', models.IntegerField(default=0)),
                ('s', models.IntegerField(default=0)),
                ('d', models.IntegerField(default=0)),
                ('t', models.IntegerField(default=0)),
                ('hr', models.IntegerField(default=0)),
                ('rbi', models.IntegerField(default=0)),
                ('r', models.IntegerField(default=0)),
                ('hbp', models.IntegerField(default=0)),
                ('sb', models.IntegerField(default=0)),
                ('cs', models.IntegerField(default=0)),
                ('ktotal', models.IntegerField(default=0)),
                ('ab', models.IntegerField(default=0)),
                ('ap', models.IntegerField(default=0)),
                ('lob', models.IntegerField(default=0)),
                ('xbh', models.IntegerField(default=0)),
                ('game', models.ForeignKey(to='mlb.Game')),
                ('player', models.ForeignKey(to='mlb.Player')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PlayerStatsPitcher',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid_game', models.CharField(max_length=64, help_text='the sportsradar global id for the game')),
                ('srid_player', models.CharField(max_length=64, help_text='the sportsradar global id for the player')),
                ('ip_1', models.FloatField(default=0.0)),
                ('ip_2', models.FloatField(default=0.0)),
                ('ktotal', models.IntegerField(default=0)),
                ('win', models.BooleanField(default=False)),
                ('loss', models.BooleanField(default=False)),
                ('qstart', models.BooleanField(default=False)),
                ('er', models.IntegerField(default=0)),
                ('h', models.IntegerField(default=0)),
                ('bb', models.IntegerField(default=0)),
                ('hbp', models.IntegerField(default=0)),
                ('cg', models.BooleanField(default=False)),
                ('cgso', models.BooleanField(default=False)),
                ('nono', models.BooleanField(default=False)),
                ('game', models.ForeignKey(to='mlb.Game')),
                ('player', models.ForeignKey(to='mlb.Player')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='PlayerStats',
        ),
    ]
