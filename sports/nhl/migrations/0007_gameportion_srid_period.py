# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nhl', '0006_gameportion'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameportion',
            name='srid_period',
            field=models.CharField(max_length=64, default=''),
        ),
    ]
