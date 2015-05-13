# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0011_auto_20150513_0402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='srid_venue',
            field=models.CharField(max_length=64, help_text='the sportsradar global id'),
        ),
    ]
