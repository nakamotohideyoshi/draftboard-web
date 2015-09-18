# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test', '0009_gamechild_prev_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balancechild',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=9),
        ),
        migrations.AlterField(
            model_name='transactiondetailchild',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=9),
        ),
    ]
