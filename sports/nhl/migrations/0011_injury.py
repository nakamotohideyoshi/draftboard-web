# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('nhl', '0010_auto_20150527_0156'),
    ]

    operations = [
        migrations.CreateModel(
            name='Injury',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('player_id', models.PositiveIntegerField()),
                ('status', models.CharField(max_length=32, default='')),
                ('description', models.CharField(max_length=1024, default='')),
                ('srid', models.CharField(max_length=64, default='')),
                ('player_type', models.ForeignKey(to='contenttypes.ContentType', related_name='nhl_injury_injured_player')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
