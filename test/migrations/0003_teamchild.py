# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test', '0002_auto_20150623_2321'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamChild',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid', models.CharField(unique=True, help_text='the sportsradar global id', max_length=64)),
                ('srid_venue', models.CharField(help_text='the sportsradar global id', max_length=64)),
                ('name', models.CharField(default='', help_text='the team name, without the market/city. ie: "Lakers", or "Eagles"', max_length=64)),
                ('alias', models.CharField(default='', help_text='the abbreviation for the team, ie: for Boston Celtic alias == "BOS"', max_length=64)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
