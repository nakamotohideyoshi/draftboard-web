# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0014_auto_20150813_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='status',
            field=models.CharField(choices=[('Upcoming', (('reservable', 'Reservable'), ('scheduled', 'Scheduled'))), ('Live', (('inprogress', 'In Progress'), ('completed', 'Completed'))), ('History', (('closed', 'Closed'), ('cancelled', 'Cancelled')))], default='reservable', max_length=32),
        ),
    ]
