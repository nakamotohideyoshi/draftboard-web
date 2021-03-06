# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-01 22:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_auto_20150408_0015'),
        ('cash', '0012_paypalcreditcardtransaction_paypalsavedcardtransaction_paypaltransaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='VZeroTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('transaction_identifier', models.CharField(max_length=128)),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transaction.Transaction')),
            ],
        ),
    ]
