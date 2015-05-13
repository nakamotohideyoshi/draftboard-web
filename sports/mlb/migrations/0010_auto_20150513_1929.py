# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mlb', '0009_auto_20150513_0424'),
    ]

    operations = [
        migrations.DeleteModel(
            name='GameBoxscore',
        ),
        migrations.DeleteModel(
            name='Injury',
        ),
        migrations.DeleteModel(
            name='PlayerStatsSeason',
        ),
        migrations.DeleteModel(
            name='RosterPlayer',
        ),
        migrations.DeleteModel(
            name='Venue',
        ),
        migrations.AddField(
            model_name='team',
            name='market',
            field=models.CharField(max_length=64, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='team',
            name='srid_division',
            field=models.CharField(help_text='division sportsradar id', max_length=64, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='team',
            name='srid_league',
            field=models.CharField(help_text='league sportsradar id', max_length=64, default=''),
            preserve_default=False,
        ),
    ]
