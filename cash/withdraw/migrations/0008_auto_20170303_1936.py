# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-03 19:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('withdraw', '0007_auto_20161026_0117'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payouttransaction',
            options={'get_latest_by': 'created'},
        ),
    ]
