# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0013_auto_20150723_1525'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='gpp',
            field=models.BooleanField(default=False, help_text='a gpp Contest will not be cancelled if it does not fill'),
        ),
        migrations.AddField(
            model_name='contest',
            name='respawn',
            field=models.BooleanField(default=False, help_text='indicates whether a new identical Contest should be created when this one fills up'),
        ),
    ]
