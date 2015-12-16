# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('sports', '0006_auto_20151216_1353'),
        ('nhl', '0004_game_prev_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='TsxInjury',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('srid', models.CharField(max_length=64, help_text='the sportradar global id for the item')),
                ('pcid', models.CharField(max_length=64, help_text='the providers content id for this item')),
                ('content_created', models.DateTimeField()),
                ('content_modified', models.DateTimeField()),
                ('content_published', models.DateTimeField()),
                ('title', models.CharField(max_length=256)),
                ('byline', models.CharField(max_length=256)),
                ('dateline', models.CharField(max_length=32)),
                ('credit', models.CharField(max_length=128)),
                ('content', models.CharField(max_length=8192)),
                ('tsxcontent', models.ForeignKey(related_name='nhl_tsxinjury_tsxcontent', to='sports.TsxContent')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TsxNews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('srid', models.CharField(max_length=64, help_text='the sportradar global id for the item')),
                ('pcid', models.CharField(max_length=64, help_text='the providers content id for this item')),
                ('content_created', models.DateTimeField()),
                ('content_modified', models.DateTimeField()),
                ('content_published', models.DateTimeField()),
                ('title', models.CharField(max_length=256)),
                ('byline', models.CharField(max_length=256)),
                ('dateline', models.CharField(max_length=32)),
                ('credit', models.CharField(max_length=128)),
                ('content', models.CharField(max_length=8192)),
                ('tsxcontent', models.ForeignKey(related_name='nhl_tsxnews_tsxcontent', to='sports.TsxContent')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TsxPlayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sportsdataid', models.CharField(max_length=64)),
                ('sportradarid', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=128)),
                ('tsxitem_id', models.PositiveIntegerField()),
                ('tsxitem_type', models.ForeignKey(related_name='nhl_tsxplayer_tsxitem_tsxitemref', to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TsxTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sportsdataid', models.CharField(max_length=64)),
                ('sportradarid', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=128)),
                ('tsxitem_id', models.PositiveIntegerField()),
                ('tsxitem_type', models.ForeignKey(related_name='nhl_tsxteam_tsxitem_tsxitemref', to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TsxTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('srid', models.CharField(max_length=64, help_text='the sportradar global id for the item')),
                ('pcid', models.CharField(max_length=64, help_text='the providers content id for this item')),
                ('content_created', models.DateTimeField()),
                ('content_modified', models.DateTimeField()),
                ('content_published', models.DateTimeField()),
                ('title', models.CharField(max_length=256)),
                ('byline', models.CharField(max_length=256)),
                ('dateline', models.CharField(max_length=32)),
                ('credit', models.CharField(max_length=128)),
                ('content', models.CharField(max_length=8192)),
                ('tsxcontent', models.ForeignKey(related_name='nhl_tsxtransaction_tsxcontent', to='sports.TsxContent')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
