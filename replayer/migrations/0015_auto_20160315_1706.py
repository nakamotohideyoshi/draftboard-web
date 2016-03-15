# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('replayer', '0014_auto_20151209_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='update',
            name='o',
            field=models.CharField(max_length=131072),
        ),
    ]
