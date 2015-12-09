# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('replayer', '0012_timemachine_snapshot_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timemachine',
            name='snapshot_datetime',
            field=models.DateTimeField(help_text='internal field for settings the time to rewind the server to when the replay dump is re-loaded.', null=True),
        ),
    ]
