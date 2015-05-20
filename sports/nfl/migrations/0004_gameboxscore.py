# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('nfl', '0003_auto_20150520_1852'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameBoxscore',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid_game', models.CharField(help_text='the sportsradar global id for the game', default=None, max_length=64, unique=True)),
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
    ]
