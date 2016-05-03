# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0005_auto_20160503_1415'),
    ]

    operations = [
        migrations.AddField(
            model_name='salary',
            name='ownership_percentage',
            field=models.FloatField(null=True, default=10.0),
        ),
    ]
