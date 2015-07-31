# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transaction', '0002_auto_20150408_0015'),
        ('rakepaid', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RakepaidBalance',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=7)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RakepaidTransactionDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=7)),
                ('created', models.DateTimeField(null=True, auto_now_add=True)),
                ('transaction', models.ForeignKey(related_name='+', to='transaction.Transaction')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='rakepaidtransactiondetail',
            unique_together=set([('user', 'transaction')]),
        ),
    ]
