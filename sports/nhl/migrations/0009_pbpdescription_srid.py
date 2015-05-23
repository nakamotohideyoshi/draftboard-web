# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nhl', '0008_auto_20150522_2317'),
    ]

    operations = [
        migrations.AddField(
            model_name='pbpdescription',
            name='srid',
            field=models.CharField(default='', max_length=64),
        ),
    ]
