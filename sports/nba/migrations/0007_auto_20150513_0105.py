# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0006_auto_20150512_2340'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerstats',
            name='game',
            field=models.ForeignKey(default=None, to='nba.Game'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='playerstats',
            name='player',
            field=models.ForeignKey(default=None, to='nba.Player'),
            preserve_default=False,
        ),
    ]
