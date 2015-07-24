# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('roster', '0002_auto_20150529_0216'),
        ('lineup', '0003_lineup_draftgroup'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('player_id', models.PositiveIntegerField()),
                ('idx', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='lineup',
            name='draftgroup',
            field=models.ForeignKey(to='draftgroup.DraftGroup'),
        ),
        migrations.AddField(
            model_name='player',
            name='lineup',
            field=models.ForeignKey(to='lineup.Lineup'),
        ),
        migrations.AddField(
            model_name='player',
            name='player_type',
            field=models.ForeignKey(to='contenttypes.ContentType', related_name='lineup_player_player'),
        ),
        migrations.AddField(
            model_name='player',
            name='roster_spot',
            field=models.ForeignKey(to='roster.RosterSpot'),
        ),
    ]
