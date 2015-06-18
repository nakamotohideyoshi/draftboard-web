# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prize', '0006_auto_20150617_1507'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CashAmount',
        ),
    ]
