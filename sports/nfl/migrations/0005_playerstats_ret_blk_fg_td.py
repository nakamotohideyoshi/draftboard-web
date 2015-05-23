# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nfl', '0004_gameboxscore'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerstats',
            name='ret_blk_fg_td',
            field=models.IntegerField(default=0),
        ),
    ]
