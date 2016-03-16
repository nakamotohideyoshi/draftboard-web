# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nhl', '0006_auto_20160315_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='season',
            name='srid',
            field=models.CharField(help_text='the sportsradar global id of the season/schedule', max_length=64),
        ),
    ]
