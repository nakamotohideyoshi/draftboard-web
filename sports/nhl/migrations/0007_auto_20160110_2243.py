# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nhl', '0006_auto_20160110_2115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tsxinjury',
            name='content',
            field=models.CharField(max_length=16384),
        ),
        migrations.AlterField(
            model_name='tsxnews',
            name='content',
            field=models.CharField(max_length=16384),
        ),
        migrations.AlterField(
            model_name='tsxtransaction',
            name='content',
            field=models.CharField(max_length=16384),
        ),
    ]
