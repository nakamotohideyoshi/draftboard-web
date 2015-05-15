# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mlb', '0019_auto_20150515_0129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameboxscore',
            name='srid_away_pp',
            field=models.CharField(help_text='srid of the AWAY probable pitcher set before the game starts', null=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='gameboxscore',
            name='srid_away_sp',
            field=models.CharField(help_text='srid of the AWAY starting pitcher', null=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='gameboxscore',
            name='srid_hold',
            field=models.CharField(null=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='gameboxscore',
            name='srid_home_pp',
            field=models.CharField(help_text='srid of the HOME probable pitcher set before the game starts', null=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='gameboxscore',
            name='srid_home_sp',
            field=models.CharField(help_text='srid of the HOME starting pitcher', null=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='gameboxscore',
            name='srid_loss',
            field=models.CharField(null=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='gameboxscore',
            name='srid_save',
            field=models.CharField(null=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='gameboxscore',
            name='srid_win',
            field=models.CharField(null=True, max_length=64),
        ),
    ]
