# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0002_auto_20150427_0306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketamount',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, unique=True),
        ),
    ]
