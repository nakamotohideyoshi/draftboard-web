# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0015_auto_20150817_1959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='draft_group',
            field=models.ForeignKey(null=True, help_text='the pool of draftable players and their salaries, for the games this contest includes.', to='draftgroup.DraftGroup', verbose_name='DraftGroup', blank=True),
        ),
        migrations.AlterField(
            model_name='contest',
            name='status',
            field=models.CharField(choices=[('Upcoming', (('reservable', 'Reservable'), ('scheduled', 'Scheduled'))), ('Live', (('inprogress', 'In Progress'), ('completed', 'Completed'))), ('History', (('closed', 'Closed'), ('cancelled', 'Cancelled')))], max_length=32, default='scheduled'),
        ),
    ]
