# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-22 19:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mlb', '0015_livefeed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='livefeed',
            old_name='at_bat',
            new_name='data',
        ),
    ]
