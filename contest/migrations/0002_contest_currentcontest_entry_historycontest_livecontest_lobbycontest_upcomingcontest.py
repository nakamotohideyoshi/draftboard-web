# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('draftgroup', '0014_auto_20150319_0023'),
        ('lineup', '0008_auto_20150321_0552'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('prize', '0005_auto_20150902_1507'),
        ('sports', '0005_merge'),
        ('contest', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('cid', models.CharField(blank=True, editable=False, max_length=6, default='', help_text='unique, randomly chosen when Contest is created')),
                ('name', models.CharField(verbose_name='Public Name', max_length=64, default='', help_text='The front-end name of the Contest')),
                ('status', models.CharField(max_length=32, default='scheduled', choices=[('Upcoming', (('reservable', 'Reservable'), ('scheduled', 'Scheduled'))), ('Live', (('inprogress', 'In Progress'), ('completed', 'Completed'))), ('History', (('closed', 'Closed'), ('cancelled', 'Cancelled')))])),
                ('start', models.DateTimeField(verbose_name='The time this contest will start!', help_text='the start should coincide with the start of a real-life game.')),
                ('end', models.DateTimeField(verbose_name='the time, after which real-life games will not be included in this contest', blank=True, help_text='forces the end time of the contest (will override "Ends tonight" checkbox!!')),
                ('max_entries', models.PositiveIntegerField(default=1, help_text='USER entry limit')),
                ('entries', models.PositiveIntegerField(default=2, help_text='CONTEST limit')),
                ('current_entries', models.PositiveIntegerField(default=0, help_text='The current # of entries in the contest')),
                ('gpp', models.BooleanField(default=False, help_text='a gpp Contest will not be cancelled if it does not fill')),
                ('respawn', models.BooleanField(default=False, help_text='indicates whether a new identical Contest should be created when this one fills up')),
                ('doubleup', models.BooleanField(default=False, help_text='whether this contest has a double-up style prize structure')),
                ('draft_group', models.ForeignKey(verbose_name='DraftGroup', blank=True, help_text='the pool of draftable players and their salaries, for the games this contest includes.', to='draftgroup.DraftGroup', null=True)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('contest', models.ForeignKey(to='contest.Contest')),
                ('lineup', models.ForeignKey(to='lineup.Lineup', null=True)),
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
    ]
