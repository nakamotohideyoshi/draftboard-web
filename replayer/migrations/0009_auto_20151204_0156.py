# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('replayer', '0008_auto_20151204_0133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timemachine',
            name='target',
            field=models.DateTimeField(help_text='SET THE STOP TARGET FOR PLAY-TO-TARGET mode. the time you want to start at in the replay. must be within the start and end of the recorded stats', null=True, blank=True),
        ),
    ]
