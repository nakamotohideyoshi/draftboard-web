# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('draftgroup', '0002_auto_20150625_1824'),
    ]

    operations = [
        migrations.RenameField(
            model_name='draftgroup',
            old_name='start_dt',
            new_name='start',
        ),
        migrations.RemoveField(
            model_name='draftgroup',
            name='start_ts',
        ),
        migrations.AddField(
            model_name='draftgroup',
            name='end',
            field=models.DateTimeField(help_text='the DateTime on, or after which no players from games are included', default=None),
            preserve_default=False,
        ),
    ]
