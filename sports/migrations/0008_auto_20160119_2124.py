# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0007_sitesport_current_season'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesport',
            name='current_season',
            field=models.IntegerField(help_text='year this sports current season began in. example: for the nba 2015-16 season, current_season should be set to: 2015'),
        ),
    ]
