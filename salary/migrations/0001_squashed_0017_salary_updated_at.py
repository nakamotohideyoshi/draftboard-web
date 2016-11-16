# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-15 13:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('salary', '0001_initial'), ('salary', '0002_auto_20150624_1538'), ('salary', '0003_pool_generate_salary_task_id'), ('salary', '0004_auto_20160209_2241'), ('salary', '0005_auto_20160503_1415'), ('salary', '0006_salary_ownership_percentage'), ('salary', '0007_salary_amount_unadjusted'), ('salary', '0008_pool_max_percent_adjust'), ('salary', '0009_auto_20160519_1922'), ('salary', '0010_auto_20160525_1719'), ('salary', '0011_salary_avg_fppg_for_position'), ('salary', '0012_salary_num_games_included'), ('salary', '0013_auto_20160727_1807'), ('salary', '0014_auto_20161005_1526'), ('salary', '0015_auto_20161015_1456'), ('salary', '0016_auto_20161015_1537'), ('salary', '0017_salary_updated_at')]

    initial = True

    dependencies = [
        ('sports', '0001_squashed_0008_auto_20160119_2124'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('roster', '0002_auto_20150529_0216'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-active', 'site_sport', '-created'),
                'verbose_name': 'Player Pool',
            },
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('amount', models.PositiveIntegerField(verbose_name='Salary')),
                ('flagged', models.BooleanField(default=False)),
                ('fppg', models.FloatField(default=0.0, verbose_name='STATS Projection')),
                ('player_id', models.PositiveIntegerField()),
                ('player_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('pool', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salary.Pool')),
                ('primary_roster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roster.RosterSpot', verbose_name='Position')),
                ('ownership_percentage', models.FloatField(default=10.0, null=True)),
                ('amount_unadjusted', models.PositiveIntegerField(default=0, verbose_name='Salary Pre-Ownership Adjustments')),
                ('fppg_pos_weighted', models.FloatField(default=0.0, verbose_name='STATS Projection')),
                ('avg_fppg_for_position', models.FloatField(default=0.0, verbose_name='Avg Proj for Position')),
                ('num_games_included', models.IntegerField(default=0, verbose_name='Num Games Included')),
                ('sal_dk', models.FloatField(blank=True, null=True, verbose_name='DK Salary')),
                ('sal_fd', models.FloatField(blank=True, null=True, verbose_name='FD Salary')),
                ('random_adjust_amount', models.FloatField(default=0.0, help_text='the amount of ($) salary +/- applied before final rounding.')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='When was this salary last updated?', null=True)),
            ],
            options={
                'ordering': ('primary_roster', '-amount'),
                'verbose_name': 'Player',
            },
        ),
        migrations.CreateModel(
            name='SalaryConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(default='', help_text='The plain text name of the configuration', max_length=64, verbose_name='Name')),
                ('days_since_last_game_flag', models.PositiveIntegerField(help_text='Flag the player if X days since last game played', verbose_name='Days Since Last Game Flag')),
                ('min_games_flag', models.PositiveIntegerField(help_text='Flag the player if X games have not been played', verbose_name='Min Games Flag')),
                ('min_player_salary', models.PositiveIntegerField(help_text='The minimum salary a player can be worth.', verbose_name='Min Player Salary')),
                ('max_team_salary', models.PositiveIntegerField(help_text='The total team salary for drafting', verbose_name='Team Salary')),
                ('min_avg_fppg_allowed_for_avg_calc', models.FloatField(default=0.0, help_text="The minimum fppg allowed for a player's stats to be used to calculate position averages.", verbose_name='Min FPPG Allowed for Avg Calc')),
                ('trailing_games', models.PositiveIntegerField(help_text='The total number of games considered in the trailing weight section.', verbose_name='Trailing Games')),
            ],
            options={
                'verbose_name': 'Algorithm Configuration',
            },
        ),
        migrations.CreateModel(
            name='TrailingGameWeight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('through', models.PositiveIntegerField()),
                ('weight', models.FloatField(help_text='Multiplier')),
                ('salary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trailing_game_weights', to='salary.SalaryConfig')),
            ],
            options={
                'ordering': ('through',),
            },
        ),
        migrations.AddField(
            model_name='pool',
            name='salary_config',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salary.SalaryConfig'),
        ),
        migrations.AddField(
            model_name='pool',
            name='site_sport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sports.SiteSport'),
        ),
        migrations.AlterUniqueTogether(
            name='trailinggameweight',
            unique_together=set([('salary', 'through')]),
        ),
        migrations.AddField(
            model_name='pool',
            name='generate_salary_task_id',
            field=models.CharField(default=None, max_length=255, null=True, verbose_name='Generating Salary'),
        ),
        migrations.AlterModelOptions(
            name='salaryconfig',
            options={'verbose_name': 'Algorithm'},
        ),
        migrations.AddField(
            model_name='pool',
            name='high_cutoff_increment',
            field=models.FloatField(default=1.0, null=True),
        ),
        migrations.AddField(
            model_name='pool',
            name='low_cutoff_increment',
            field=models.FloatField(default=1.0, null=True),
        ),
        migrations.AddField(
            model_name='pool',
            name='ownership_threshold_high_cutoff',
            field=models.FloatField(default=30.0, null=True),
        ),
        migrations.AddField(
            model_name='pool',
            name='ownership_threshold_low_cutoff',
            field=models.FloatField(default=10.0, null=True),
        ),
        migrations.AddField(
            model_name='pool',
            name='max_percent_adjust',
            field=models.FloatField(default=10.0, help_text='the maximum percentage shift due to ownership adjustment'),
        ),
        migrations.AlterField(
            model_name='salaryconfig',
            name='min_avg_fppg_allowed_for_avg_calc',
            field=models.FloatField(default=0.0, help_text='The minimum fppg allowed for a players stats to be used to calculate position averages.', verbose_name='Min FPPG Allowed for Avg Calc'),
        ),
        migrations.AddField(
            model_name='pool',
            name='random_percent_adjust',
            field=models.FloatField(default=0.0, help_text='if this is non-zero, apply an additional shift to all salaries randomly chosen from [-X%, +X% ]. this will happen before the final rounding.'),
        ),
    ]
