# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_auto_20150408_0015'),
        ('cash', '0007_auto_20150918_1546'),
    ]

    operations = [
        migrations.CreateModel(
            name='OptimalPaymentsTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('netbanx_transaction_id', models.CharField(help_text='netbanx id found in the payment processor account', max_length=128)),
                ('created', models.DateTimeField(null=True, auto_now_add=True)),
                ('transaction', models.ForeignKey(to='transaction.Transaction')),
            ],
        ),
    ]
