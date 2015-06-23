# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0002_contest_entry'),
        ('transaction', '0002_auto_20150408_0015'),
        ('payout', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payout',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('rank', models.PositiveIntegerField(default=0)),
                ('contest', models.ForeignKey(to='contest.Contest')),
                ('entry', models.ForeignKey(to='contest.Entry')),
                ('transaction', models.ForeignKey(to='transaction.Transaction')),
            ],
        ),
    ]
