# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0003_auto_20150528_2321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesport',
            name='name',
            field=models.CharField(unique=True, max_length=128),
        ),
    ]
