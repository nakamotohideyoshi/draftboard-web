# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataden', '0002_livestatscacheconfig_trigger'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='trigger',
            unique_together=set([('db', 'collection', 'parent_api')]),
        ),
    ]
