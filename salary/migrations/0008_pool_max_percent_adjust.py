# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0007_salary_amount_unadjusted'),
    ]

    operations = [
        migrations.AddField(
            model_name='pool',
            name='max_percent_adjust',
            field=models.FloatField(default=10.0, help_text='the maximum percentage shift due to ownership adjustment'),
        ),
    ]
