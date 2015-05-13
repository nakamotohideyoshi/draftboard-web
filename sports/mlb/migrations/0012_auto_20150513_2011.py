# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mlb', '0011_auto_20150513_1955'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='bat_hand',
            field=models.CharField(max_length=8, default=''),
        ),
        migrations.AddField(
            model_name='player',
            name='birthcity',
            field=models.CharField(max_length=64, default=''),
        ),
        migrations.AddField(
            model_name='player',
            name='birthcountry',
            field=models.CharField(max_length=64, default=''),
        ),
        migrations.AddField(
            model_name='player',
            name='birthdate',
            field=models.CharField(max_length=64, default=''),
        ),
        migrations.AddField(
            model_name='player',
            name='height',
            field=models.FloatField(help_text='inches', default=0.0),
        ),
        migrations.AddField(
            model_name='player',
            name='jersey_number',
            field=models.CharField(max_length=64, default=''),
        ),
        migrations.AddField(
            model_name='player',
            name='position',
            field=models.CharField(max_length=64, default=''),
        ),
        migrations.AddField(
            model_name='player',
            name='preferred_name',
            field=models.CharField(max_length=64, default=''),
        ),
        migrations.AddField(
            model_name='player',
            name='primary_position',
            field=models.CharField(max_length=64, default=''),
        ),
        migrations.AddField(
            model_name='player',
            name='pro_debut',
            field=models.CharField(max_length=64, default=''),
        ),
        migrations.AddField(
            model_name='player',
            name='srid_team',
            field=models.CharField(max_length=64, default=''),
        ),
        migrations.AddField(
            model_name='player',
            name='status',
            field=models.CharField(max_length=64, help_text='roster status - ie: "A" means they are ON the roster. Not particularly active as in not-injured!', default=''),
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(to='mlb.Team', default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='throw_hand',
            field=models.CharField(max_length=8, default=''),
        ),
        migrations.AddField(
            model_name='player',
            name='weight',
            field=models.FloatField(help_text='lbs', default=0.0),
        ),
    ]
