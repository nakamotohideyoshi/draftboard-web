# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mlb', '0006_auto_20160309_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='season',
            name='srid',
            field=models.CharField(help_text='the sportsradar global id of the season/schedule', max_length=64),
        ),
    ]
