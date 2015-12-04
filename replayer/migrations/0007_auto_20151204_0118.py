# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('replayer', '0006_auto_20151201_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timemachine',
            name='playback_mode',
            field=models.CharField(max_length=64, choices=[('play-all', 'Play All'), ('play-to-current', 'Play to Current')]),
        ),
    ]
