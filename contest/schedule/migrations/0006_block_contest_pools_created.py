# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0005_auto_20160409_2103'),
    ]

    operations = [
        migrations.AddField(
            model_name='block',
            name='contest_pools_created',
            field=models.BooleanField(default=False),
        ),
    ]
