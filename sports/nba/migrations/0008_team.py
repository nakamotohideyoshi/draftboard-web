# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0007_auto_20150513_0105'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid', models.CharField(help_text='the sportsradar global id', unique=True, max_length=64)),
                ('srid_venue', models.CharField(help_text='the sportsradar global id', unique=True, max_length=64)),
                ('name', models.CharField(help_text='the team name, without the market/city. ie: "Lakers", or "Eagles"', default='', max_length=64)),
                ('alias', models.CharField(help_text='the abbreviation for the team, ie: for Boston Celtic alias == "BOS"', default='', max_length=64)),
                ('srid_league', models.CharField(help_text='league sportsradar id', max_length=64)),
                ('srid_conference', models.CharField(help_text='conference sportsradar id', max_length=64)),
                ('srid_division', models.CharField(help_text='division sportsradar id', max_length=64)),
                ('market', models.CharField(max_length=64)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
