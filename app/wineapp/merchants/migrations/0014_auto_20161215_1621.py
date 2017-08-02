# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchants', '0013_negoces2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='negoces2',
            name='a_type_chinese',
            field=models.CharField(default=b'N/A', max_length=180, verbose_name=b'Type Chinese'),
        ),
        migrations.AlterField(
            model_name='negoces2',
            name='a_type_english',
            field=models.CharField(default=b'N/A', max_length=180, verbose_name=b'Type English'),
        ),
        migrations.AlterField(
            model_name='negoces2',
            name='country_chinese',
            field=models.CharField(default=b'N/A', max_length=180, verbose_name=b'Country Chinese'),
        ),
        migrations.AlterField(
            model_name='negoces2',
            name='country_english',
            field=models.CharField(default=b'N/A', max_length=180, verbose_name=b'Country English'),
        ),
        migrations.AlterField(
            model_name='negoces2',
            name='vendor_chinese',
            field=models.CharField(default=b'N/A', max_length=180, verbose_name=b'Vendor Chinese'),
        ),
        migrations.AlterField(
            model_name='negoces2',
            name='vendor_english',
            field=models.CharField(default=b'N/A', max_length=180, verbose_name=b'Vendor English'),
        ),
    ]
