# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('draftgroup', '0007_auto_20150630_2303'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='salary',
            new_name='salary_player',
        ),
        migrations.AlterUniqueTogether(
            name='player',
            unique_together=set([('draft_group', 'salary_player')]),
        ),
    ]
