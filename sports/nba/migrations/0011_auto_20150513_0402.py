# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0010_auto_20150513_0347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='height',
            field=models.FloatField(default=0.0, help_text='inches'),
        ),
        migrations.AlterField(
            model_name='player',
            name='weight',
            field=models.FloatField(default=0.0, help_text='lbs'),
        ),
    ]
