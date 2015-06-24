# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('withdraw', '0002_auto_20150422_1944'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutomaticWithdraw',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('created', models.DateTimeField(null=True, auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('auto_payout_below', models.DecimalField(max_digits=9, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='CashoutWithdrawSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('created', models.DateTimeField(null=True, auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('max_withdraw_amount', models.DecimalField(default=10000.0, max_digits=9, decimal_places=2)),
                ('min_withdraw_amount', models.DecimalField(default=5.0, max_digits=9, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='PendingWithdrawMax',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('created', models.DateTimeField(null=True, auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('max_pending', models.IntegerField(default=3)),
            ],
        ),
        migrations.CreateModel(
            name='ReviewPendingWithdraw',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
        migrations.RemoveField(
            model_name='reviewwithdraw',
            name='cash_transaction_detail',
        ),
        migrations.RemoveField(
            model_name='reviewwithdraw',
            name='status',
        ),
        migrations.AddField(
            model_name='paypalwithdraw',
            name='auth_status',
            field=models.CharField(default='', null=True, max_length=128),
        ),
        migrations.AddField(
            model_name='paypalwithdraw',
            name='get_status',
            field=models.CharField(default='', null=True, max_length=128),
        ),
        migrations.AddField(
            model_name='paypalwithdraw',
            name='payout_status',
            field=models.CharField(default='', null=True, max_length=128),
        ),
        migrations.AddField(
            model_name='paypalwithdraw',
            name='paypal_errors',
            field=models.CharField(default='', max_length=2048),
        ),
        migrations.AddField(
            model_name='paypalwithdraw',
            name='started_processing',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='checkwithdraw',
            name='check_number',
            field=models.IntegerField(unique=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='checkwithdraw',
            name='state',
            field=models.CharField(choices=[('AL', 'AL'), ('AK', 'AK'), ('AR', 'AR'), ('CA', 'CA'), ('CO', 'CO'), ('CT', 'CT'), ('DE', 'DE'), ('FL', 'FL'), ('GA', 'GA'), ('HI', 'HI'), ('ID', 'ID'), ('IL', 'IL'), ('IN', 'IN'), ('KS', 'KS'), ('KY', 'KY'), ('LA', 'LA'), ('ME', 'ME'), ('MD', 'MD'), ('MA', 'MA'), ('MI', 'MI'), ('MN', 'MN'), ('MS', 'MS'), ('MO', 'MO'), ('NE', 'NE'), ('NV', 'NV'), ('NH', 'NH'), ('NJ', 'NJ'), ('NM', 'NM'), ('NY', 'NY'), ('NC', 'NC'), ('ND', 'ND'), ('OH', 'OH'), ('OK', 'OK'), ('OR', 'OR'), ('PA', 'PA'), ('RI', 'RI'), ('SC', 'SC'), ('SD', 'SD'), ('TN', 'TN'), ('TX', 'TX'), ('UT', 'UT'), ('VT', 'VT'), ('VA', 'VA'), ('WV', 'WV'), ('WI', 'WI'), ('WY', 'WY')], default='', max_length=2),
        ),
        migrations.DeleteModel(
            name='ReviewWithdraw',
        ),
    ]
