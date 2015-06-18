# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roster', '0002_auto_20150529_0216'),
        ('salary', '0006_auto_20150612_2112'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='salary',
            options={'ordering': ('primary_roster', '-amount')},
        ),
        migrations.AddField(
            model_name='salary',
            name='fppg',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='salary',
            name='primary_roster',
            field=models.ForeignKey(to='roster.RosterSpot', default=1),
            preserve_default=False,
        ),
    ]
