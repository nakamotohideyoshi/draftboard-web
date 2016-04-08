# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0006_auto_20160407_1435'),
    ]

    operations = [
        migrations.CreateModel(
            name='UpcomingBlock',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('schedule.block',),
        ),
    ]
