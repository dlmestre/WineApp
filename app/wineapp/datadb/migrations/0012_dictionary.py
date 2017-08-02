# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datadb', '0011_gbphkd'),
    ]

    operations = [
        migrations.CreateModel(
            name='dictionary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=200, verbose_name=b'File name')),
                ('uploadingdate', models.DateTimeField(auto_now=True)),
                ('wineid', models.CharField(max_length=200, verbose_name=b'Wine ID')),
                ('rating', models.CharField(max_length=200, verbose_name=b'Rating')),
                ('vintage', models.CharField(max_length=20, verbose_name=b'Vintage')),
                ('growth', models.CharField(max_length=200, verbose_name=b'Growth')),
                ('typeenglish', models.CharField(max_length=200, verbose_name=b'Type (English)')),
                ('wineenglish', models.CharField(max_length=200, verbose_name=b'Wine (English)')),
                ('countryenglish', models.CharField(max_length=200, verbose_name=b'Country (English)')),
                ('regionenglish', models.CharField(max_length=200, verbose_name=b'Region (English)')),
                ('vendorenglish', models.CharField(max_length=200, verbose_name=b'Vendor (English)')),
                ('typechinese', models.CharField(max_length=200, verbose_name=b'Type (Chinese)')),
                ('winechinese', models.CharField(max_length=200, verbose_name=b'Wine (Chinese)')),
                ('countrychinese', models.CharField(max_length=200, verbose_name=b'Country (Chinese)')),
                ('regionchinese', models.CharField(max_length=200, verbose_name=b'Region (Chinese)')),
                ('vendorchinese', models.CharField(max_length=200, verbose_name=b'Vendor (Chinese)')),
            ],
            options={
                'verbose_name': 'Dictionary Table',
                'verbose_name_plural': 'Dictionary Table',
            },
        ),
    ]
