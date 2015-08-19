# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fpp', '0002_auto_20150428_0122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fppbalance',
            name='transaction_id',
        ),
        migrations.RemoveField(
            model_name='fppbalance',
            name='transaction_type',
        ),
    ]
