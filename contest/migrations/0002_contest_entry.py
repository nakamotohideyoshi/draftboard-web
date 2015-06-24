# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lineup', '0002_lineup'),
        ('prize', '0002_createticketprizestructure_generatorsettings_prizestructure_rank'),
        ('contest', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(default='', verbose_name='Name', max_length=64, help_text='The plain text name of the Contest')),
                ('status', models.CharField(default='SCH', choices=[('SCH', 'Scheduled'), ('INP', 'In Progress'), ('CMP', 'Completed'), ('CLS', 'Closed')], max_length=3)),
                ('prize_structure', models.ForeignKey(to='prize.PrizeStructure')),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('contest', models.ForeignKey(to='contest.Contest')),
                ('lineup', models.ForeignKey(to='lineup.Lineup')),
            ],
        ),
    ]
