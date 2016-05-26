# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0009_auto_20160519_1922'),
    ]

    operations = [
        migrations.AddField(
            model_name='salary',
            name='fppg_pos_weighted',
            field=models.FloatField(default=0.0, verbose_name='FPPG Position Weighted'),
        ),
        migrations.AlterField(
            model_name='salary',
            name='fppg',
            field=models.FloatField(default=0.0, verbose_name='FPPG', help_text='simply: (sum of fantasy points for trailing games) / (# of trailing games)'),
        ),
    ]
