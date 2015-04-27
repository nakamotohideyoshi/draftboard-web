# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_auto_20150408_0015'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ticket', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(null=True, auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TicketAmount',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created', models.DateTimeField(null=True, auto_now_add=True)),
                ('amount', models.DecimalField(max_digits=10, decimal_places=2)),
            ],
        ),
        migrations.AddField(
            model_name='ticket',
            name='amount',
            field=models.ForeignKey(to='ticket.TicketAmount'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='consume_transaction',
            field=models.OneToOneField(related_name='+', to='transaction.Transaction', null=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='deposit_transaction',
            field=models.OneToOneField(to='transaction.Transaction', related_name='+'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
