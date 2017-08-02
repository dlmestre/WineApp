# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchants', '0010_auto_20160728_0940'),
    ]

    operations = [
        migrations.AddField(
            model_name='manual',
            name='negoce',
            field=models.CharField(default=None, max_length=200, verbose_name=b'Negoce'),
            preserve_default=False,
        ),
    ]
