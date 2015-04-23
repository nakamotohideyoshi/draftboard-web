# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from ..constants import WithdrawStatusConstants

def load_initial_data(apps, schema_editor):
    """
    Loads the initial WithdrawStatus(s). This function will be passed to 'migrations.RunPython' which supplies the arguments.

    :param apps:
    :param schema_editor:
    :return:
    """


    #
    # get the model by name
    WithdrawStatus = apps.get_model('withdraw', 'WithdrawStatus')
    arr =  WithdrawStatusConstants.getJSON()
    for data in arr:
        fields = data['fields']
        try:
            t = WithdrawStatus.objects.get( pk=data['pk'] )
        except WithdrawStatus.DoesNotExist:
            t = WithdrawStatus()

        #
        # set the data['fields'] to the email notification
        t.category     = fields['category']
        t.description  = fields['description']
        t.name         = fields['name']
        t.save()



class Migration(migrations.Migration):

    dependencies = [
        ('cash', '0002_auto_20150422_1944'),
        ('withdraw', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckWithdraw',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, auto_now_add=True)),
                ('status_updated', models.DateTimeField(auto_now=True)),
                ('check_number', models.IntegerField(unique=True, null=True)),
                ('fullname', models.CharField(max_length=100, default='')),
                ('address1', models.CharField(max_length=255, default='')),
                ('address2', models.CharField(max_length=255, default='')),
                ('city', models.CharField(max_length=64, default='')),
                ('state', models.CharField(max_length=2, default='', choices=[('NH', 'NH'), ('CA', 'CA'), ('FL', 'FL')])),
                ('zipcode', models.CharField(max_length=5, default='')),
                ('cash_transaction_detail', models.OneToOneField(to='cash.CashTransactionDetail')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PayPalWithdraw',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, auto_now_add=True)),
                ('status_updated', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=254)),
                ('paypal_transaction', models.CharField(max_length=255)),
                ('cash_transaction_detail', models.OneToOneField(to='cash.CashTransactionDetail')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReviewWithdraw',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, auto_now_add=True)),
                ('status_updated', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=254)),
                ('paypal_transaction', models.CharField(max_length=255)),
                ('check_number', models.IntegerField(unique=True, null=True)),
                ('fullname', models.CharField(max_length=100, default='')),
                ('address1', models.CharField(max_length=255, default='')),
                ('address2', models.CharField(max_length=255, default='')),
                ('city', models.CharField(max_length=64, default='')),
                ('state', models.CharField(max_length=2, default='', choices=[('NH', 'NH'), ('CA', 'CA'), ('FL', 'FL')])),
                ('zipcode', models.CharField(max_length=5, default='')),
                ('cash_transaction_detail', models.OneToOneField(to='cash.CashTransactionDetail')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WithdrawStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='withdrawstatus',
            unique_together=set([('category', 'name')]),
        ),
        migrations.AddField(
            model_name='reviewwithdraw',
            name='status',
            field=models.ForeignKey(to='withdraw.WithdrawStatus'),
        ),
        migrations.AddField(
            model_name='paypalwithdraw',
            name='status',
            field=models.ForeignKey(to='withdraw.WithdrawStatus'),
        ),
        migrations.AddField(
            model_name='checkwithdraw',
            name='status',
            field=models.ForeignKey(to='withdraw.WithdrawStatus'),
        ),

        #
        # additionally, run function to load the initial objects
        migrations.RunPython( load_initial_data )
    ]
