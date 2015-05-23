# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('nhl', '0004_pbp_pbpdescription'),
    ]

    operations = [
        migrations.AddField(
            model_name='pbpdescription',
            name='portion_id',
            field=models.PositiveIntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pbpdescription',
            name='portion_type',
            field=models.ForeignKey(default=None, to='contenttypes.ContentType', related_name='nhl_pbpdescription_pbpdesc_portion'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pbpdescription',
            name='pbp_type',
            field=models.ForeignKey(related_name='nhl_pbpdescription_pbpdesc_pbp', to='contenttypes.ContentType'),
        ),
    ]
