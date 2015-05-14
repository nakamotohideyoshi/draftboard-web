# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mlb', '0015_auto_20150513_2341'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerstatspitcher',
            name='r_total',
            field=models.IntegerField(default=0),
        ),
    ]
