# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_auto_20150408_0015'),
        ('contest', '0002_contest_currentcontest_entry_historycontest_livecontest_lobbycontest_upcomingcontest'),
        ('payout', '0002_payout'),
    ]

    operations = [
        migrations.CreateModel(
            name='FPP',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('contest', models.ForeignKey(to='contest.Contest')),
                ('transaction', models.OneToOneField(to='transaction.Transaction')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Rake',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('contest', models.ForeignKey(to='contest.Contest')),
                ('transaction', models.OneToOneField(to='transaction.Transaction')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
