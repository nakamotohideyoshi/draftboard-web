# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0006_auto_20151216_1353'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('nba', '0005_auto_20151016_1942'),
    ]

    operations = [
        migrations.CreateModel(
            name='TsxInjury',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('srid', models.CharField(help_text='the sportradar global id for the item', max_length=64)),
                ('pcid', models.CharField(help_text='the providers content id for this item', max_length=64)),
                ('content_created', models.DateTimeField()),
                ('content_modified', models.DateTimeField()),
                ('content_published', models.DateTimeField()),
                ('title', models.CharField(max_length=256)),
                ('byline', models.CharField(max_length=256)),
                ('dateline', models.CharField(max_length=32)),
                ('credit', models.CharField(max_length=128)),
                ('content', models.CharField(max_length=8192)),
                ('tsxcontent', models.ForeignKey(related_name='nba_tsxinjury_tsxcontent', to='sports.TsxContent')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TsxNews',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('srid', models.CharField(help_text='the sportradar global id for the item', max_length=64)),
                ('pcid', models.CharField(help_text='the providers content id for this item', max_length=64)),
                ('content_created', models.DateTimeField()),
                ('content_modified', models.DateTimeField()),
                ('content_published', models.DateTimeField()),
                ('title', models.CharField(max_length=256)),
                ('byline', models.CharField(max_length=256)),
                ('dateline', models.CharField(max_length=32)),
                ('credit', models.CharField(max_length=128)),
                ('content', models.CharField(max_length=8192)),
                ('tsxcontent', models.ForeignKey(related_name='nba_tsxnews_tsxcontent', to='sports.TsxContent')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TsxPlayer',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('sportsdataid', models.CharField(max_length=64)),
                ('sportradarid', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=128)),
                ('tsxitem_id', models.PositiveIntegerField()),
                ('tsxitem_type', models.ForeignKey(related_name='nba_tsxplayer_tsxitem_tsxitemref', to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TsxTeam',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('sportsdataid', models.CharField(max_length=64)),
                ('sportradarid', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=128)),
                ('tsxitem_id', models.PositiveIntegerField()),
                ('tsxitem_type', models.ForeignKey(related_name='nba_tsxteam_tsxitem_tsxitemref', to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TsxTransaction',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('srid', models.CharField(help_text='the sportradar global id for the item', max_length=64)),
                ('pcid', models.CharField(help_text='the providers content id for this item', max_length=64)),
                ('content_created', models.DateTimeField()),
                ('content_modified', models.DateTimeField()),
                ('content_published', models.DateTimeField()),
                ('title', models.CharField(max_length=256)),
                ('byline', models.CharField(max_length=256)),
                ('dateline', models.CharField(max_length=32)),
                ('credit', models.CharField(max_length=128)),
                ('content', models.CharField(max_length=8192)),
                ('tsxcontent', models.ForeignKey(related_name='nba_tsxtransaction_tsxcontent', to='sports.TsxContent')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
