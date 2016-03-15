# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test', '0014_auto_20160229_1717'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamechild',
            name='season_type',
        ),
        migrations.RemoveField(
            model_name='gamechild',
            name='season_year',
        ),
    ]
