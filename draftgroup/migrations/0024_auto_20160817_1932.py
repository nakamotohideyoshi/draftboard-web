# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-17 23:32
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('draftgroup', '0023_auto_20160525_2200'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameupdate',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 17, 23, 32, 48, 157573, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='playerupdate',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 17, 23, 32, 52, 516645, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
