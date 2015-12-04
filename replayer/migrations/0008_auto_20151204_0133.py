# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('replayer', '0007_auto_20151204_0118'),
    ]

    operations = [
        migrations.AddField(
            model_name='timemachine',
            name='target',
            field=models.DateTimeField(blank=True, help_text='the time you want to start at in the replay. must be within the start and end of the recorded stats', null=True),
        ),
        migrations.AlterField(
            model_name='timemachine',
            name='current',
            field=models.DateTimeField(blank=True, help_text='where the replay is currently', null=True),
        ),
        migrations.AlterField(
            model_name='timemachine',
            name='playback_mode',
            field=models.CharField(max_length=64, choices=[('play-all', 'Play All'), ('play-to-target', 'Play to Target')]),
        ),
    ]
