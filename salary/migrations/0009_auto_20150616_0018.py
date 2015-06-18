# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0008_auto_20150616_0016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salary',
            name='player_type',
            field=models.ForeignKey(to='contenttypes.ContentType'),
        ),
    ]
