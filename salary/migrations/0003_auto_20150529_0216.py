# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0003_auto_20150528_2321'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('salary', '0002_auto_20150523_0204'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pool',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('amount', models.PositiveIntegerField()),
                ('flagged', models.BooleanField(default=False)),
                ('player_id', models.PositiveIntegerField()),
                ('player_type', models.ForeignKey(related_name='salary_salary_sport_player', to='contenttypes.ContentType')),
                ('pool', models.ForeignKey(to='salary.Pool')),
            ],
        ),
        migrations.AlterField(
            model_name='salaryconfig',
            name='days_since_last_game_flag',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='salaryconfig',
            name='max_team_salary',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='salaryconfig',
            name='min_games_flag',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='salaryconfig',
            name='min_player_salary',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='salaryconfig',
            name='trailing_games',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='trailinggameweight',
            name='through',
            field=models.PositiveIntegerField(),
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
    ]
