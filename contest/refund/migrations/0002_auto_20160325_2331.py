# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('refund', '0001_squashed_0002_refund'),
    ]

    operations = [
        migrations.AlterField(
            model_name='refund',
            name='contest',
            field=models.ForeignKey(to='contest.Contest', null=True),
        ),
    ]
