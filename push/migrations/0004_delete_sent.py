# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-18 23:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('push', '0003_sent'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Sent',
        ),
    ]
