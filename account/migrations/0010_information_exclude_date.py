# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-02 13:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_auto_20161028_0029'),
    ]

    operations = [
        migrations.AddField(
            model_name='information',
            name='exclude_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
