# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bonuscash', '0005_auto_20150918_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bonuscashbalance',
            name='amount',
            field=models.DecimalField(max_digits=11, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='bonuscashtransactiondetail',
            name='amount',
            field=models.DecimalField(max_digits=11, decimal_places=2),
        ),
    ]
