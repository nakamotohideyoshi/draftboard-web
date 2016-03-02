# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mlb', '0004_auto_20160302_1121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='season_type',
        ),
        migrations.RemoveField(
            model_name='game',
            name='season_year',
        ),
    ]
