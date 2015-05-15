# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0012_auto_20150513_0424'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameBoxscore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid_game', models.CharField(max_length=64, help_text='the sportsradar global id for the game')),
                ('srid_home', models.CharField(max_length=64)),
                ('srid_away', models.CharField(max_length=64)),
                ('attendance', models.IntegerField(default=0)),
                ('clock', models.CharField(max_length=16, default='')),
                ('coverage', models.CharField(max_length=16, default='')),
                ('duration', models.CharField(max_length=16, default='')),
                ('lead_changes', models.IntegerField(default=0)),
                ('quarter', models.CharField(max_length=16, default='')),
                ('status', models.CharField(max_length=64, default='')),
                ('times_tied', models.IntegerField(default=0)),
                ('title', models.CharField(max_length=256, default='')),
                ('home_points', models.IntegerField(default=0)),
                ('away_points', models.IntegerField(default=0)),
                ('away', models.ForeignKey(to='nba.Team', related_name='gameboxscore_away')),
                ('home', models.ForeignKey(to='nba.Team', related_name='gameboxscore_home')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
