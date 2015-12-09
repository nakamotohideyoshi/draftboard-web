# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('replayer', '0009_auto_20151204_0156'),
    ]

    operations = [
        migrations.AddField(
            model_name='timemachine',
            name='fill_contest_status',
            field=models.CharField(max_length=64, default=None, null=True),
        ),
        migrations.AddField(
            model_name='timemachine',
            name='fill_contests_task_id',
            field=models.CharField(max_length=255, default=None, null=True),
        ),
        migrations.AddField(
            model_name='timemachine',
            name='load_status',
            field=models.CharField(max_length=64, default=None, null=True),
        ),
        migrations.AddField(
            model_name='timemachine',
            name='playback_status',
            field=models.CharField(max_length=64, default=None, null=True),
        ),
    ]
