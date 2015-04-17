# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cash', '0002_auto_20150415_1816'),
    ]

    operations = [
        migrations.CreateModel(
            name='WithdrawalStatus',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('approved', models.BooleanField(default=False)),
                ('flagged', models.BooleanField(default=False)),
                ('tax_info_required', models.BooleanField(default=False)),
                ('mail_check', models.BooleanField(default=False)),
                ('paypal_email', models.CharField(default='', blank=True, max_length=255)),
                ('cash_transaction_detail', models.ForeignKey(to='cash.CashTransactionDetail')),
            ],
        ),
    ]
