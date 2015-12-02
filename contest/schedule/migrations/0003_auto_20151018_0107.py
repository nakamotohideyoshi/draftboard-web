# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0002_contest_currentcontest_entry_historycontest_livecontest_lobbycontest_upcomingcontest'),
        ('schedule', '0002_auto_20151108_2312'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreatedContest',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('day', models.DateField()),
                ('contest', models.ForeignKey(to='contest.Contest', related_name='scheduled_contest_contest')),
                ('scheduled_template_contest', models.ForeignKey(to='schedule.ScheduledTemplateContest', related_name='scheduled_contest_history_item')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='createdcontest',
            unique_together=set([('day', 'scheduled_template_contest')]),
        ),
    ]
