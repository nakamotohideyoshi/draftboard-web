# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-20 00:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test', '0004_auto_20170303_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamechild',
            name='boxscore_data',
            field=models.CharField(blank=True, max_length=8192, null=True),
        ),
    ]
