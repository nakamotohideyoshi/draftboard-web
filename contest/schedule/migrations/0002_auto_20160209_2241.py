# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_squashed_0005_auto_20151201_1551'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Time Slot'},
        ),
        migrations.AlterModelOptions(
            name='scheduledtemplatecontest',
            options={'verbose_name': 'Master Schedule'},
        ),
        migrations.AlterModelOptions(
            name='templatecontest',
            options={'verbose_name': 'Contest Template'},
        ),
        migrations.AlterField(
            model_name='templatecontest',
            name='end',
            field=models.DateTimeField(verbose_name='Cutoff Time', help_text='forces the end time of the contest (will override "Ends tonight" checkbox!!', blank=True),
        ),
        migrations.AlterField(
            model_name='templatecontest',
            name='start',
            field=models.DateTimeField(verbose_name='Start Time', help_text='the start should coincide with the start of a real-life game.'),
        ),
    ]
