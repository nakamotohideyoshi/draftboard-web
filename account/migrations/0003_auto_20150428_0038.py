# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20150418_0110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='information',
            name='address2',
            field=models.CharField(max_length=255, default='', blank=True),
        ),
    ]
