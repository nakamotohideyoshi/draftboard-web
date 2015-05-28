# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0002_sitesport'),
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=128)),
                ('site_sport', models.ForeignKey(to='sports.SiteSport')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='position',
            unique_together=set([('name', 'site_sport')]),
        ),
    ]
