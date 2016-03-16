# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test', '0015_auto_20160302_1624'),
    ]

    operations = [
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('srid', models.CharField(help_text='the sportsradar global id of the season/schedule', max_length=64)),
                ('season_year', models.IntegerField(default=0, help_text='the year the season started')),
                ('season_type', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='gamechild',
            name='season',
            field=models.ForeignKey(null=True, to='test.Season'),
        ),
    ]
