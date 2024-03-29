# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-30 21:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gidx', '0002_auto_20170720_0034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gidxsession',
            name='device_location',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='gidxsession',
            name='gidx_customer_id',
            field=models.CharField(blank=True, help_text='The MerchantCustomerID in the GIDX dashboard', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='gidxsession',
            name='reason_codes',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='gidxsession',
            name='session_id',
            field=models.CharField(help_text='MerchantSessionID field in GIDX responses.', max_length=128),
        ),
    ]
