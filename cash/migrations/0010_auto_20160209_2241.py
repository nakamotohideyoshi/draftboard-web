# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cash', '0009_auto_20151204_1204'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='admincashdeposit',
            options={'verbose_name': 'Admin Gift'},
        ),
        migrations.AlterModelOptions(
            name='admincashwithdrawal',
            options={'verbose_name': 'Admin Removal'},
        ),
        migrations.AlterModelOptions(
            name='cashtransactiondetail',
            options={'verbose_name': 'Cash Transaction'},
        ),
        migrations.AlterUniqueTogether(
            name='cashtransactiondetail',
            unique_together=set([]),
        ),
    ]
