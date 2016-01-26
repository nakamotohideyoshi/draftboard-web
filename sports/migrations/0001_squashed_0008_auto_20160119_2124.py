# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from ..classes import SiteSportManager

# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# sports.migrations.0002_sitesport
def load_initial_data(apps, schema_editor):
    """
    Loads the initial WithdrawStatus(s). This function will be passed to 'migrations.RunPython' which supplies the arguments.

    :param apps:
    :param schema_editor:
    :return:
    """
    #
    # get the model by name
    SiteSport = apps.get_model('sports', 'SiteSport')
    for sport in SiteSportManager.get_sport_names():   # ie: iterate SiteSportManager.SPORTS
        model = SiteSport()
        model.name = sport
        model.save()

class Migration(migrations.Migration):

    replaces = [('sports', '0001_initial'), ('sports', '0002_sitesport'), ('sports', '0003_auto_20150528_2321'), ('sports', '0004_auto_20150612_2112'), ('sports', '0004_auto_20150603_2146'), ('sports', '0005_merge'), ('sports', '0006_auto_20151216_1353'), ('sports', '0007_sitesport_current_season'), ('sports', '0008_auto_20160119_2124')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSport',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.RunPython(
            load_initial_data,
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=128)),
                ('site_sport', models.ForeignKey(to='sports.SiteSport')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='position',
            unique_together=set([('name', 'site_sport')]),
        ),
        migrations.AlterField(
            model_name='sitesport',
            name='name',
            field=models.CharField(max_length=128, unique=True),
        ),
        migrations.AlterField(
            model_name='sitesport',
            name='name',
            field=models.CharField(max_length=128, unique=True),
        ),
        migrations.CreateModel(
            name='TsxContent',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('srid', models.CharField(max_length=256, help_text='use the right part url for the actual feed after splitting on "tsx". heres an example srid: "/news/2015/12/15/all.xml"')),
                ('sport', models.CharField(max_length=32)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='tsxcontent',
            unique_together=set([('srid', 'sport')]),
        ),
        migrations.AddField(
            model_name='sitesport',
            name='current_season',
            field=models.IntegerField(default=2015),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sitesport',
            name='current_season',
            field=models.IntegerField(help_text='year this sports current season began in. example: for the nba 2015-16 season, current_season should be set to: 2015'),
        ),
        migrations.AlterField(
            model_name='sitesport',
            name='current_season',
            field=models.IntegerField(help_text='year this sports current season began in. example: for the nba 2015-16 season, current_season should be set to: 2015', null=True),
        ),
    ]
