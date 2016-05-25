# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mlb', '0009_player_on_active_roster'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProbablePitcher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('srid_game', models.CharField(max_length=64)),
                ('srid_player', models.CharField(max_length=64)),
            ],
        ),
    ]
