# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fpp', '0004_auto_20150731_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fppbalance',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=9),
        ),
        migrations.AlterField(
            model_name='fpptransactiondetail',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=9),
        ),
    ]
