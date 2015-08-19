# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test', '0008_auto_20150731_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamechild',
            name='prev_status',
            field=models.CharField(max_length=32, default=''),
        ),
    ]
