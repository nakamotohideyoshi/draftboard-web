# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0004_auto_20160209_2241'),
    ]

    operations = [
        migrations.AddField(
            model_name='pool',
            name='high_cutoff_increment',
            field=models.FloatField(null=True, default=1.0),
        ),
        migrations.AddField(
            model_name='pool',
            name='low_cutoff_increment',
            field=models.FloatField(null=True, default=1.0),
        ),
        migrations.AddField(
            model_name='pool',
            name='ownership_threshold_high_cutoff',
            field=models.FloatField(null=True, default=30.0),
        ),
        migrations.AddField(
            model_name='pool',
            name='ownership_threshold_low_cutoff',
            field=models.FloatField(null=True, default=10.0),
        ),
    ]
