# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prize', '0006_auto_20160209_2241'),
        ('draftgroup', '0018_draftgroup_fantasy_points_finalized'),
        ('sports', '0001_squashed_0008_auto_20160119_2124'),
        ('contest', '0003_closedcontest_closedentry'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pool',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('cid', models.CharField(default='', blank=True, editable=False, help_text='unique, randomly chosen when Contest is created', max_length=6)),
                ('name', models.CharField(verbose_name='Public Name', default='', max_length=64, help_text='The front-end name of the Contest')),
                ('start', models.DateTimeField(verbose_name='Start Time', help_text='the start should coincide with the start of a real-life game.')),
                ('end', models.DateTimeField(verbose_name='Cutoff Time', blank=True, help_text='forces the end time of the contest (will override "Ends tonight" checkbox!!')),
                ('max_entries', models.PositiveIntegerField(default=1, help_text='USER entry limit')),
                ('entries', models.PositiveIntegerField(default=2, help_text='CONTEST limit')),
                ('current_entries', models.PositiveIntegerField(default=0, help_text='The current # of entries in the contest')),
                ('gpp', models.BooleanField(default=False, help_text='a gpp Contest will not be cancelled if it does not fill')),
                ('respawn', models.BooleanField(default=False, help_text='indicates whether a new identical Contest should be created when this one fills up')),
                ('doubleup', models.BooleanField(default=False, help_text='whether this contest has a double-up style prize structure')),
                ('draft_group', models.ForeignKey(to='draftgroup.DraftGroup', verbose_name='DraftGroup', blank=True, help_text='the pool of draftable players and their salaries, for the games this contest includes.', null=True)),
                ('prize_structure', models.ForeignKey(to='prize.PrizeStructure')),
                ('site_sport', models.ForeignKey(to='sports.SiteSport', related_name='contest_pool_site_sport')),
            ],
            options={
                'verbose_name': 'Contest Pools',
                'abstract': False,
                'verbose_name_plural': 'Contest Pools',
            },
        ),
        migrations.DeleteModel(
            name='CurrentContest',
        ),
        migrations.DeleteModel(
            name='LobbyContest',
        ),
        migrations.DeleteModel(
            name='UpcomingContest',
        ),
        migrations.AlterField(
            model_name='contest',
            name='site_sport',
            field=models.ForeignKey(to='sports.SiteSport', related_name='contest_contest_site_sport'),
        ),
        migrations.AlterField(
            model_name='contest',
            name='status',
            field=models.CharField(default='inprogress', choices=[('Upcoming', (('reservable', 'Reservable'), ('scheduled', 'Scheduled'))), ('Live', (('inprogress', 'In Progress'), ('completed', 'Completed'))), ('History', (('closed', 'Closed'), ('cancelled', 'Cancelled')))], max_length=32),
        ),
    ]
