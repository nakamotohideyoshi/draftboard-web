# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0002_auto_20150624_1538'),
    ]

    operations = [
        migrations.AddField(
            model_name='pool',
            name='generate_salary_task_id',
            field=models.CharField(max_length=255, null=True, default=None, verbose_name='Generating Salary'),
        ),
    ]
