# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0004_scheduledtemplatecontest_multiplier'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='createdcontest',
            unique_together=set([]),
        ),
    ]
