# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test', '0016_auto_20160315_2251'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerchild',
            name='on_active_roster',
            field=models.BooleanField(default=True),
        ),
    ]
