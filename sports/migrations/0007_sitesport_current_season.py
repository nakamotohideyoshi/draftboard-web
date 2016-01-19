# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0006_auto_20151216_1353'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesport',
            name='current_season',
            field=models.IntegerField(default=2015),
            preserve_default=False,
        ),
    ]
