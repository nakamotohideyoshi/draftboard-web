# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-22 18:40
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('push', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PusherWebhook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('callback', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
    ]
