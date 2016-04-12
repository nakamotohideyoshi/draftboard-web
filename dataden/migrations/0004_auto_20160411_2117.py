# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataden', '0003_auto_20150513_0406'),
    ]

    operations = [
        migrations.CreateModel(
            name='PbpDebug',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('url', models.CharField(null=True, max_length=2048)),
                ('game_srid', models.CharField(max_length=128)),
                ('srid', models.CharField(max_length=128)),
                ('description', models.CharField(null=True, max_length=2048)),
                ('xml_str', models.CharField(null=True, max_length=16384)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='pbpdebug',
            unique_together=set([('game_srid', 'srid')]),
        ),
    ]
