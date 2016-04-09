# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prize', '0006_auto_20160209_2241'),
        ('sports', '0001_squashed_0008_auto_20160119_2124'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('schedule', '0003_auto_20160325_2331'),
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('dfsday_start', models.DateTimeField()),
                ('dfsday_end', models.DateTimeField()),
                ('cutoff_time', models.TimeField()),
                ('cutoff', models.DateTimeField(help_text='the UTC datetime object for the cutoff_time', blank=True)),
                ('site_sport', models.ForeignKey(to='sports.SiteSport')),
            ],
        ),
        migrations.CreateModel(
            name='BlockGame',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(default='', max_length=256)),
                ('srid', models.CharField(max_length=128)),
                ('game_id', models.PositiveIntegerField()),
                ('block', models.ForeignKey(to='schedule.Block')),
                ('game_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='BlockPrizeStructure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('block', models.ForeignKey(to='schedule.Block')),
                ('prize_structure', models.ForeignKey(to='prize.PrizeStructure')),
            ],
        ),
        migrations.CreateModel(
            name='DefaultPrizeStructure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('prize_structure', models.ForeignKey(to='prize.PrizeStructure')),
                ('site_sport', models.ForeignKey(to='sports.SiteSport')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('enabled', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='UpcomingBlock',
            fields=[
            ],
            options={
                'verbose_name': 'Schedule',
                'proxy': True,
            },
            bases=('schedule.block',),
        ),
        migrations.AlterUniqueTogether(
            name='defaultprizestructure',
            unique_together=set([('site_sport', 'prize_structure')]),
        ),
        migrations.AlterUniqueTogether(
            name='blockprizestructure',
            unique_together=set([('block', 'prize_structure')]),
        ),
        migrations.AlterUniqueTogether(
            name='blockgame',
            unique_together=set([('block', 'srid')]),
        ),
        migrations.AlterUniqueTogether(
            name='block',
            unique_together=set([('site_sport', 'dfsday_start', 'dfsday_end', 'cutoff_time')]),
        ),
    ]
