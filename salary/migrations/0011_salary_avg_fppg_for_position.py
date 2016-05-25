# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0010_auto_20160525_1719'),
    ]

    operations = [
        migrations.AddField(
            model_name='salary',
            name='avg_fppg_for_position',
            field=models.FloatField(default=0.0, verbose_name='AVG Positional FPPG'),
        ),
    ]
