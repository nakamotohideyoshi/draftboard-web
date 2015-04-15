# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transaction', '0002_auto_20150408_0015'),
        ('auth', '0006_require_contenttypes_0002'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('cash', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminCashDeposit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20, default=0, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('reason', models.CharField(blank=True, default='', max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AdminCashWithdrawal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20, default=0, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('reason', models.CharField(blank=True, default='', max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BraintreeTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('braintree_transaction', models.CharField(max_length=128)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('transaction', models.ForeignKey(to='transaction.Transaction')),
            ],
        ),
        migrations.CreateModel(
            name='CashBalance',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=7)),
                ('transaction_id', models.PositiveIntegerField(null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('transaction_type', models.ForeignKey(null=True, to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CashTransactionDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=7)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('transaction', models.ForeignKey(to='transaction.Transaction')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='admincashwithdrawal',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='admincashwithdrawal_user'),
        ),
        migrations.AddField(
            model_name='admincashdeposit',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='admincashdeposit_user'),
        ),
        migrations.AlterUniqueTogether(
            name='cashtransactiondetail',
            unique_together=set([('user', 'transaction')]),
        ),
    ]
