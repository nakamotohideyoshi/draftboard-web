# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0012_entry_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='lineup',
            field=models.ForeignKey(to='lineup.Lineup', null=True),
        ),
    ]
