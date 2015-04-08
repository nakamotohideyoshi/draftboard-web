# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0006_require_contenttypes_0002'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('transaction', '0002_auto_20150408_0015'),
        ('test', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BalanceChild',
            fields=[
                ('user', models.OneToOneField(serialize=False, to=settings.AUTH_USER_MODEL, primary_key=True)),
                ('amount', models.DecimalField(max_digits=7, decimal_places=2)),
                ('transaction_id', models.PositiveIntegerField(null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('transaction_type', models.ForeignKey(null=True, to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TransactionDetailChild',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('amount', models.DecimalField(max_digits=7, decimal_places=2)),
                ('created', models.DateTimeField(null=True, auto_now_add=True)),
                ('transaction', models.ForeignKey(to='transaction.Transaction')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='transactiondetailchild',
            unique_together=set([('user', 'transaction')]),
        ),
    ]
