# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prize', '0002_prizestructure'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActualCash',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('tied', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActualTicket',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('tied', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Cash',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('rank', models.IntegerField(default=0)),
                ('value', models.FloatField(default=0)),
                ('prize_structure', models.ForeignKey(to='prize.PrizeStructure')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('rank', models.IntegerField(default=0)),
                ('value', models.FloatField(default=0)),
                ('prize_structure', models.ForeignKey(to='prize.PrizeStructure')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='ticket',
            unique_together=set([('prize_structure', 'rank')]),
        ),
        migrations.AlterUniqueTogether(
            name='cash',
            unique_together=set([('prize_structure', 'rank')]),
        ),
    ]
