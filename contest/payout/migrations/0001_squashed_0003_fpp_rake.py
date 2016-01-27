# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    replaces = [('payout', '0001_initial'), ('payout', '0002_payout'), ('payout', '0003_fpp_rake')]

    dependencies = [
        ('transaction', '0002_auto_20150408_0015'),
        ('contest', '0002_contest_currentcontest_entry_historycontest_livecontest_lobbycontest_upcomingcontest'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payout',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('rank', models.PositiveIntegerField(default=0)),
                ('contest', models.ForeignKey(to='contest.Contest')),
                ('entry', models.OneToOneField(to='contest.Entry')),
                ('transaction', models.OneToOneField(to='transaction.Transaction')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FPP',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('contest', models.ForeignKey(to='contest.Contest')),
                ('transaction', models.OneToOneField(to='transaction.Transaction')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
