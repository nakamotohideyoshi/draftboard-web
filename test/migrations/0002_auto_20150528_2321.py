# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_auto_20150408_0015'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('sports', '0003_auto_20150528_2321'),
        ('auth', '0006_require_contenttypes_0002'),
        ('test', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BalanceChild',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=7)),
                ('transaction_id', models.PositiveIntegerField(null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('transaction_type', models.ForeignKey(to='contenttypes.ContentType', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GameChild',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid', models.CharField(help_text='the sportsradar global id', unique=True, max_length=64)),
                ('start', models.DateTimeField()),
                ('status', models.CharField(max_length=32)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PlayerChild',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid', models.CharField(help_text='the sportsradar global id', unique=True, max_length=64)),
                ('first_name', models.CharField(max_length=32)),
                ('last_name', models.CharField(max_length=32)),
                ('injury_id', models.PositiveIntegerField(null=True)),
                ('injury_type', models.ForeignKey(to='contenttypes.ContentType', null=True, related_name='test_playerchild_players_injury')),
                ('position', models.ForeignKey(to='sports.Position', related_name='test_playerchild_player_position')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PlayerStatsChild',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('srid_game', models.CharField(help_text='the sportsradar global id for the game', max_length=64)),
                ('srid_player', models.CharField(help_text='the sportsradar global id for the player', max_length=64)),
                ('game_id', models.PositiveIntegerField()),
                ('player_id', models.PositiveIntegerField()),
                ('fantasy_points', models.FloatField(default=0.0)),
                ('game_type', models.ForeignKey(to='contenttypes.ContentType', related_name='test_playerstatschild_sport_game')),
                ('player_type', models.ForeignKey(to='contenttypes.ContentType', related_name='test_playerstatschild_sport_player')),
                ('position', models.ForeignKey(to='sports.Position', related_name='test_playerstatschild_playerstats_position')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TransactionDetailChild',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=7)),
                ('created', models.DateTimeField(null=True, auto_now_add=True)),
                ('transaction', models.ForeignKey(to='transaction.Transaction')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='transactiondetailchild',
            unique_together=set([('user', 'transaction')]),
        ),
        migrations.AlterUniqueTogether(
            name='playerstatschild',
            unique_together=set([('srid_player', 'srid_game')]),
        ),
    ]
