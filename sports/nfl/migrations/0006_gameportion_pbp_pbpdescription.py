# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('nfl', '0005_playerstats_ret_blk_fg_td'),
    ]

    operations = [
        migrations.CreateModel(
            name='GamePortion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid_game', models.CharField(help_text='the sportsradar global id for the game this is associate with', max_length=64)),
                ('game_id', models.PositiveIntegerField()),
                ('category', models.CharField(help_text='typically one of these: ["inning-half","quarter","period"]', default='', max_length=32)),
                ('sequence', models.IntegerField(help_text='an ordering of all GamePortions with the same srid_game', default=0)),
                ('game_type', models.ForeignKey(related_name='nfl_gameportion_sport_game', to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pbp',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid_game', models.CharField(help_text='the sportsradar global id for the game', max_length=64)),
                ('game_id', models.PositiveIntegerField()),
                ('game_type', models.ForeignKey(related_name='nfl_pbp_sport_game', to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PbpDescription',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('pbp_id', models.PositiveIntegerField()),
                ('portion_id', models.PositiveIntegerField()),
                ('idx', models.IntegerField(default=0)),
                ('description', models.CharField(default='', max_length=1024)),
                ('pbp_type', models.ForeignKey(related_name='nfl_pbpdescription_pbpdesc_pbp', to='contenttypes.ContentType')),
                ('portion_type', models.ForeignKey(related_name='nfl_pbpdescription_pbpdesc_portion', to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
