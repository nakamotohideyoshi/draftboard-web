# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0009_auto_20150616_0018'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pool',
            options={'verbose_name': 'Player Pool', 'ordering': ('-active', 'site_sport', '-created')},
        ),
        migrations.AlterModelOptions(
            name='salary',
            options={'verbose_name': 'Player', 'ordering': ('primary_roster', '-amount')},
        ),
        migrations.AlterModelOptions(
            name='salaryconfig',
            options={'verbose_name': 'Algorithm Configuration'},
        ),
        migrations.AlterField(
            model_name='salaryconfig',
            name='trailing_games',
            field=models.PositiveIntegerField(help_text='The total number of games considered in the trailing weight section.', verbose_name='Trailing Games'),
        ),
        migrations.AlterField(
            model_name='trailinggameweight',
            name='weight',
            field=models.FloatField(help_text='Multiplier'),
        ),
    ]
