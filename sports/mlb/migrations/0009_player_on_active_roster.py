# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mlb', '0008_auto_20160404_1312'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='on_active_roster',
            field=models.BooleanField(default=True),
        ),
    ]
