# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0019_currentcontest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='current_entries',
            field=models.PositiveIntegerField(help_text='The current # of entries in the contest', default=0),
        ),
        migrations.AlterField(
            model_name='contest',
            name='entries',
            field=models.PositiveIntegerField(help_text='CONTEST limit', default=2),
        ),
        migrations.AlterField(
            model_name='contest',
            name='max_entries',
            field=models.PositiveIntegerField(help_text='USER entry limit', default=1),
        ),
    ]
