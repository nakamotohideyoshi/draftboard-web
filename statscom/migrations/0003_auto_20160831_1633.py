# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-31 20:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nfl', '0013_merge'),
        ('statscom', '0002_playerlookup'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playerlookup',
            name='player_id',
        ),
        migrations.RemoveField(
            model_name='playerlookup',
            name='player_type',
        ),
        migrations.AddField(
            model_name='playerlookup',
            name='first_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='playerlookup',
            name='last_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='playerlookup',
            name='player',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='nfl.Player'),
        ),
        migrations.AlterField(
            model_name='playerlookup',
            name='pid',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
