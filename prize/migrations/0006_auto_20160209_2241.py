# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prize', '0005_auto_20150902_1507'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='prizestructure',
            options={'verbose_name': 'Prize Structure', 'verbose_name_plural': 'Prize Structure'},
        ),
        migrations.AlterModelOptions(
            name='rank',
            options={'verbose_name': 'Payout Structure', 'verbose_name_plural': 'Payout Structure'},
        ),
    ]
