# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('draftgroup', '0014_auto_20150319_0023'),
        ('prize', '0005_auto_20150902_1507'),
        ('sports', '0005_merge'),
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Interval',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('monday', models.BooleanField(default=False)),
                ('tuesday', models.BooleanField(default=False)),
                ('wednesday', models.BooleanField(default=False)),
                ('thursday', models.BooleanField(default=False)),
                ('friday', models.BooleanField(default=False)),
                ('saturday', models.BooleanField(default=False)),
                ('sunday', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('enable', models.BooleanField(default=False, help_text='if enable=True, the scheduler should be creating Contests for this schedule!')),
                ('category', models.ForeignKey(to='schedule.Category')),
                ('site_sport', models.ForeignKey(to='sports.SiteSport')),
            ],
        ),
        migrations.CreateModel(
            name='ScheduledTemplateContest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('start_time', models.TimeField(help_text='the time the scheduled contest should begin. ie: 19:00:00 ... (thats 7:00 PM)')),
                ('duration_minutes', models.IntegerField(default=0, help_text='so we can calculate the end time. end_time = (start_time + timedelta(minutes=duration_minutes)).')),
                ('interval', models.ForeignKey(to='schedule.Interval')),
                ('schedule', models.ForeignKey(to='schedule.Schedule', help_text='the main schedule this template is associated with')),
            ],
        ),
        migrations.CreateModel(
            name='TemplateContest',
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
        migrations.AddField(
            model_name='scheduledtemplatecontest',
            name='template_contest',
            field=models.ForeignKey(to='schedule.TemplateContest', help_text='this is the contest the scheduler will create when the time comes'),
        ),
        migrations.AlterUniqueTogether(
            name='scheduledtemplatecontest',
            unique_together=set([('schedule', 'template_contest', 'start_time', 'duration_minutes')]),
        ),
        migrations.AlterUniqueTogether(
            name='schedule',
            unique_together=set([('site_sport', 'category')]),
        ),
    ]
