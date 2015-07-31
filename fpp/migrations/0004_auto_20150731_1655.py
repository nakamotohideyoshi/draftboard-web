# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fpp', '0003_auto_20150727_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fpptransactiondetail',
            name='transaction',
            field=models.ForeignKey(related_name='+', to='transaction.Transaction'),
        ),
    ]
