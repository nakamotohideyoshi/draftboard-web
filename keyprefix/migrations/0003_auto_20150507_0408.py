# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('keyprefix', '0002_keyprefix'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyprefix',
            name='prefix',
            field=models.CharField(max_length=16),
        ),
    ]
