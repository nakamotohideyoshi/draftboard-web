# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0007_injury_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='injury',
            name='iid',
            field=models.CharField(unique=True, help_text='custom injury id', default=None, max_length=64),
            preserve_default=False,
        ),
    ]
