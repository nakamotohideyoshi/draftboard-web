# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mlb', '0014_auto_20150513_2307'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerstatshitter',
            name='play',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='playerstatshitter',
            name='start',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='playerstatspitcher',
            name='play',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='playerstatspitcher',
            name='start',
            field=models.BooleanField(default=False),
        ),
    ]
