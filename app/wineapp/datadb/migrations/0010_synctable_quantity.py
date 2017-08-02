# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datadb', '0009_auto_20160920_1930'),
    ]

    operations = [
        migrations.AddField(
            model_name='synctable',
            name='quantity',
            field=models.CharField(default=b'N/A', max_length=10, verbose_name=b'Quantity'),
        ),
    ]
