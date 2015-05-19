# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nhl', '0002_auto_20150518_2133'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerstats',
            name='assist',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='blk',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='ga',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='goal',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='l',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='otl',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='pp_goal',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='save',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='sh_goal',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='shutout',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='so_goal',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='sog',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='w',
            field=models.BooleanField(default=False),
        ),
    ]
