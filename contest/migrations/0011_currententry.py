# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0010_auto_20160505_1724'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrentEntry',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('contest.entry',),
        ),
    ]
