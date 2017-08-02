# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchants', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='negoces',
            name='recommended_price',
            field=models.CharField(default=None, max_length=10),
            preserve_default=False,
        ),
    ]
