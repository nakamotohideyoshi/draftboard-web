# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mlb', '0003_auto_20160229_1717'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='season',
            name='start_year',
        ),
        migrations.AddField(
            model_name='game',
            name='season',
            field=models.ForeignKey(to='mlb.Season', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='season',
            name='season_year',
            field=models.IntegerField(default=0, help_text='the year the season started'),
        ),
        migrations.AddField(
            model_name='season',
            name='srid',
            field=models.CharField(default=None, help_text='the sportsradar global id of the season/schedule', max_length=64, unique=True),
            preserve_default=False,
        ),
    ]
