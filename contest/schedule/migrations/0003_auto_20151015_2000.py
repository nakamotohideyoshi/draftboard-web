# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_auto_20151018_0207'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='scheduledtemplatecontest',
            unique_together=set([('schedule', 'template_contest', 'start_time', 'duration_minutes')]),
        ),
    ]
