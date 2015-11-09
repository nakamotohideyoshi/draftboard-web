# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_auto_20150408_0015'),
        ('contest', '0002_contest_currentcontest_entry_historycontest_livecontest_lobbycontest_upcomingcontest'),
        ('buyin', '0002_buyin'),
    ]

    operations = [
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
