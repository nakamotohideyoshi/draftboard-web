# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_auto_20150408_0015'),
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('fpp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminFppDeposit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('amount', models.DecimalField(default=0, decimal_places=2, max_digits=20)),
                ('reason', models.CharField(default='', blank=True, max_length=255)),
                ('created', models.DateTimeField(null=True, auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AdminFppWithdraw',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('amount', models.DecimalField(default=0, decimal_places=2, max_digits=20)),
                ('reason', models.CharField(default='', blank=True, max_length=255)),
                ('created', models.DateTimeField(null=True, auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FppBalance',
            fields=[
                ('user', models.OneToOneField(serialize=False, primary_key=True, to=settings.AUTH_USER_MODEL)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=7)),
                ('transaction_id', models.PositiveIntegerField(null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('transaction_type', models.ForeignKey(to='contenttypes.ContentType', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FppTransactionDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=7)),
                ('created', models.DateTimeField(null=True, auto_now_add=True)),
                ('transaction', models.ForeignKey(to='transaction.Transaction')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='adminfppwithdraw',
            name='user',
            field=models.ForeignKey(related_name='adminfppwithdraw_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='adminfppdeposit',
            name='user',
            field=models.ForeignKey(related_name='adminfppdeposit_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='fpptransactiondetail',
            unique_together=set([('user', 'transaction')]),
        ),
    ]
