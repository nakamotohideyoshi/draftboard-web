# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prize', '0005_cash_rank_ticket'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashAmount',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GeneratorSettings',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('buyin', models.IntegerField(default=0)),
                ('first_place', models.IntegerField(default=0)),
                ('round_payouts', models.IntegerField(default=0)),
                ('payout_spots', models.IntegerField(default=0)),
                ('prize_pool', models.IntegerField(default=0)),
            ],
        ),
        migrations.DeleteModel(
            name='Cash',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='ticket_amount',
        ),
        migrations.RenameField(
            model_name='rank',
            old_name='prize_id',
            new_name='amount_id',
        ),
        migrations.RenameField(
            model_name='rank',
            old_name='prize_type',
            new_name='amount_type',
        ),
        migrations.RemoveField(
            model_name='prizestructure',
            name='buyin',
        ),
        migrations.RemoveField(
            model_name='prizestructure',
            name='first_place',
        ),
        migrations.RemoveField(
            model_name='prizestructure',
            name='payout_spots',
        ),
        migrations.RemoveField(
            model_name='prizestructure',
            name='prize_pool',
        ),
        migrations.RemoveField(
            model_name='prizestructure',
            name='round_payouts',
        ),
        migrations.DeleteModel(
            name='Ticket',
        ),
        migrations.AddField(
            model_name='prizestructure',
            name='generator',
            field=models.ForeignKey(null=True, to='prize.GeneratorSettings'),
        ),
    ]
