# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prize', '0002_createticketprizestructure_generatorsettings_prizestructure_rank'),
    ]

    operations = [
        migrations.AddField(
            model_name='prizestructure',
            name='buyin',
            field=models.DecimalField(max_digits=7, default=0, decimal_places=2),
        ),
    ]
