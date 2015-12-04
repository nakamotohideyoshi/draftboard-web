# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0002_contest_currentcontest_entry_historycontest_livecontest_lobbycontest_upcomingcontest'),
        ('lobby', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContestBanner',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('internal_description', models.CharField(max_length=2048, default='', help_text='PRIVATE description of what this banner is for. should not displayed on the front end')),
                ('start_time', models.DateTimeField(help_text='do not display the banner before the start time')),
                ('end_time', models.DateTimeField(help_text='all good things must come to an end. and you need to specify the time when this banner should no longer be displayed.')),
                ('image_url', models.URLField(null=True, help_text='a public link to the image for this banner')),
                ('links_to', models.URLField(null=True, help_text='if you want the banner to be clickable, then you should add a link here')),
                ('contest', models.ForeignKey(to='contest.Contest')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PromotionBanner',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('internal_description', models.CharField(max_length=2048, default='', help_text='PRIVATE description of what this banner is for. should not displayed on the front end')),
                ('start_time', models.DateTimeField(help_text='do not display the banner before the start time')),
                ('end_time', models.DateTimeField(help_text='all good things must come to an end. and you need to specify the time when this banner should no longer be displayed.')),
                ('image_url', models.URLField(null=True, help_text='a public link to the image for this banner')),
                ('links_to', models.URLField(null=True, help_text='if you want the banner to be clickable, then you should add a link here')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
