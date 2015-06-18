# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('ticket', '0002_auto_20150427_0306'),
        ('prize', '0004_auto_20150616_1948'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cash',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('rank', models.IntegerField(default=0)),
                ('prize_id', models.IntegerField()),
                ('prize_structure', models.ForeignKey(to='prize.PrizeStructure')),
                ('prize_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('value', models.FloatField(default=0)),
                ('ticket_amount', models.ForeignKey(related_name='prize_ticket_ticket_amount', to='ticket.TicketAmount')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
