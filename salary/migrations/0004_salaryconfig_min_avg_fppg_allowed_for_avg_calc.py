# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0003_auto_20150529_0216'),
    ]

    operations = [
        migrations.AddField(
            model_name='salaryconfig',
            name='min_avg_fppg_allowed_for_avg_calc',
            field=models.FloatField(default=0.0),
        ),
    ]
