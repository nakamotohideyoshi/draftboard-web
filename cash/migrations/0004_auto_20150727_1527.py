# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cash', '0003_cashamount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cashbalance',
            name='transaction_id',
        ),
        migrations.RemoveField(
            model_name='cashbalance',
            name='transaction_type',
        ),
    ]
