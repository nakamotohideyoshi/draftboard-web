# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0005_auto_20160302_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerstats',
            name='minutes',
            field=models.FloatField(default=0.0),
        ),
    ]
