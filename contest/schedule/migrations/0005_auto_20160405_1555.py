# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0004_auto_20160405_1548'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SportDefaultPrizeStructure',
            new_name='DefaultPrizeStructure',
        ),
    ]
