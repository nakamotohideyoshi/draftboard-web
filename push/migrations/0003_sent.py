# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-22 19:59
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('push', '0002_pusherwebhook'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('channel', models.CharField(max_length=64)),
                ('event', models.CharField(max_length=64)),
                ('api_response', django.contrib.postgres.fields.jsonb.JSONField()),
                ('data', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
    ]
