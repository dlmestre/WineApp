# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchants', '0009_manual_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='negoces',
            name='quantity',
            field=models.CharField(max_length=5, verbose_name=b'Qty'),
        ),
    ]
