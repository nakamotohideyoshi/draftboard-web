# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prize', '0004_auto_20150902_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generatorsettings',
            name='buyin',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='generatorsettings',
            name='first_place',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='generatorsettings',
            name='prize_pool',
            field=models.FloatField(default=0),
        ),
    ]
