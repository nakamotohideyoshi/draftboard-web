# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('withdraw', '0010_auto_20150426_0708'),
    ]

    operations = [
        migrations.AddField(
            model_name='paypalwithdraw',
            name='auth_status',
            field=models.CharField(null=True, max_length=128, default=''),
        ),
        migrations.AddField(
            model_name='paypalwithdraw',
            name='get_status',
            field=models.CharField(null=True, max_length=128, default=''),
        ),
        migrations.AddField(
            model_name='paypalwithdraw',
            name='payout_status',
            field=models.CharField(null=True, max_length=128, default=''),
        ),
    ]
