# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from ..constants import TransactionTypeConstants
def load_initial_transaction_types(apps, schema_editor):
    """
    Loads the initial TransactionType(s). This function will be passed to 'migrations.RunPython' which supplies the arguments.

    :param apps:
    :param schema_editor:
    :return:
    """
    transaction_types = [
        {
            "pk": TransactionTypeConstants.CashWithdraw.value,
            "model": "transaction.transactiontype",
            "fields":
              {
                "category": "cash",
                "description": "Cash Withdraw",
                "name": "withdraw"
              }
        },
        {
            "pk": TransactionTypeConstants.CashDeposit.value,
            "model": "transaction.transactiontype",
            "fields":
              {
                "category": "cash",
                "description": "Cash Deposit",
                "name": "deposit"
              }
        },
        {
            "pk": TransactionTypeConstants.AdminCancelWithdraw.value,
            "model": "transaction.transactiontype",
            "fields":
              {
                "category": "cash",
                "description": "Cancel Cash Withdraw",
                "name": "cancel withdraw"
              }
        },
        {
            "pk": TransactionTypeConstants.TicketConsume.value,
            "model": "transaction.transactiontype",
            "fields":
              {
                "category": "ticket",
                "description": "Ticket Consume",
                "name": "ticket consume"
              }
        },
        {
            "pk": TransactionTypeConstants.TicketDeposit.value,
            "model": "transaction.transactiontype",
            "fields":
              {
                "category": "ticket",
                "description": "Ticket Deposit",
                "name": "ticketDeposit"
              }
        },
        {
            "pk": TransactionTypeConstants.FppWithdraw.value,
            "model": "transaction.transactiontype",
            "fields":
              {
                "category": "fpp",
                "description": "FPP Withdraw",
                "name": "fpp-withdraw"
              }
        },
        {
            "pk": TransactionTypeConstants.FppDeposit.value,
            "model": "transaction.transactiontype",
            "fields":
              {
                "category": "fpp",
                "description": "FPP Deposit",
                "name": "fpp-deposit"
              }
        },
        {
            "pk": TransactionTypeConstants.BonusCashWithdraw.value,
            "model": "transaction.transactiontype",
            "fields":
              {
                "category": "bonuscash",
                "description": "BonusCash Withdraw",
                "name": "bonuscash-withdraw"
              }
        },
        {
            "pk": TransactionTypeConstants.BonusCashDeposit.value,
            "model": "transaction.transactiontype",
            "fields":
              {
                "category": "bonuscash",
                "description": "BonusCash Deposit",
                "name": "bonuscash-deposit"
              }
        },
        {
            "pk": TransactionTypeConstants.PromoCodeAdd.value,
            "model": "transaction.transactiontype",
            "fields":
              {
                "category": "promocode",
                "description": "Promo Code Added",
                "name": "promocode-add"
              }
        },
        {
            "pk": TransactionTypeConstants.PromoCodeRemove.value,
            "model": "transaction.transactiontype",
            "fields":
              {
                "category": "promocode",
                "description": "Promo Code Removed",
                "name": "promocode-remove"
              }
        }
    ]

    #
    # get the model by name
    TransactionType = apps.get_model('transaction', 'TransactionType')

    #
    # create the "fixtures" the 1.8 way, ie: programmatically
    for data in transaction_types:
        fields = data['fields']
        try:
            t = TransactionType.objects.get( pk=data['pk'] )
        except TransactionType.DoesNotExist:
            t = TransactionType()

        #
        # set the data['fields'] to the email notification
        t.category     = fields['category']
        t.description  = fields['description']
        t.name         = fields['name']
        t.save()

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transaction', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionType',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('category', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='transactiontype',
            unique_together=set([('category', 'name')]),
        ),
        migrations.AddField(
            model_name='transaction',
            name='category',
            field=models.ForeignKey(to='transaction.TransactionType'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),

        #
        # additionally, run function to load the initial objects
        migrations.RunPython( load_initial_transaction_types )
    ]
