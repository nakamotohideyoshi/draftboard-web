# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0005_merge'),
        ('contest', '0020_auto_20151017_2132'),
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('enable', models.BooleanField(help_text='if enable=True, the scheduler should be creating Contests for this schedule!', default=False)),
                ('category', models.ForeignKey(to='schedule.Category')),
                ('site_sport', models.ForeignKey(to='sports.SiteSport')),
            ],
        ),
        migrations.CreateModel(
            name='ScheduledTemplateContest',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('start_time', models.TimeField(help_text='the time the scheduled contest should begin. ie: 19:00:00 ... (thats 7:00 PM)')),
                ('duration_minutes', models.IntegerField(help_text='so we can calculate the end time. end_time = (start_time + timedelta(minutes=duration_minutes)).', default=0)),
                ('schedule', models.ForeignKey(help_text='the main schedule this template is associated with', to='schedule.Schedule')),
            ],
        ),
        migrations.CreateModel(
            name='TemplateContest',
            fields=[
                ('contest_ptr', models.OneToOneField(primary_key=True, serialize=False, to='contest.Contest', auto_created=True, parent_link=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('contest.contest',),
        ),
        migrations.AddField(
            model_name='scheduledtemplatecontest',
            name='template_contest',
            field=models.ForeignKey(help_text='this is the contest the scheduler will create when the time comes', to='schedule.TemplateContest'),
        ),
        migrations.AlterUniqueTogether(
            name='schedule',
            unique_together=set([('site_sport', 'category')]),
        ),
    ]
