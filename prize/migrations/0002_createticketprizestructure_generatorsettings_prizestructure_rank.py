# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('prize', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreateTicketPrizeStructure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('ticket_value', models.FloatField(verbose_name='Ticket Value', default=0.0, help_text='Enter the value of a valid ticket.')),
                ('num_prizes', models.IntegerField(verbose_name='The Number of Total Tickets', default=0, help_text='The number of tickets this prize structure should pay out.')),
            ],
        ),
        migrations.CreateModel(
            name='GeneratorSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('buyin', models.IntegerField(default=0)),
                ('first_place', models.IntegerField(default=0)),
                ('round_payouts', models.IntegerField(default=0)),
                ('payout_spots', models.IntegerField(default=0)),
                ('prize_pool', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='PrizeStructure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=128, default='', blank=True, help_text='Use a name that will help you remember what the prize structure is for.')),
                ('generator', models.ForeignKey(null=True, to='prize.GeneratorSettings', help_text='You do not need to specify one of these. But automatically created prize pools may be associated with a generator.', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rank', models.IntegerField(default=0)),
                ('amount_id', models.IntegerField(help_text='the id of the amount_type field')),
                ('amount_type', models.ForeignKey(to='contenttypes.ContentType', help_text='MUST be a CashAmount or TicketAmount')),
                ('prize_structure', models.ForeignKey(to='prize.PrizeStructure')),
            ],
        ),
    ]
