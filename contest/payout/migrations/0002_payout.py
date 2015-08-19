# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_auto_20150408_0015'),
        ('contest', '0010_auto_20150722_1328'),
        ('payout', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payout',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('rank', models.PositiveIntegerField(default=0)),
                ('contest', models.ForeignKey(to='contest.Contest')),
                ('entry', models.ForeignKey(to='contest.Entry')),
                ('transaction', models.ForeignKey(to='transaction.Transaction')),
            ],
        ),
    ]
