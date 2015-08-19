# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bonuscash', '0002_auto_20150428_0437'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bonuscashbalance',
            name='transaction_id',
        ),
        migrations.RemoveField(
            model_name='bonuscashbalance',
            name='transaction_type',
        ),
    ]
