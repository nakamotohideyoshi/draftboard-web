# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payout', '0001_squashed_0003_fpp_rake'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payout',
            name='entry',
            field=models.OneToOneField(related_name='payout', to='contest.Entry'),
        ),
    ]
