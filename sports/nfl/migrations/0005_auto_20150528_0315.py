# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nfl', '0004_injury'),
    ]

    operations = [
        migrations.AddField(
            model_name='injury',
            name='practice_status',
            field=models.CharField(default='', max_length=1024),
        ),
        migrations.AddField(
            model_name='injury',
            name='srid',
            field=models.CharField(default='', max_length=64),
        ),
    ]
