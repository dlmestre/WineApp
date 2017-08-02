# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchants', '0005_auto_20160714_0822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='negoces',
            name='date',
            field=models.CharField(max_length=50, verbose_name=b'Date'),
        ),
        migrations.AlterField(
            model_name='negoces',
            name='format',
            field=models.CharField(max_length=10, verbose_name=b'Format'),
        ),
        migrations.AlterField(
            model_name='negoces',
            name='margin',
            field=models.CharField(max_length=10, verbose_name=b'Margin'),
        ),
        migrations.AlterField(
            model_name='negoces',
            name='markup_percentile',
            field=models.CharField(max_length=10, verbose_name=b'Markup %'),
        ),
        migrations.AlterField(
            model_name='negoces',
            name='markup_price',
            field=models.CharField(max_length=10, verbose_name=b'Markup Price'),
        ),
        migrations.AlterField(
            model_name='negoces',
            name='negoce_name',
            field=models.CharField(max_length=200, verbose_name=b'Negoce'),
        ),
        migrations.AlterField(
            model_name='negoces',
            name='price',
            field=models.CharField(max_length=10, verbose_name=b'Cost'),
        ),
        migrations.AlterField(
            model_name='negoces',
            name='recommended_price',
            field=models.CharField(max_length=10, verbose_name=b'Recommended Selling Price'),
        ),
        migrations.AlterField(
            model_name='negoces',
            name='region',
            field=models.CharField(max_length=50, verbose_name=b'Region'),
        ),
        migrations.AlterField(
            model_name='negoces',
            name='sell',
            field=models.CharField(max_length=5, verbose_name=b'Sell'),
        ),
        migrations.AlterField(
            model_name='negoces',
            name='wine',
            field=models.CharField(max_length=50, verbose_name=b'Wine'),
        ),
        migrations.AlterField(
            model_name='negoces',
            name='ws_merchants',
            field=models.CharField(max_length=200, verbose_name=b'WS Merchant'),
        ),
        migrations.AlterField(
            model_name='negoces',
            name='ws_price',
            field=models.CharField(max_length=10, verbose_name=b'Lowest WS Price'),
        ),
        migrations.AlterField(
            model_name='negoces',
            name='year',
            field=models.CharField(max_length=10, verbose_name=b'Vintage'),
        ),
    ]
