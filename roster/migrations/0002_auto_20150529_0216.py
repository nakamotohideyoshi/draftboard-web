# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0003_auto_20150528_2321'),
        ('roster', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RosterSpot',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(help_text='the roster position spot, i.e. FLEX or WR', max_length=64, default='')),
                ('amount', models.PositiveIntegerField(help_text='the quantity of these spots allowed in a lineup for the sport.', default=0)),
                ('idx', models.PositiveIntegerField(help_text='the order the spot will be displayed to the user.', default=0)),
                ('site_sport', models.ForeignKey(to='sports.SiteSport')),
            ],
        ),
        migrations.CreateModel(
            name='RosterSpotPosition',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('is_primary', models.BooleanField(default=False)),
                ('position', models.ForeignKey(to='sports.Position')),
                ('roster_spot', models.ForeignKey(to='roster.RosterSpot')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='rosterspotposition',
            unique_together=set([('roster_spot', 'position')]),
        ),
        migrations.AlterUniqueTogether(
            name='rosterspot',
            unique_together=set([('name', 'site_sport')]),
        ),
    ]
