# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datadb', '0007_remove_synctable_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='synctable',
            name='negoce',
            field=models.CharField(default=None, max_length=200, verbose_name=b'Negoce'),
            preserve_default=False,
        ),
    ]
