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
        ('cash', '0003_withdrawalstatus'),
        ('withdraw', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckWithdraw',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(null=True, auto_now_add=True)),
                ('status_updated', models.DateTimeField(auto_now=True)),
                ('check_number', models.IntegerField(unique=True, null=True)),
                ('fullname', models.CharField(default='', max_length=100)),
                ('address1', models.CharField(default='', max_length=255)),
                ('address2', models.CharField(default='', max_length=255)),
                ('city', models.CharField(default='', max_length=64)),
                ('state', models.CharField(choices=[('NH', 'NH'), ('CA', 'CA'), ('FL', 'FL')], default='', max_length=2)),
                ('zipcode', models.CharField(default='', max_length=5)),
                ('cash_transaction_detail', models.OneToOneField(to='cash.CashTransactionDetail')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PayPalWithdraw',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
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
            name='WithdrawStatus',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
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
