# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test', '0003_teamchild'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerchild',
            name='team',
            field=models.ForeignKey(default=1, to='test.TeamChild'),
            preserve_default=False,
        ),
    ]
