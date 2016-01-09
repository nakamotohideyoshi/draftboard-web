# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mlb', '0006_injury_ddtimestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='injury',
            name='ddtimestamp',
            field=models.BigIntegerField(help_text='the time this injury update was parsed by dataden.this will be the same value for all objects that were in the feed on the last parse.', default=0),
        ),
    ]
