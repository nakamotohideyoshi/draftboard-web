# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0003_auto_20151018_0107'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduledtemplatecontest',
            name='multiplier',
            field=models.IntegerField(help_text='the number of copies of this contest to create (ie: you might want ten 1v1 contests of the same type active at the same time)', default=1),
        ),
    ]
