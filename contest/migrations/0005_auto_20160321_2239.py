# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prize', '0006_auto_20160209_2241'),
        ('draftgroup', '0018_draftgroup_fantasy_points_finalized'),
        ('sports', '0001_squashed_0008_auto_20160119_2124'),
        ('contest', '0004_auto_20160321_2142'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContestPool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('cid', models.CharField(editable=False, blank=True, max_length=6, help_text='unique, randomly chosen when Contest is created', default='')),
                ('name', models.CharField(default='', max_length=64, help_text='The front-end name of the Contest', verbose_name='Public Name')),
                ('start', models.DateTimeField(help_text='the start should coincide with the start of a real-life game.', verbose_name='Start Time')),
                ('end', models.DateTimeField(blank=True, help_text='forces the end time of the contest (will override "Ends tonight" checkbox!!', verbose_name='Cutoff Time')),
                ('max_entries', models.PositiveIntegerField(default=1, help_text='USER entry limit')),
                ('entries', models.PositiveIntegerField(default=2, help_text='CONTEST limit')),
                ('current_entries', models.PositiveIntegerField(default=0, help_text='The current # of entries in the contest')),
                ('gpp', models.BooleanField(default=False, help_text='a gpp Contest will not be cancelled if it does not fill')),
                ('respawn', models.BooleanField(default=False, help_text='indicates whether a new identical Contest should be created when this one fills up')),
                ('doubleup', models.BooleanField(default=False, help_text='whether this contest has a double-up style prize structure')),
                ('status', models.CharField(choices=[('Scheduled', (('scheduled', 'Scheduled'),)), ('Created', (('created', 'Created'),))], default='scheduled', max_length=32)),
                ('draft_group', models.ForeignKey(blank=True, to='draftgroup.DraftGroup', help_text='the pool of draftable players and their salaries, for the games this contest includes.', null=True, verbose_name='DraftGroup')),
                ('prize_structure', models.ForeignKey(to='prize.PrizeStructure')),
                ('site_sport', models.ForeignKey(to='sports.SiteSport', related_name='contest_contestpool_site_sport')),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'Contest Pools',
                'verbose_name': 'Contest Pools',
            },
        ),
        migrations.RemoveField(
            model_name='pool',
            name='draft_group',
        ),
        migrations.RemoveField(
            model_name='pool',
            name='prize_structure',
        ),
        migrations.RemoveField(
            model_name='pool',
            name='site_sport',
        ),
        migrations.DeleteModel(
            name='Pool',
        ),
        migrations.CreateModel(
            name='CurrentContestPool',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('contest.contestpool',),
        ),
    ]
