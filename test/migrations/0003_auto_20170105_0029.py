# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-05 00:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('test', '0002_auto_20161207_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerchild',
            name='injury_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='playerchild',
            name='injury_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='test_playerchild_players_injury', to='contenttypes.ContentType'),
        ),
    ]
