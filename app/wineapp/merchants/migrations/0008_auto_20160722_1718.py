# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchants', '0007_manual'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='manual',
            options={'verbose_name': 'Manual', 'verbose_name_plural': 'Manual'},
        ),
        migrations.AddField(
            model_name='negoces',
            name='quantity',
            field=models.CharField(default=0, max_length=5, verbose_name=b'Sell'),
            preserve_default=False,
        ),
    ]
