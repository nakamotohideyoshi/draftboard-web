# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-03 19:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_merge'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='identity',
            options={'verbose_name': 'Trulioo User Identity', 'verbose_name_plural': 'Trulioo User Identities'},
        ),
        migrations.AlterField(
            model_name='limit',
            name='value',
            field=models.IntegerField(blank=True),
        ),
    ]
