# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cash', '0004_auto_20150421_1658'),
        ('withdraw', '0002_auto_20150417_2303'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewWithdraw',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('status_updated', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=254)),
                ('paypal_transaction', models.CharField(max_length=255)),
                ('check_number', models.IntegerField(unique=True, null=True)),
                ('fullname', models.CharField(default='', max_length=100)),
                ('address1', models.CharField(default='', max_length=255)),
                ('address2', models.CharField(default='', max_length=255)),
                ('city', models.CharField(default='', max_length=64)),
                ('state', models.CharField(default='', max_length=2, choices=[('NH', 'NH'), ('CA', 'CA'), ('FL', 'FL')])),
                ('zipcode', models.CharField(default='', max_length=5)),
                ('cash_transaction_detail', models.OneToOneField(to='cash.CashTransactionDetail')),
                ('status', models.ForeignKey(to='withdraw.WithdrawStatus')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
