# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prize', '0009_auto_20150618_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='createticketprizestructure',
            name='num_prizes',
            field=models.IntegerField(help_text='The number of tickets this prize structure should pay out.', default=0, verbose_name='The Number of Total Tickets'),
        ),
        migrations.AlterField(
            model_name='createticketprizestructure',
            name='ticket_value',
            field=models.FloatField(help_text='Enter the value of a valid ticket.', default=0.0, verbose_name='Ticket Value'),
        ),
    ]
