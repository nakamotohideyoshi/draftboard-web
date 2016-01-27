# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    replaces = [('contest', '0001_initial'), ('contest', '0002_contest_currentcontest_entry_historycontest_livecontest_lobbycontest_upcomingcontest'), ('contest', '0003_completedcontest'), ('contest', '0004_historyentry')]

    dependencies = [
        ('draftgroup', '0014_auto_20150319_0023'),
        ('lineup', '0008_auto_20150321_0552'),
        ('prize', '0005_auto_20150902_1507'),
        ('sports', '0001_squashed_0008_auto_20160119_2124'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('cid', models.CharField(help_text='unique, randomly chosen when Contest is created', editable=False, max_length=6, blank=True, default='')),
                ('name', models.CharField(help_text='The front-end name of the Contest', verbose_name='Public Name', max_length=64, default='')),
                ('status', models.CharField(choices=[('Upcoming', (('reservable', 'Reservable'), ('scheduled', 'Scheduled'))), ('Live', (('inprogress', 'In Progress'), ('completed', 'Completed'))), ('History', (('closed', 'Closed'), ('cancelled', 'Cancelled')))], max_length=32, default='scheduled')),
                ('start', models.DateTimeField(help_text='the start should coincide with the start of a real-life game.', verbose_name='The time this contest will start!')),
                ('end', models.DateTimeField(help_text='forces the end time of the contest (will override "Ends tonight" checkbox!!', blank=True, verbose_name='the time, after which real-life games will not be included in this contest')),
                ('max_entries', models.PositiveIntegerField(help_text='USER entry limit', default=1)),
                ('entries', models.PositiveIntegerField(help_text='CONTEST limit', default=2)),
                ('current_entries', models.PositiveIntegerField(help_text='The current # of entries in the contest', default=0)),
                ('gpp', models.BooleanField(help_text='a gpp Contest will not be cancelled if it does not fill', default=False)),
                ('respawn', models.BooleanField(help_text='indicates whether a new identical Contest should be created when this one fills up', default=False)),
                ('doubleup', models.BooleanField(help_text='whether this contest has a double-up style prize structure', default=False)),
                ('draft_group', models.ForeignKey(help_text='the pool of draftable players and their salaries, for the games this contest includes.', to='draftgroup.DraftGroup', null=True, blank=True, verbose_name='DraftGroup')),
                ('prize_structure', models.ForeignKey(to='prize.PrizeStructure')),
                ('site_sport', models.ForeignKey(to='sports.SiteSport')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('contest', models.ForeignKey(to='contest.Contest')),
                ('lineup', models.ForeignKey(null=True, to='lineup.Lineup')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CurrentContest',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('contest.contest',),
        ),
        migrations.CreateModel(
            name='HistoryContest',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('contest.contest',),
        ),
        migrations.CreateModel(
            name='LiveContest',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('contest.contest',),
        ),
        migrations.CreateModel(
            name='LobbyContest',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('contest.contest',),
        ),
        migrations.CreateModel(
            name='UpcomingContest',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('contest.contest',),
        ),
        migrations.CreateModel(
            name='CompletedContest',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('contest.contest',),
        ),
        migrations.CreateModel(
            name='HistoryEntry',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('contest.entry',),
        ),
    ]
