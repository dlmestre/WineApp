# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datadb', '0013_auto_20170716_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dictionary',
            name='countrychinese',
            field=models.CharField(max_length=200, verbose_name=b'Country (Chinese)', blank=True),
        ),
        migrations.AlterField(
            model_name='dictionary',
            name='countryenglish',
            field=models.CharField(max_length=200, verbose_name=b'Country (English)', blank=True),
        ),
        migrations.AlterField(
            model_name='dictionary',
            name='regionchinese',
            field=models.CharField(max_length=200, verbose_name=b'Region (Chinese)', blank=True),
        ),
        migrations.AlterField(
            model_name='dictionary',
            name='regionenglish',
            field=models.CharField(max_length=200, verbose_name=b'Region (English)', blank=True),
        ),
        migrations.AlterField(
            model_name='dictionary',
            name='typechinese',
            field=models.CharField(max_length=200, verbose_name=b'Type (Chinese)', blank=True),
        ),
        migrations.AlterField(
            model_name='dictionary',
            name='typeenglish',
            field=models.CharField(max_length=200, verbose_name=b'Type (English)', blank=True),
        ),
        migrations.AlterField(
            model_name='dictionary',
            name='vendorchinese',
            field=models.CharField(max_length=200, verbose_name=b'Vendor (Chinese)', blank=True),
        ),
        migrations.AlterField(
            model_name='dictionary',
            name='vendorenglish',
            field=models.CharField(max_length=200, verbose_name=b'Vendor (English)', blank=True),
        ),
        migrations.AlterField(
            model_name='dictionary',
            name='winechinese',
            field=models.CharField(max_length=200, verbose_name=b'Wine (Chinese)', blank=True),
        ),
        migrations.AlterField(
            model_name='dictionary',
            name='wineenglish',
            field=models.CharField(max_length=200, verbose_name=b'Wine (English)', blank=True),
        ),
    ]
