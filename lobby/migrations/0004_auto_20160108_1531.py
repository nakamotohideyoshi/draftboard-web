# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lobby', '0003_auto_20160108_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contestbanner',
            name='contest',
            field=models.ForeignKey(null=True, to='contest.Contest'),
        ),
    ]
