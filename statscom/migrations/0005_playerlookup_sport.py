# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-14 21:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statscom', '0004_auto_20161109_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerlookup',
            name='sport',
            field=models.CharField(blank=True, choices=[('NBA', 'NBA'), ('NHL', 'NHL'), ('NFL', 'NFL'), ('MLB', 'MLB')], max_length=8, null=True),
        ),
    ]
