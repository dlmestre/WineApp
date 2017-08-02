# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchants', '0008_auto_20160722_1718'),
    ]

    operations = [
        migrations.AddField(
            model_name='manual',
            name='quantity',
            field=models.CharField(default=0, max_length=5, verbose_name=b'Qty'),
            preserve_default=False,
        ),
    ]
