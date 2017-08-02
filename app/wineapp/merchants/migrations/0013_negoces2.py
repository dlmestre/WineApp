# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchants', '0012_auto_20160920_1930'),
    ]

    operations = [
        migrations.CreateModel(
            name='negoces2',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wine', models.CharField(max_length=50, verbose_name=b'Wine')),
                ('year', models.CharField(max_length=10, verbose_name=b'Vintage')),
                ('region_english', models.CharField(max_length=50, verbose_name=b'Region English')),
                ('region_chinese', models.CharField(max_length=50, verbose_name=b'Region Chinese')),
                ('a_format', models.CharField(max_length=10, verbose_name=b'Format')),
                ('negoce_name', models.CharField(max_length=200, verbose_name=b'Negoce')),
                ('price', models.CharField(max_length=10, verbose_name=b'Cost')),
                ('markup_percentile', models.CharField(max_length=10, verbose_name=b'Markup %')),
                ('markup_price', models.CharField(max_length=10, verbose_name=b'Markup Price')),
                ('ws_merchants', models.CharField(max_length=200, verbose_name=b'WS Merchant')),
                ('ws_price', models.CharField(max_length=10, verbose_name=b'Lowest WS Price')),
                ('recommended_price', models.CharField(max_length=10, verbose_name=b'Recommended Selling Price')),
                ('margin', models.CharField(max_length=10, verbose_name=b'Margin')),
                ('sell', models.CharField(max_length=5, verbose_name=b'Sell')),
                ('date', models.CharField(max_length=50, verbose_name=b'Date')),
                ('quantity', models.CharField(max_length=5, verbose_name=b'Qty')),
                ('a_type_english', models.CharField(default=b'N/A', max_length=200, verbose_name=b'Type English')),
                ('a_type_chinese', models.CharField(default=b'N/A', max_length=200, verbose_name=b'Type Chinese')),
                ('vendor_english', models.CharField(default=b'N/A', max_length=200, verbose_name=b'Vendor English')),
                ('vendor_chinese', models.CharField(default=b'N/A', max_length=200, verbose_name=b'Vendor Chinese')),
                ('rating', models.CharField(default=b'N/A', max_length=200, verbose_name=b'Rating')),
                ('growth', models.CharField(default=b'N/A', max_length=200, verbose_name=b'Growth')),
                ('country_english', models.CharField(default=b'N/A', max_length=200, verbose_name=b'Country English')),
                ('country_chinese', models.CharField(default=b'N/A', max_length=200, verbose_name=b'Country Chinese')),
            ],
            options={
                'verbose_name': 'Negoce 2',
                'verbose_name_plural': 'Negoce 2',
            },
        ),
    ]
