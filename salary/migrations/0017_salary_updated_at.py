# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-10 19:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0016_auto_20161015_1537'),
    ]

    operations = [
        migrations.AddField(
            model_name='salary',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='When was this salary last updated?', null=True),
        ),
    ]
