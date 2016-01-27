# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    replaces = [('buyin', '0001_initial'), ('buyin', '0002_buyin'), ('buyin', '0003_auto_20151108_2312')]

    dependencies = [
        ('contest', '0002_contest_currentcontest_entry_historycontest_livecontest_lobbycontest_upcomingcontest'),
        ('transaction', '0002_auto_20150408_0015'),
    ]

    operations = [
        migrations.CreateModel(
            name='Buyin',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='buyin',
            name='contest',
            field=models.ForeignKey(to='contest.Contest'),
        ),
        migrations.AddField(
            model_name='buyin',
            name='entry',
            field=models.OneToOneField(to='contest.Entry'),
        ),
        migrations.AddField(
            model_name='buyin',
            name='transaction',
            field=models.OneToOneField(to='transaction.Transaction'),
        ),
    ]
