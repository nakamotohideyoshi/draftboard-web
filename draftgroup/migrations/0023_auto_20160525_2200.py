# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('draftgroup', '0022_auto_20160525_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameupdate',
            name='update_id',
            field=models.CharField(null=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='playerupdate',
            name='update_id',
            field=models.CharField(null=True, max_length=128),
        ),
    ]
