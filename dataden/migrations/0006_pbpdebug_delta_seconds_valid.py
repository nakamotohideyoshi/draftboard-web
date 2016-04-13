# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataden', '0005_pbpdebug_timestamp_pushered'),
    ]

    operations = [
        migrations.AddField(
            model_name='pbpdebug',
            name='delta_seconds_valid',
            field=models.BooleanField(default=False),
        ),
    ]
