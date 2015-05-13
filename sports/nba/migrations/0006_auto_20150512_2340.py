# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0005_auto_20150510_0251'),
    ]

    operations = [
        migrations.RenameField(
            model_name='playerstats',
            old_name='fouls',
            new_name='tech_fouls',
        ),
        migrations.AddField(
            model_name='playerstats',
            name='assists',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='assists_turnover_ratio',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='blocked_att',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='blocks',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='defensive_rebounds',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='field_goals_att',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='field_goals_made',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='field_goals_pct',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='flagrant_fouls',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='free_throws_att',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='free_throws_made',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='free_throws_pct',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='offensive_rebounds',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='personal_fouls',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='rebounds',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='steals',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='three_points_att',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='three_points_made',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='three_points_pct',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='turnovers',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='two_points_att',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='two_points_made',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='two_points_pct',
            field=models.FloatField(default=0.0),
        ),
    ]
