# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalaryConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('trailing_games', models.IntegerField()),
                ('days_since_last_game_flag', models.IntegerField()),
                ('min_games_flag', models.IntegerField()),
                ('min_player_salary', models.IntegerField()),
                ('max_team_salary', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TrailingGameWeight',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('through', models.IntegerField()),
                ('weight', models.FloatField()),
                ('salary', models.ForeignKey(to='salary.SalaryConfig')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='trailinggameweight',
            unique_together=set([('salary', 'through')]),
        ),
    ]
