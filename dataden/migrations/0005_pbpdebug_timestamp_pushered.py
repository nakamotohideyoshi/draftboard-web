# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataden', '0004_auto_20160411_2117'),
    ]

    operations = [
        migrations.AddField(
            model_name='pbpdebug',
            name='timestamp_pushered',
            field=models.DateTimeField(null=True),
        ),
    ]
