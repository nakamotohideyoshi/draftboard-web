# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0009_contest_cid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='end',
            field=models.DateTimeField(help_text='forces the end time of the contest (will override "Ends tonight" checkbox!!', blank=True, verbose_name='the time, after which real-life games will not be included in this contest'),
        ),
        migrations.AlterField(
            model_name='contest',
            name='name',
            field=models.CharField(max_length=64, help_text='The front-end name of the Contest', default='', verbose_name='Public Name'),
        ),
        migrations.AlterField(
            model_name='contest',
            name='status',
            field=models.CharField(max_length=32, choices=[('Upcoming', (('reservable', 'Reservable'), ('scheduled', 'Scheduled'))), ('Live', (('inprogress', 'In Progress'), ('completed', 'Completed'))), ('History', (('closed', 'Closed'), ('cancelled', 'Cancelled')))], default=['scheduled', 'reservable']),
        ),
    ]
