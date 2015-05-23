# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('nhl', '0003_auto_20150520_2017'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pbp',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid_game', models.CharField(max_length=64, help_text='the sportsradar global id for the game')),
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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('pbp_id', models.PositiveIntegerField()),
                ('idx', models.IntegerField(default=0)),
                ('description', models.CharField(max_length=1024, default='')),
                ('pbp_type', models.ForeignKey(related_name='nhl_pbpdescription_sport_game', to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
