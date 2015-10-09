# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('draftgroup', '0013_auto_20150318_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='draftgroup',
            name='num_games',
            field=models.IntegerField(default=0, help_text='the number of live games this draft group spans'),
        ),
    ]
