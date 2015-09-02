# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lineup', '0005_auto_20150817_1959'),
    ]

    operations = [
        migrations.AddField(
            model_name='lineup',
            name='name',
            field=models.CharField(default='', max_length=64),
        ),
    ]
