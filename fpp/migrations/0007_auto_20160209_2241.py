# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fpp', '0006_auto_20150918_1546'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='adminfppdeposit',
            options={'verbose_name': 'Admin Gift'},
        ),
        migrations.AlterModelOptions(
            name='adminfppwithdraw',
            options={'verbose_name': 'Admin Removal'},
        ),
        migrations.AlterModelOptions(
            name='fppbalance',
            options={'verbose_name': 'FPP Balance'},
        ),
        migrations.AlterModelOptions(
            name='fpptransactiondetail',
            options={'verbose_name': 'FPP Transaction'},
        ),
        migrations.AlterUniqueTogether(
            name='fpptransactiondetail',
            unique_together=set([]),
        ),
    ]
