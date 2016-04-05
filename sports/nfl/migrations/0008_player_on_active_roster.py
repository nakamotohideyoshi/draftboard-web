# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nfl', '0007_auto_20160315_1927'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='on_active_roster',
            field=models.BooleanField(default=True),
        ),
    ]
