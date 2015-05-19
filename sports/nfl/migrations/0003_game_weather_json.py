# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nfl', '0002_auto_20150518_2200'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='weather_json',
            field=models.CharField(default=None, max_length=512),
            preserve_default=False,
        ),
    ]
