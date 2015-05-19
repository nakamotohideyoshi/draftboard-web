# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nhl', '0004_auto_20150519_0015'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameBoxscore',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid_game', models.CharField(max_length=64, unique=True, default=None, help_text='the sportsradar global id for the game')),
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
                ('away', models.ForeignKey(related_name='gameboxscore_away', to='nhl.Team')),
                ('home', models.ForeignKey(related_name='gameboxscore_home', to='nhl.Team')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
