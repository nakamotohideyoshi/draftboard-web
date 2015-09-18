# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rakepaid', '0004_playertier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rakepaidbalance',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=9),
        ),
        migrations.AlterField(
            model_name='rakepaidtransactiondetail',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=9),
        ),
    ]
