# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('withdraw', '0005_auto_20150423_0542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkwithdraw',
            name='check_number',
            field=models.IntegerField(null=True, blank=True, unique=True),
        ),
    ]
