# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('transaction', '0002_auto_20150408_0015'),
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cash', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminCashDeposit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('amount', models.DecimalField(default=0, max_digits=20, decimal_places=2)),
                ('reason', models.CharField(max_length=255, default='', blank=True)),
                ('created', models.DateTimeField(null=True, auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CashBalance',
            fields=[
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, serialize=False, primary_key=True)),
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
            name='CashTransactionDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('amount', models.DecimalField(max_digits=7, decimal_places=2)),
                ('created', models.DateTimeField(null=True, auto_now_add=True)),
                ('transaction', models.ForeignKey(to='transaction.Transaction')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='admincashdeposit',
            name='user',
            field=models.ForeignKey(related_name='admincashdeposit_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='cashtransactiondetail',
            unique_together=set([('user', 'transaction')]),
        ),
    ]
