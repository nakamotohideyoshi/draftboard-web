# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-03 19:23
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_auto_20170321_1942'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='identity',
            options={'verbose_name': 'User Identity', 'verbose_name_plural': 'User Identities'},
        ),
        migrations.RemoveField(
            model_name='identity',
            name='birth_day',
        ),
        migrations.RemoveField(
            model_name='identity',
            name='birth_month',
        ),
        migrations.RemoveField(
            model_name='identity',
            name='birth_year',
        ),
        migrations.RemoveField(
            model_name='identity',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='identity',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='identity',
            name='postal_code',
        ),
        migrations.AddField(
            model_name='identity',
            name='country',
            field=models.CharField(blank=True, help_text='Country - this is where they live, not current location', max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='identity',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='identity',
            name='gidx_customer_id',
            field=models.CharField(default='validated by trulioo', help_text='The MerchantCustomerID in the GIDX dashboard', max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='identity',
            name='metadata',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='identity',
            name='region',
            field=models.CharField(blank=True, help_text='State - this is where they live, not current location', max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='identity',
            name='flagged',
            field=models.BooleanField(default=False, help_text="This identity was previously 'claimed' in our GIDX system."),
        ),
        migrations.AlterField(
            model_name='userlog',
            name='type',
            field=models.SmallIntegerField(choices=[(0, 'Location verification'), (1, 'Contest actions'), (2, 'User funds actions'), (3, 'User authentication')]),
        ),
    ]
