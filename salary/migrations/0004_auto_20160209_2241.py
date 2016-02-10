# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0003_pool_generate_salary_task_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='salaryconfig',
            options={'verbose_name': 'Algorithm'},
        ),
        migrations.AlterField(
            model_name='salary',
            name='fppg',
            field=models.FloatField(verbose_name='Weighted FPPG', default=0.0),
        ),
    ]
