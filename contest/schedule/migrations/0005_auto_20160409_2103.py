# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0004_auto_20160409_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='templatecontest',
            name='name',
            field=models.CharField(verbose_name='Name', help_text='frontfacing name', default='', max_length=64),
        ),
    ]
