# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lobby', '0004_auto_20160108_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contestbanner',
            name='contest',
            field=models.ForeignKey(blank=True, to='contest.Contest', null=True),
        ),
    ]
