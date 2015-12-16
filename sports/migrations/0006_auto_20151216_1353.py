# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0005_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='TsxContent',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('srid', models.CharField(help_text='use the right part url for the actual feed after splitting on "tsx". heres an example srid: "/news/2015/12/15/all.xml"', max_length=256)),
                ('sport', models.CharField(max_length=32)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='tsxcontent',
            unique_together=set([('srid', 'sport')]),
        ),
    ]
