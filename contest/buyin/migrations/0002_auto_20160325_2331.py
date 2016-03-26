# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buyin', '0001_squashed_0003_auto_20151108_2312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyin',
            name='contest',
            field=models.ForeignKey(to='contest.Contest', null=True),
        ),
    ]
