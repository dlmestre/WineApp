# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datadb', '0005_auto_20160713_1155'),
    ]

    operations = [
        migrations.CreateModel(
            name='synctable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wine', models.CharField(max_length=50, verbose_name=b'Wine')),
                ('year', models.CharField(max_length=10, verbose_name=b'Vintage')),
                ('region', models.CharField(max_length=50, verbose_name=b'Region')),
                ('format', models.CharField(max_length=10, verbose_name=b'Format')),
                ('price', models.CharField(max_length=10, verbose_name=b'Cost')),
                ('markup_percentile', models.CharField(max_length=10, verbose_name=b'Markup %')),
                ('markup_price', models.CharField(max_length=10, verbose_name=b'Markup Price')),
                ('ws_merchants', models.CharField(max_length=200, verbose_name=b'WS Merchant')),
                ('ws_price', models.CharField(max_length=10, verbose_name=b'Lowest WS Price')),
                ('recommended_price', models.CharField(max_length=10, verbose_name=b'Recommended Selling Price')),
                ('margin', models.CharField(max_length=10, verbose_name=b'Margin')),
                ('sell', models.CharField(max_length=5, verbose_name=b'Sell')),
                ('date', models.CharField(max_length=50, verbose_name=b'Date')),
            ],
            options={
                'verbose_name': 'Sync Table',
                'verbose_name_plural': 'Sync Table',
            },
        ),
    ]
