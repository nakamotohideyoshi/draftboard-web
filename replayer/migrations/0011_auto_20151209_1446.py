# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('replayer', '0010_auto_20151208_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timemachine',
            name='replay',
            field=models.CharField(help_text='the name of the replay (a postgres dump) on s3', max_length=255, default=''),
        ),
    ]
