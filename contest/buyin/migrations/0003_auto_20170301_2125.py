# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-01 21:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('buyin', '0002_auto_20160325_2331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyin',
            name='contest',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='contest.Contest'),
        ),
        migrations.AlterField(
            model_name='buyin',
            name='entry',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='contest.Entry'),
        ),
    ]
