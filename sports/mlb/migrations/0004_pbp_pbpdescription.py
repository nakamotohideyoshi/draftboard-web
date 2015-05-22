# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('mlb', '0003_auto_20150520_2017'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pbp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('game_id', models.PositiveIntegerField()),
                ('game_type', models.ForeignKey(to='contenttypes.ContentType', related_name='mlb_pbp_sport_game')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PbpDescription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('pbp_id', models.PositiveIntegerField()),
                ('description', models.CharField(max_length=1024, default='')),
                ('pbp_type', models.ForeignKey(to='contenttypes.ContentType', related_name='mlb_pbpdescription_sport_game')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
