# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-07 17:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0013_auto_20161109_1913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameboxscore',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='playerstats',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='tsxplayer',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nba.Player'),
        ),
        migrations.AlterField(
            model_name='tsxteam',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nba.Team'),
        ),
    ]
