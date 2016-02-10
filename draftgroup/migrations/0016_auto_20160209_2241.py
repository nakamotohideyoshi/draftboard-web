# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('draftgroup', '0015_auto_20151205_2241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='draftgroup',
            name='category',
            field=models.CharField(help_text='currently unused - originally intended as a grouping like "Early", "Late", or "Turbo"', null=True, max_length=32),
        ),
    ]
