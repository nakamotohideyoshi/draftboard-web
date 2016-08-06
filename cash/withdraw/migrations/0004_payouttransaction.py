# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-04 01:58
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('withdraw', '0003_auto_20150624_1548'),
    ]

    operations = [
        migrations.CreateModel(
            name='PayoutTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField()),
                ('withdraw_id', models.PositiveIntegerField()),
                ('withdraw_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
    ]
