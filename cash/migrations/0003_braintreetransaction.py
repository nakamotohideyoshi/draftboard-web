# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_auto_20150408_0015'),
        ('cash', '0002_auto_20150414_1827'),
    ]

    operations = [
        migrations.CreateModel(
            name='BraintreeTransaction',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('braintree_transaction', models.CharField(max_length=128)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('transaction', models.ForeignKey(to='transaction.Transaction')),
            ],
        ),
    ]
