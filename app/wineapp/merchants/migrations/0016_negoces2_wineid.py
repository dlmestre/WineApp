# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchants', '0015_negoces2_cheapest_percent'),
    ]

    operations = [
        migrations.AddField(
            model_name='negoces2',
            name='wineid',
            field=models.CharField(default=None, max_length=80, verbose_name=b'Wine ID'),
            preserve_default=False,
        ),
    ]
