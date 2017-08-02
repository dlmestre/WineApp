# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchants', '0006_auto_20160715_1301'),
    ]

    operations = [
        migrations.CreateModel(
            name='manual',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wine', models.CharField(max_length=50, verbose_name=b'Wine')),
                ('price', models.CharField(max_length=10, verbose_name=b'Cost')),
                ('year', models.CharField(max_length=10, verbose_name=b'Vintage')),
                ('region', models.CharField(max_length=50, verbose_name=b'Region')),
                ('format', models.CharField(max_length=10, verbose_name=b'Format')),
                ('markup_price', models.CharField(max_length=10, verbose_name=b'Markup Price')),
                ('markup_percentile', models.CharField(max_length=10, verbose_name=b'Markup %')),
            ],
        ),
    ]
