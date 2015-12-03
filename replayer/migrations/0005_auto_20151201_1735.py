# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('replayer', '0004_auto_20151201_0035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timemachine',
            name='current',
            field=models.DateTimeField(null=True, help_text='the time you want to start at in the replay. must be within the start and end of the recorded stats', blank=True),
        ),
        migrations.AlterField(
            model_name='timemachine',
            name='loading_status',
            field=models.CharField(max_length=255, default='', choices=[('todo-status', 'TODO-LOADING-STATUS')], help_text='status of replay. initial -> loading -> playing'),
        ),
        migrations.AlterField(
            model_name='timemachine',
            name='playback_status',
            field=models.CharField(max_length=255, default='', choices=[('todo-status', 'TODO-PLAYBACK-STATUS')], help_text='status of replay. initial -> loading -> playing'),
        ),
    ]
