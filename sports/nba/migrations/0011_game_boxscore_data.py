# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-11 22:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0010_playerstats_fp_change'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='boxscore_data',
            field=models.CharField(max_length=8192, null=True),
        ),
    ]
