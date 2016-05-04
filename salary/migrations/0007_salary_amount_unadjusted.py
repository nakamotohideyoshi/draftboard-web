# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0006_salary_ownership_percentage'),
    ]

    operations = [
        migrations.AddField(
            model_name='salary',
            name='amount_unadjusted',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
