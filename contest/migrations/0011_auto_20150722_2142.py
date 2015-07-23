# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0010_auto_20150722_1328'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='current_entries',
            field=models.PositiveIntegerField(help_text='The number of entries submitted to the contest', default=0),
        ),
        migrations.AddField(
            model_name='contest',
            name='entries',
            field=models.PositiveIntegerField(help_text='Total spots available for the contest', default=2),
        ),
        migrations.AddField(
            model_name='contest',
            name='max_entries',
            field=models.PositiveIntegerField(help_text='The total number of entries a user can add to a contest', default=1),
        ),
    ]
