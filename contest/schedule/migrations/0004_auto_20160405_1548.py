# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0001_squashed_0008_auto_20160119_2124'),
        ('prize', '0006_auto_20160209_2241'),
        ('schedule', '0003_auto_20160325_2331'),
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('start', models.DateTimeField()),
                ('site_sport', models.ForeignKey(to='sports.SiteSport')),
            ],
        ),
        migrations.CreateModel(
            name='BlockPrizeStructure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('block', models.ForeignKey(to='schedule.Block')),
                ('prize_structure', models.ForeignKey(to='prize.PrizeStructure')),
            ],
        ),
        migrations.CreateModel(
            name='SportDefaultPrizeStructure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('prize_structure', models.ForeignKey(to='prize.PrizeStructure')),
                ('site_sport', models.ForeignKey(to='sports.SiteSport')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='sportdefaultprizestructure',
            unique_together=set([('site_sport', 'prize_structure')]),
        ),
        migrations.AlterUniqueTogether(
            name='blockprizestructure',
            unique_together=set([('block', 'prize_structure')]),
        ),
        migrations.AlterUniqueTogether(
            name='block',
            unique_together=set([('site_sport', 'start')]),
        ),
    ]
