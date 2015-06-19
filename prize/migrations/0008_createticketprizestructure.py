# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prize', '0007_delete_cashamount'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreateTicketPrizeStructure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('ticket_value', models.FloatField(verbose_name='Ticket Value', default=0.0)),
                ('num_prizes', models.IntegerField(verbose_name='The Number of Total Tickets', default=0)),
            ],
        ),
    ]
