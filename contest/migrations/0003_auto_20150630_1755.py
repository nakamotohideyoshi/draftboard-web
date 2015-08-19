# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0002_contest_entry'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='end',
            field=models.DateTimeField(default=None, verbose_name='the after which real-life games will not be included in this contest', help_text='this field is overridden if the TodayOnly box is enabled'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contest',
            name='start',
            field=models.DateTimeField(default=None, verbose_name='The time this contest will start!', help_text='the start should coincide with the start of a real-life game.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contest',
            name='today_only',
            field=models.BooleanField(default=True),
        ),
    ]
