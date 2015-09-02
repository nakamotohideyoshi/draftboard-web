# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0016_auto_20150901_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='doubleup',
            field=models.BooleanField(help_text='whether this contest has a double-up style prize structure', default=False),
        ),
    ]
