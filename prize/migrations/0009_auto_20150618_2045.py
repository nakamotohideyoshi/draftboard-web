# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prize', '0008_createticketprizestructure'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prizestructure',
            name='generator',
            field=models.ForeignKey(to='prize.GeneratorSettings', null=True, blank=True, help_text='You do not need to specify one of these. But automatically created prize pools may be associated with a generator.'),
        ),
        migrations.AlterField(
            model_name='prizestructure',
            name='name',
            field=models.CharField(default='', max_length=128, help_text='Use a name that will help you remember what the prize structure is for.', blank=True),
        ),
        migrations.AlterField(
            model_name='rank',
            name='amount_id',
            field=models.IntegerField(help_text='the id of the amount_type field'),
        ),
        migrations.AlterField(
            model_name='rank',
            name='amount_type',
            field=models.ForeignKey(to='contenttypes.ContentType', help_text='MUST be a CashAmount or TicketAmount'),
        ),
    ]
