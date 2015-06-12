# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0005_auto_20150611_2200'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pool',
            options={'ordering': ('-active', 'site_sport')},
        ),
    ]
