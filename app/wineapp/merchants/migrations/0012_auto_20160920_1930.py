# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchants', '0011_manual_negoce'),
    ]

    operations = [
        migrations.AddField(
            model_name='negoces',
            name='a_type',
            field=models.CharField(default=b'N/A', max_length=200, verbose_name=b'Type'),
        ),
        migrations.AddField(
            model_name='negoces',
            name='vendor',
            field=models.CharField(default=b'N/A', max_length=200, verbose_name=b'Vendor'),
        ),
    ]
