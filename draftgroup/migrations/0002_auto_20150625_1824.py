# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0002_auto_20150624_1538'),
        ('draftgroup', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DraftGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('start_dt', models.DateTimeField(help_text='the DateTime for the earliest possible players in the group.')),
                ('start_ts', models.IntegerField(default=0, help_text='save() converts start_dt into a unix timestamp and sets the value to this field')),
                ('salary_pool', models.ForeignKey(verbose_name='the Salary Pool is the set of active player salaries for a sport', to='salary.Pool')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('draft_group', models.ForeignKey(verbose_name='the DraftGroup this player is a member of', to='draftgroup.DraftGroup')),
                ('salary', models.ForeignKey(verbose_name='points to the player salary object, which has fantasy salary information', to='salary.Salary')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='player',
            unique_together=set([('draft_group', 'salary')]),
        ),
    ]
