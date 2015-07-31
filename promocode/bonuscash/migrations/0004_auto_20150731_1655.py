# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_auto_20150408_0015'),
        ('bonuscash', '0003_auto_20150727_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='bonuscashtransactiondetail',
            name='trigger_transaction',
            field=models.ForeignKey(to='transaction.Transaction', null=True, related_name='+', default=None),
        ),
        migrations.AlterField(
            model_name='bonuscashtransactiondetail',
            name='transaction',
            field=models.ForeignKey(related_name='+', to='transaction.Transaction'),
        ),
    ]
