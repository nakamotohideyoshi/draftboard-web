# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('withdraw', '0007_automaticwithdraw'),
    ]

    operations = [
        migrations.CreateModel(
            name='PendingWithdrawMax',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('max_pending', models.IntegerField(default=3)),
            ],
        ),
    ]
