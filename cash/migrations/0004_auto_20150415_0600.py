# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('cash', '0003_admincashwithdrawal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admincashdeposit',
            name='amount',
            field=models.DecimalField(default=0, validators=[django.core.validators.MinValueValidator(0.01)], decimal_places=2, max_digits=20),
        ),
        migrations.AlterField(
            model_name='admincashwithdrawal',
            name='amount',
            field=models.DecimalField(default=0, validators=[django.core.validators.MinValueValidator(0.01)], decimal_places=2, max_digits=20),
        ),
    ]
