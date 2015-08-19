# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0005_merge'),
        ('contest', '0004_auto_20150630_1956'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='site_sport',
            field=models.ForeignKey(default=1, to='sports.SiteSport'),
            preserve_default=False,
        ),
    ]
