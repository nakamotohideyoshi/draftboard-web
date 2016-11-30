# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0004_historyentry'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='completedcontest',
            options={'verbose_name': 'Completed', 'verbose_name_plural': 'Completed'},
        ),
        migrations.AlterModelOptions(
            name='contest',
            options={'verbose_name': 'All Contests', 'verbose_name_plural': 'All Contests'},
        ),
        migrations.AlterModelOptions(
            name='entry',
            options={'verbose_name': 'Entry', 'verbose_name_plural': 'Entries'},
        ),
        migrations.AlterModelOptions(
            name='historycontest',
            options={'verbose_name': 'History', 'verbose_name_plural': 'History'},
        ),
        migrations.AlterModelOptions(
            name='livecontest',
            options={'verbose_name': 'Live', 'verbose_name_plural': 'Live'},
        ),
        migrations.AlterModelOptions(
            name='upcomingcontest',
            options={'verbose_name': 'Upcoming', 'verbose_name_plural': 'Upcoming'},
        ),
        migrations.AddField(
            model_name='entry',
            name='final_rank',
            field=models.IntegerField(help_text='the rank of the entry after the contest has been paid out', default=-1),
        ),
        migrations.AlterField(
            model_name='contest',
            name='end',
            field=models.DateTimeField(verbose_name='Cutoff Time', help_text='forces the end time of the contest (will override "Ends tonight" checkbox!!', blank=True),
        ),
        migrations.AlterField(
            model_name='contest',
            name='start',
            field=models.DateTimeField(verbose_name='Start Time', help_text='the start should coincide with the start of a real-life game.'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='contest',
            field=models.ForeignKey(related_name='contests', to='contest.Contest'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='lineup',
            field=models.ForeignKey(null=True, to='lineup.Lineup', related_name='entries'),
        ),
    ]
