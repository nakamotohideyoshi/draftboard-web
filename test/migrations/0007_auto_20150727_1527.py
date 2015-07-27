# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test', '0006_auto_20150701_1916'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='balancechild',
            name='transaction_id',
        ),
        migrations.RemoveField(
            model_name='balancechild',
            name='transaction_type',
        ),
    ]
