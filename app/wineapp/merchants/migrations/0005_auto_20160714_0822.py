# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchants', '0004_auto_20160713_1155'),
    ]

    operations = [
        migrations.AddField(
            model_name='negoces',
            name='margin',
            field=models.CharField(default=None, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='negoces',
            name='sell',
            field=models.CharField(default=None, max_length=5),
            preserve_default=False,
        ),
    ]
