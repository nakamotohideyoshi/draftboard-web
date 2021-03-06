# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-15 11:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# contest.migrations.0013_auto_20160719_1804
def load_initial_data(apps, schema_editor):
    """
    Loads the initial SkillLevel models.
    This function will be passed to 'migrations.RunPython' which supplies the arguments.

    :param apps:
    :param schema_editor:
    :return:
    """

    skill_levels = [
        {
            'name': 'veteran',
            'gte': 10.0,
            'enforced': True,
        },
        {
            'name': 'rookie',
            'gte': 0.0,
            'enforced': True,
        },
        {
            'name': 'all',
            'gte': 0,
            'enforced': False,
        }
    ]

    #
    # get the model by name
    SkillLevel = apps.get_model('contest', 'SkillLevel')

    for data in skill_levels:
        skill_level, created = SkillLevel.objects.get_or_create(name=data.get('name'),
                                        gte=data.get('gte'), enforced=data.get('enforced'))


class Migration(migrations.Migration):

    replaces = [('contest', '0001_initial'), ('contest', '0002_contest_currentcontest_entry_historycontest_livecontest_lobbycontest_upcomingcontest'), ('contest', '0003_completedcontest'), ('contest', '0004_historyentry'), ('contest', '0002_auto_20160209_2241'), ('contest', '0003_closedcontest_closedentry'), ('contest', '0004_auto_20160321_2142'), ('contest', '0005_auto_20160321_2239'), ('contest', '0006_auto_20160325_2357'), ('contest', '0007_currentcontest_upcomingcontestpool'), ('contest', '0008_livecontestpool'), ('contest', '0009_auto_20160409_1845'), ('contest', '0010_auto_20160505_1724'), ('contest', '0011_currententry'), ('contest', '0012_auto_20160705_1647'), ('contest', '0013_auto_20160719_1804')]

    initial = True

    dependencies = [
        ('draftgroup', '0018_draftgroup_fantasy_points_finalized'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sports', '0001_squashed_0008_auto_20160119_2124'),
        ('prize', '0006_auto_20160209_2241'),
        ('prize', '0005_auto_20150902_1507'),
        ('lineup', '0008_auto_20150321_0552'),
        ('draftgroup', '0014_auto_20150319_0023'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('cid', models.CharField(blank=True, default='', editable=False, help_text='unique, randomly chosen when Contest is created', max_length=6)),
                ('name', models.CharField(default='', help_text='The front-end name of the Contest', max_length=64, verbose_name='Public Name')),
                ('status', models.CharField(choices=[('Upcoming', (('reservable', 'Reservable'), ('scheduled', 'Scheduled'))), ('Live', (('inprogress', 'In Progress'), ('completed', 'Completed'))), ('History', (('closed', 'Closed'), ('cancelled', 'Cancelled')))], default='scheduled', max_length=32)),
                ('start', models.DateTimeField(help_text='the start should coincide with the start of a real-life game.', verbose_name='The time this contest will start!')),
                ('end', models.DateTimeField(blank=True, help_text='forces the end time of the contest (will override "Ends tonight" checkbox!!', verbose_name='the time, after which real-life games will not be included in this contest')),
                ('max_entries', models.PositiveIntegerField(default=1, help_text='USER entry limit')),
                ('entries', models.PositiveIntegerField(default=2, help_text='CONTEST limit')),
                ('current_entries', models.PositiveIntegerField(default=0, help_text='The current # of entries in the contest')),
                ('gpp', models.BooleanField(default=False, help_text='a gpp Contest will not be cancelled if it does not fill')),
                ('respawn', models.BooleanField(default=False, help_text='indicates whether a new identical Contest should be created when this one fills up')),
                ('doubleup', models.BooleanField(default=False, help_text='whether this contest has a double-up style prize structure')),
                ('draft_group', models.ForeignKey(blank=True, help_text='the pool of draftable players and their salaries, for the games this contest includes.', null=True, on_delete=django.db.models.deletion.CASCADE, to='draftgroup.DraftGroup', verbose_name='DraftGroup')),
                ('prize_structure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prize.PrizeStructure')),
                ('site_sport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sports.SiteSport')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contest.Contest')),
                ('lineup', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='lineup.Lineup')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
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
        migrations.AlterModelOptions(
            name='completedcontest',
            options={'verbose_name': 'Completed', 'verbose_name_plural': 'Completed'},
        ),
        migrations.AlterModelOptions(
            name='contest',
            options={'verbose_name': 'All Contests', 'verbose_name_plural': 'All Contests'},
        ),
        migrations.AlterModelOptions(
            name='entry',
            options={'verbose_name': 'Entry', 'verbose_name_plural': 'Entries'},
        ),
        migrations.AlterModelOptions(
            name='historycontest',
            options={'verbose_name': 'History', 'verbose_name_plural': 'History'},
        ),
        migrations.AlterModelOptions(
            name='livecontest',
            options={'verbose_name': 'Live', 'verbose_name_plural': 'Live'},
        ),
        migrations.AlterModelOptions(
            name='upcomingcontest',
            options={'verbose_name': 'Upcoming', 'verbose_name_plural': 'Upcoming'},
        ),
        migrations.AddField(
            model_name='entry',
            name='final_rank',
            field=models.IntegerField(default=-1, help_text='the rank of the entry after the contest has been paid out'),
        ),
        migrations.AlterField(
            model_name='contest',
            name='end',
            field=models.DateTimeField(blank=True, help_text='forces the end time of the contest (will override "Ends tonight" checkbox!!', verbose_name='Cutoff Time'),
        ),
        migrations.AlterField(
            model_name='contest',
            name='start',
            field=models.DateTimeField(help_text='the start should coincide with the start of a real-life game.', verbose_name='Start Time'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='contest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contests', to='contest.Contest'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='lineup',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='lineup.Lineup'),
        ),
        migrations.CreateModel(
            name='ClosedContest',
            fields=[
            ],
            options={
                'verbose_name': 'Paid Out',
                'verbose_name_plural': 'Paid Out',
                'proxy': True,
            },
            bases=('contest.contest',),
        ),
        migrations.CreateModel(
            name='ClosedEntry',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('contest.entry',),
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
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contest_contest_site_sport', to='sports.SiteSport'),
        ),
        migrations.AlterField(
            model_name='contest',
            name='status',
            field=models.CharField(choices=[('Upcoming', (('reservable', 'Reservable'), ('scheduled', 'Scheduled'))), ('Live', (('inprogress', 'In Progress'), ('completed', 'Completed'))), ('History', (('closed', 'Closed'), ('cancelled', 'Cancelled')))], default='inprogress', max_length=32),
        ),
        migrations.CreateModel(
            name='ContestPool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('cid', models.CharField(blank=True, default='', editable=False, help_text='unique, randomly chosen when Contest is created', max_length=6)),
                ('name', models.CharField(default='', help_text='The front-end name of the Contest', max_length=64, verbose_name='Public Name')),
                ('start', models.DateTimeField(help_text='the start should coincide with the start of a real-life game.', verbose_name='Start Time')),
                ('end', models.DateTimeField(blank=True, help_text='forces the end time of the contest (will override "Ends tonight" checkbox!!', verbose_name='Cutoff Time')),
                ('max_entries', models.PositiveIntegerField(default=1, help_text='USER entry limit')),
                ('entries', models.PositiveIntegerField(default=2, help_text='CONTEST limit')),
                ('current_entries', models.PositiveIntegerField(default=0, help_text='The current # of entries in the contest')),
                ('gpp', models.BooleanField(default=False, help_text='a gpp Contest will not be cancelled if it does not fill')),
                ('respawn', models.BooleanField(default=False, help_text='indicates whether a new identical Contest should be created when this one fills up')),
                ('doubleup', models.BooleanField(default=False, help_text='whether this contest has a double-up style prize structure')),
                ('status', models.CharField(choices=[('Scheduled', (('scheduled', 'Scheduled'),)), ('Created', (('created', 'Created'),))], default='scheduled', max_length=32)),
                ('draft_group', models.ForeignKey(blank=True, help_text='the pool of draftable players and their salaries, for the games this contest includes.', null=True, on_delete=django.db.models.deletion.CASCADE, to='draftgroup.DraftGroup', verbose_name='DraftGroup')),
                ('prize_structure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prize.PrizeStructure')),
                ('site_sport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contest_contestpool_site_sport', to='sports.SiteSport')),
            ],
            options={
                'verbose_name': 'Contest Pools',
                'abstract': False,
                'verbose_name_plural': 'Contest Pools',
            },
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
        migrations.CreateModel(
            name='LobbyContestPool',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('contest.contestpool',),
        ),
        migrations.AddField(
            model_name='entry',
            name='contest_pool',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contest_pools', to='contest.ContestPool'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='contest',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contests', to='contest.Contest'),
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
            name='UpcomingContestPool',
            fields=[
            ],
            options={
                'verbose_name': 'Upcoming',
                'verbose_name_plural': 'Upcoming',
                'proxy': True,
            },
            bases=('contest.contestpool',),
        ),
        migrations.CreateModel(
            name='LiveContestPool',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('contest.contestpool',),
        ),
        migrations.DeleteModel(
            name='CurrentContestPool',
        ),
        migrations.AlterModelOptions(
            name='lobbycontestpool',
            options={'verbose_name': 'Contest Pools (Lobby)', 'verbose_name_plural': 'Contest Pools (Lobby)'},
        ),
        migrations.AlterModelOptions(
            name='contestpool',
            options={'verbose_name': 'Contest Pools (All)', 'verbose_name_plural': 'Contest Pools (All)'},
        ),
        migrations.AlterField(
            model_name='contest',
            name='name',
            field=models.CharField(default='', help_text='frontfacing name', max_length=64, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='contestpool',
            name='name',
            field=models.CharField(default='', help_text='frontfacing name', max_length=64, verbose_name='Name'),
        ),
        migrations.CreateModel(
            name='CurrentEntry',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('contest.entry',),
        ),
        migrations.AlterField(
            model_name='contest',
            name='name',
            field=models.CharField(default='', help_text='frontfacing name', max_length=256, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='contestpool',
            name='name',
            field=models.CharField(default='', help_text='frontfacing name', max_length=256, verbose_name='Name'),
        ),
        migrations.CreateModel(
            name='SkillLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=32, unique=True)),
                ('gte', models.FloatField(default=0.0, help_text='this SkillLevel is for buyins Greater-than-or-Equal (gte) to this value.')),
                ('enforced', models.BooleanField(default=True)),
            ],
        ),
        migrations.RunPython(
            code=load_initial_data,
        ),
        migrations.AddField(
            model_name='contest',
            name='skill_level',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='contest.SkillLevel'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contestpool',
            name='skill_level',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='contest.SkillLevel'),
            preserve_default=False,
        ),
    ]
