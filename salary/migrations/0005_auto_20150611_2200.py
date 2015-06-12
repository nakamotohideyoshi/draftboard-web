# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0004_salaryconfig_min_avg_fppg_allowed_for_avg_calc'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='trailinggameweight',
            options={'ordering': ('through',)},
        ),
        migrations.AddField(
            model_name='salaryconfig',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 6, 11, 22, 0, 59, 407715, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='salaryconfig',
            name='name',
            field=models.CharField(verbose_name='Name', help_text='The plain text name of the configuration', max_length=64, default=''),
        ),
        migrations.AlterField(
            model_name='salaryconfig',
            name='days_since_last_game_flag',
            field=models.PositiveIntegerField(verbose_name='Days Since Last Game Flag', help_text='Flag the player if X days since last game played'),
        ),
        migrations.AlterField(
            model_name='salaryconfig',
            name='max_team_salary',
            field=models.PositiveIntegerField(verbose_name='Team Salary', help_text='The total team salary for drafting'),
        ),
        migrations.AlterField(
            model_name='salaryconfig',
            name='min_avg_fppg_allowed_for_avg_calc',
            field=models.FloatField(verbose_name='Min FPPG Allowed for Avg Calc', help_text="The minimum fppg allowed for a player's stats to be used to calculate position averages.", default=0.0),
        ),
        migrations.AlterField(
            model_name='salaryconfig',
            name='min_games_flag',
            field=models.PositiveIntegerField(verbose_name='Min Games Flag', help_text='Flag the player if X games have not been played'),
        ),
        migrations.AlterField(
            model_name='salaryconfig',
            name='min_player_salary',
            field=models.PositiveIntegerField(verbose_name='Min Player Salary', help_text='The minimum salary a player can be worth.'),
        ),
        migrations.AlterField(
            model_name='salaryconfig',
            name='trailing_games',
            field=models.PositiveIntegerField(verbose_name='Trailing Games', help_text='The number of games to trail.'),
        ),
        migrations.AlterField(
            model_name='trailinggameweight',
            name='salary',
            field=models.ForeignKey(to='salary.SalaryConfig', related_name='trailing_game_weights'),
        ),
    ]
