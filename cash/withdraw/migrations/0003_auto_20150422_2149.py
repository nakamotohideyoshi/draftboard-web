# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cash', '0002_auto_20150422_1944'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('withdraw', '0002_auto_20150422_1944'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewPendingWithdraw',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('created', models.DateTimeField(null=True, auto_now_add=True)),
                ('status_updated', models.DateTimeField(auto_now=True)),
                ('object_id', models.PositiveIntegerField()),
                ('cash_transaction_detail', models.OneToOneField(to='cash.CashTransactionDetail')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('status', models.ForeignKey(to='withdraw.WithdrawStatus')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='reviewwithdraw',
            name='cash_transaction_detail',
        ),
        migrations.RemoveField(
            model_name='reviewwithdraw',
            name='status',
        ),
        migrations.DeleteModel(
            name='ReviewWithdraw',
        ),
    ]
