# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prize', '0003_prizestructure_buyin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rank',
            name='prize_structure',
            field=models.ForeignKey(to='prize.PrizeStructure', related_name='ranks'),
        ),
    ]
