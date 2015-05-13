# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mlb', '0006_auto_20150512_2354'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='alias',
            field=models.CharField(help_text='the abbreviation for the team, ie: for Boston Celtic alias == "BOS"', default='', max_length=64),
        ),
        migrations.AddField(
            model_name='team',
            name='name',
            field=models.CharField(help_text='the team name, without the market/city. ie: "Lakers", or "Eagles"', default='', max_length=64),
        ),
        migrations.AddField(
            model_name='team',
            name='srid_venue',
            field=models.CharField(help_text='the sportsradar global id', unique=True, default='', max_length=64),
            preserve_default=False,
        ),
    ]
