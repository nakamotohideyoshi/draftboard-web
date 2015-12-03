# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('replayer', '0005_auto_20151201_1735'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timemachine',
            name='loading_status',
        ),
        migrations.RemoveField(
            model_name='timemachine',
            name='playback_status',
        ),
    ]
