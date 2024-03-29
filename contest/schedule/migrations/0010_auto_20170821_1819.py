# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-21 18:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0009_block_should_create_contest_pools'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='should_create_contest_pools',
            field=models.BooleanField(default=True, help_text='If this is checked, the contest pool creator will not spawn contest pools! You should check this until you are sure all necessary games and prize structures are included.'),
        ),
    ]
