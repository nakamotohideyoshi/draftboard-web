# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('mlb', '0006_gameportion'),
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
            field=models.ForeignKey(related_name='mlb_pbpdescription_pbpdesc_portion', default=None, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pbpdescription',
            name='pbp_type',
            field=models.ForeignKey(related_name='mlb_pbpdescription_pbpdesc_pbp', to='contenttypes.ContentType'),
        ),
    ]
