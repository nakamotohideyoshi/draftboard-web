# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('nba', '0005_auto_20150523_0155'),
    ]

    operations = [
        migrations.CreateModel(
            name='Injury',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('player_id', models.PositiveIntegerField()),
                ('status', models.CharField(max_length=32, default='')),
                ('description', models.CharField(max_length=1024, default='')),
                ('srid', models.CharField(max_length=64, default='')),
                ('player_type', models.ForeignKey(to='contenttypes.ContentType', related_name='nba_injury_injured_player')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='player',
            name='injury_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='injury_type',
            field=models.ForeignKey(to='contenttypes.ContentType', null=True, related_name='nba_player_players_injury'),
        ),
    ]
