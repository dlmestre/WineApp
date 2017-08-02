# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchants', '0014_auto_20161215_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='negoces2',
            name='cheapest_percent',
            field=models.CharField(default=b'N/A', max_length=10, verbose_name=b'Cheapest Percent'),
        ),
    ]
