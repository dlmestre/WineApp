# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datadb', '0012_dictionary'),
    ]

    operations = [
        migrations.AddField(
            model_name='dictionary',
            name='a_format',
            field=models.CharField(max_length=200, verbose_name=b'Format', blank=True),
        ),
        migrations.AddField(
            model_name='dictionary',
            name='negoce',
            field=models.CharField(max_length=200, verbose_name=b'Negoce', blank=True),
        ),
        migrations.AddField(
            model_name='dictionary',
            name='quantity',
            field=models.CharField(max_length=20, verbose_name=b'Quantity', blank=True),
        ),
        migrations.AlterField(
            model_name='dictionary',
            name='growth',
            field=models.CharField(max_length=200, verbose_name=b'Growth', blank=True),
        ),
        migrations.AlterField(
            model_name='dictionary',
            name='rating',
            field=models.CharField(max_length=200, verbose_name=b'Rating', blank=True),
        ),
        migrations.AlterField(
            model_name='dictionary',
            name='vintage',
            field=models.CharField(max_length=20, verbose_name=b'Vintage', blank=True),
        ),
    ]
