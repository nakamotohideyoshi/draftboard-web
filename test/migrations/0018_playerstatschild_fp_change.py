# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-27 22:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test', '0017_playerchild_on_active_roster'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerstatschild',
            name='fp_change',
            field=models.FloatField(default=0.0),
        ),
    ]
