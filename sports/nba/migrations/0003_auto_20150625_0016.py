# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0002_auto_20150528_2321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameboxscore',
            name='coverage',
            field=models.CharField(default='', max_length=64),
        ),
    ]
