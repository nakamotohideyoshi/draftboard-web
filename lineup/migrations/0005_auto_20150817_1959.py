# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lineup', '0004_auto_20150724_1301'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lineup',
            old_name='draftgroup',
            new_name='draft_group',
        ),
    ]
