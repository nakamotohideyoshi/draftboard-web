# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0006_auto_20150527_0156'),
    ]

    operations = [
        migrations.AddField(
            model_name='injury',
            name='comment',
            field=models.CharField(max_length=1024, default=''),
        ),
    ]
