# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('nfl', '0003_auto_20150527_0156'),
    ]

    operations = [
        migrations.CreateModel(
            name='Injury',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('iid', models.CharField(max_length=64, unique=True, help_text='custom injury id')),
                ('player_id', models.PositiveIntegerField()),
                ('status', models.CharField(max_length=32, default='')),
                ('description', models.CharField(max_length=1024, default='')),
                ('player_type', models.ForeignKey(related_name='nfl_injury_injured_player', to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
