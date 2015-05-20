# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nfl', '0002_auto_20150520_0352'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerstats',
            name='fum_td_against',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='int_td_against',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='off_pass_sfty',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='off_punt_sfty',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='off_rush_sfty',
            field=models.IntegerField(default=0),
        ),
    ]
