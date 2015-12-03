# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('replayer', '0003_timemachine'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timemachine',
            name='replay',
            field=models.FilePathField(path='/vagrant/mysite/smugglin'),
        ),
    ]
