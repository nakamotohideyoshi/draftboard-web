# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-07 17:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lineup', '0001_squashed_0008_auto_20150321_0552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='draft_group_player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='draftgroup.Player'),
        ),
    ]
