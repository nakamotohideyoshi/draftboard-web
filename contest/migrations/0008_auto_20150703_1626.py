# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0007_lobbycontest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='status',
            field=models.CharField(max_length=32, default='scheduled', choices=[('Upcoming', (('reservable', 'Reservable'), ('scheduled', 'Scheduled'))), ('Live', (('inprogress', 'In Progress'),)), ('History', (('closed', 'Closed'), ('cancelled', 'Cancelled')))]),
        ),
    ]
