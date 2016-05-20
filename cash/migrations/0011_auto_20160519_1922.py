# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cash', '0010_auto_20160209_2241'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='optimalpaymentstransaction',
            name='transaction',
        ),
        migrations.DeleteModel(
            name='OptimalPaymentsTransaction',
        ),
    ]
