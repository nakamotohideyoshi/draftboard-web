# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-27 17:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0008_delete_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='block',
            name='should_create_contest_pools',
            field=models.BooleanField(default=True),
        ),
    ]
