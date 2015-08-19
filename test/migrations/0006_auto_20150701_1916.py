# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test', '0005_auto_20150701_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerchild',
            name='team',
            field=models.ForeignKey(null=True, to='test.TeamChild'),
        ),
    ]
