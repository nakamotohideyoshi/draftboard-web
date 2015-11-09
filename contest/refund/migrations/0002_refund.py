# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_auto_20150408_0015'),
        ('contest', '0002_contest_currentcontest_entry_historycontest_livecontest_lobbycontest_upcomingcontest'),
        ('refund', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Refund',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('contest', models.ForeignKey(to='contest.Contest')),
                ('entry', models.OneToOneField(to='contest.Entry')),
                ('transaction', models.OneToOneField(to='transaction.Transaction')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
