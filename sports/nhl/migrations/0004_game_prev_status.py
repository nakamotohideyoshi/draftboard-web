# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nhl', '0003_auto_20150625_0016'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='prev_status',
            field=models.CharField(max_length=32, default=''),
        ),
    ]
