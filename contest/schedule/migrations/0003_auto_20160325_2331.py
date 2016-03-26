# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_auto_20160209_2241'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='templatecontest',
            name='status',
        ),
        migrations.AlterField(
            model_name='templatecontest',
            name='site_sport',
            field=models.ForeignKey(to='sports.SiteSport', related_name='schedule_templatecontest_site_sport'),
        ),
    ]
