# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('sports', '0005_merge'),
        ('roster', '0002_auto_20150529_0216'),
        ('salary', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pool',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Player Pool',
                'ordering': ('-active', 'site_sport', '-created'),
            },
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('amount', models.PositiveIntegerField()),
                ('flagged', models.BooleanField(default=False)),
                ('fppg', models.FloatField(default=0.0)),
                ('player_id', models.PositiveIntegerField()),
                ('player_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('pool', models.ForeignKey(to='salary.Pool')),
                ('primary_roster', models.ForeignKey(to='roster.RosterSpot')),
            ],
            options={
                'verbose_name': 'Player',
                'ordering': ('primary_roster', '-amount'),
            },
        ),
        migrations.CreateModel(
            name='SalaryConfig',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=64, verbose_name='Name', default='', help_text='The plain text name of the configuration')),
                ('days_since_last_game_flag', models.PositiveIntegerField(verbose_name='Days Since Last Game Flag', help_text='Flag the player if X days since last game played')),
                ('min_games_flag', models.PositiveIntegerField(verbose_name='Min Games Flag', help_text='Flag the player if X games have not been played')),
                ('min_player_salary', models.PositiveIntegerField(verbose_name='Min Player Salary', help_text='The minimum salary a player can be worth.')),
                ('max_team_salary', models.PositiveIntegerField(verbose_name='Team Salary', help_text='The total team salary for drafting')),
                ('min_avg_fppg_allowed_for_avg_calc', models.FloatField(verbose_name='Min FPPG Allowed for Avg Calc', default=0.0, help_text="The minimum fppg allowed for a player's stats to be used to calculate position averages.")),
                ('trailing_games', models.PositiveIntegerField(verbose_name='Trailing Games', help_text='The total number of games considered in the trailing weight section.')),
            ],
            options={
                'verbose_name': 'Algorithm Configuration',
            },
        ),
        migrations.CreateModel(
            name='TrailingGameWeight',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('through', models.PositiveIntegerField()),
                ('weight', models.FloatField(help_text='Multiplier')),
                ('salary', models.ForeignKey(to='salary.SalaryConfig', related_name='trailing_game_weights')),
            ],
            options={
                'ordering': ('through',),
            },
        ),
        migrations.AddField(
            model_name='pool',
            name='salary_config',
            field=models.ForeignKey(to='salary.SalaryConfig'),
        ),
        migrations.AddField(
            model_name='pool',
            name='site_sport',
            field=models.ForeignKey(to='sports.SiteSport'),
        ),
        migrations.AlterUniqueTogether(
            name='trailinggameweight',
            unique_together=set([('salary', 'through')]),
        ),
    ]
