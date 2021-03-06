# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-07 19:35
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0012_identity_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='GidxCustomerMonitor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gidx_customer_id', models.CharField(help_text='The MerchantCustomerID in the GIDX dashboard', max_length=256)),
                ('reason_codes', models.CharField(max_length=128)),
                ('watch_checks', models.CharField(max_length=128)),
                ('location_detail', models.CharField(max_length=128)),
                ('identity_confidence_score', models.DecimalField(decimal_places=2, max_digits=6)),
                ('fraud_confidence_score', models.DecimalField(decimal_places=2, max_digits=6)),
                ('request_data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('identity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gidx_customer_monitors', to='account.Identity')),
            ],
        ),
        migrations.CreateModel(
            name='GidxSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gidx_customer_id', models.CharField(help_text='The MerchantCustomerID in the GIDX dashboard', max_length=256)),
                ('session_id', models.CharField(max_length=128)),
                ('service_type', models.CharField(max_length=128)),
                ('device_location', models.CharField(max_length=128)),
                ('request_data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('reason_codes', models.CharField(max_length=128)),
                ('response_data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gidx_sessions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
