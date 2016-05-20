# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0008_pool_max_percent_adjust'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salary',
            name='fppg',
            field=models.FloatField(default=0.0, verbose_name='FPPG'),
        ),
    ]
