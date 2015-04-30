# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transaction', '0002_auto_20150408_0015'),
        ('auth', '0006_require_contenttypes_0002'),
        ('bonuscash', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminBonusCashDeposit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(default=0, max_digits=20, decimal_places=2)),
                ('reason', models.CharField(default='', blank=True, max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AdminBonusCashWithdraw',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(default=0, max_digits=20, decimal_places=2)),
                ('reason', models.CharField(default='', blank=True, max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BonusCashBalance',
            fields=[
                ('user', models.OneToOneField(serialize=False, to=settings.AUTH_USER_MODEL, primary_key=True)),
                ('amount', models.DecimalField(max_digits=7, decimal_places=2)),
                ('transaction_id', models.PositiveIntegerField(null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('transaction_type', models.ForeignKey(to='contenttypes.ContentType', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BonusCashTransactionDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(max_digits=7, decimal_places=2)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('transaction', models.ForeignKey(to='transaction.Transaction')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='adminbonuscashwithdraw',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='adminbonuscashwithdraw_user'),
        ),
        migrations.AddField(
            model_name='adminbonuscashdeposit',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='adminbonusbashdeposit_user'),
        ),
        migrations.AlterUniqueTogether(
            name='bonuscashtransactiondetail',
            unique_together=set([('user', 'transaction')]),
        ),
    ]
