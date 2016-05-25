# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mlb', '0011_auto_20160524_2033'),
    ]

    operations = [
        migrations.AddField(
            model_name='probablepitcher',
            name='srid_team',
            field=models.CharField(max_length=64, default=''),
            preserve_default=False,
        ),
    ]
