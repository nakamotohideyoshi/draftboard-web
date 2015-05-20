# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('test', '0002_auto_20150408_0208'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameChild',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid', models.CharField(max_length=64, unique=True, help_text='the sportsradar global id')),
                ('start', models.DateTimeField()),
                ('status', models.CharField(max_length=32)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PlayerChild',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid', models.CharField(max_length=64, unique=True, help_text='the sportsradar global id')),
                ('first_name', models.CharField(max_length=32)),
                ('last_name', models.CharField(max_length=32)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PlayerStatsChild',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid_game', models.CharField(max_length=64, help_text='the sportsradar global id for the game')),
                ('srid_player', models.CharField(max_length=64, help_text='the sportsradar global id for the player')),
                ('game_id', models.PositiveIntegerField()),
                ('player_id', models.PositiveIntegerField()),
                ('fantasy_points', models.FloatField(default=0.0)),
                ('position', models.CharField(max_length=16, default='')),
                ('primary_position', models.CharField(max_length=16, default='')),
                ('game_type', models.ForeignKey(to='contenttypes.ContentType', related_name='test_playerstatschild_sport_game')),
                ('player_type', models.ForeignKey(to='contenttypes.ContentType', related_name='test_playerstatschild_sport_player')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='playerstatschild',
            unique_together=set([('srid_player', 'srid_game')]),
        ),
    ]
