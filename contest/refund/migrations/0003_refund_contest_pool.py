# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0010_auto_20160505_1724'),
        ('refund', '0002_auto_20160325_2331'),
    ]

    operations = [
        migrations.AddField(
            model_name='refund',
            name='contest_pool',
            field=models.ForeignKey(default=None, to='contest.ContestPool'),
            preserve_default=False,
        ),
    ]
